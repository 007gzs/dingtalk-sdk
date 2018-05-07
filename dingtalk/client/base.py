# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import json
import logging
import requests
from six.moves.urllib_parse import urljoin

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.core.exceptions import DingTalkClientException
from dingtalk.storage.memorystorage import MemoryStorage


logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, DingTalkBaseAPI)


class BaseClient(object):

    _http = requests.Session()

    API_BASE_URL = 'https://oapi.dingtalk.com/'

    def __new__(cls, *args, **kwargs):
        self = super(BaseClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, storage=None, timeout=None, auto_retry=True):
        self.storage = storage or MemoryStorage()
        self.timeout = timeout
        self.auto_retry = auto_retry

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = urljoin(api_base_url, url_or_endpoint)
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Content-Type'] = 'application/json'

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【异常信息】：%s",
                         url, kwargs.get('params', ''), kwargs.get('data', ''), reqe)
            raise DingTalkClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )

        result = self._handle_result(
            res, method, url, result_processor, **kwargs
        )

        logger.debug("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【响应数据】：%s",
                     url, kwargs.get('params', ''), kwargs.get('data', ''), result)
        return result

    def _decode_result(self, res):
        try:
            result = json.loads(res.content.decode('utf-8', 'ignore'), strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            logger.debug('Can not decode response as JSON', exc_info=True)
            return res
        return result

    def _handle_result(self, res, method=None, url=None, result_processor=None, **kwargs):
        if not isinstance(res, dict):
            # Dirty hack around asyncio based AsyncWeChatClient
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result

        if 'errcode' in result:
            result['errcode'] = int(result['errcode'])

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result.get('errmsg', errcode)

            logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                         url, kwargs.get('params', ''), kwargs.get('data', ''), result)
            raise DingTalkClientException(
                errcode,
                errmsg,
                client=self,
                request=res.request,
                response=res
            )

        return result if not result_processor else result_processor(result)

    def _handle_pre_request(self, method, uri, kwargs):
        return method, uri, kwargs

    def _handle_pre_top_request(self, params, uri):
        return params, uri

    def _handle_request_except(self, e, func, *args, **kwargs):
        raise e

    def request(self, method, uri, **kwargs):
        method, uri_with_access_token, kwargs = self._handle_pre_request(method, uri, kwargs)
        try:
            return self._request(method, uri_with_access_token, **kwargs)
        except DingTalkClientException as e:
            return self._handle_request_except(e, self.request, method, uri, **kwargs)

    def top_request(self, method=None, params=None, format_='json', v='2.0',
                    simplify='false', partner_id=None, url=None, **kwargs):
        from datetime import datetime
        if params is None:
            reqparams = {}
        else:
            reqparams = params.copy()
        reqparams['method'] = method
        reqparams['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        reqparams['format'] = format
        reqparams['v'] = v

        if format_ == 'json':
            reqparams['simplify'] = simplify
        if partner_id:
            reqparams['partner_id'] = partner_id

        base_url = url or '/router/rest'

        if not base_url.startswith(('http://', 'https://')):
            base_url = urljoin(self.API_BASE_URL, base_url)

        try:
            return self._request('POST', base_url, params=reqparams)
        except DingTalkClientException as e:
            return self._handle_request_except(e, self.request,
                                               method, format_, v, simplify, partner_id, url, params, **kwargs)

    def get(self, uri, params=None, **kwargs):
        if params is not None:
            kwargs['params'] = params
        return self.request('GET', uri, **kwargs)

    def post(self, uri, data=None, params=None, **kwargs):
        if data is not None:
            kwargs['data'] = data
        if params is not None:
            kwargs['params'] = params
        return self.request('POST', uri, **kwargs)
