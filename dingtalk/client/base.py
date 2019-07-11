# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import json
import logging
import requests
import six
from six.moves.urllib.parse import urljoin

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.core.exceptions import DingTalkClientException
from dingtalk.core.utils import json_loads
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
        top_response_key = kwargs.pop('top_response_key', None)
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
            res, method, url, result_processor, top_response_key, **kwargs
        )

        logger.debug("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【响应数据】：%s",
                     url, kwargs.get('params', ''), kwargs.get('data', ''), result)
        return result

    def _decode_result(self, res):
        try:
            result = json_loads(res.content.decode('utf-8', 'ignore'), strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            logger.debug('Can not decode response as JSON', exc_info=True)
            return res
        return result

    def _handle_result(self, res, method=None, url=None, result_processor=None, top_response_key=None, **kwargs):
        if not isinstance(res, dict):
            # Dirty hack around asyncio based AsyncWeChatClient
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result
        if top_response_key:
            if 'error_response' in result:
                error_response = result['error_response']
                logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                             url, kwargs.get('params', ''), kwargs.get('data', ''), result)
                raise DingTalkClientException(
                    error_response.get('code', -1),
                    error_response.get('sub_msg', error_response.get('msg', '')),
                    client=self,
                    request=res.request,
                    response=res
                )
            top_result = result
            if top_response_key in top_result:
                top_result = result[top_response_key]
                if 'result' in top_result:
                    top_result = top_result['result']
                    if isinstance(top_result, six.string_types):
                        try:
                            top_result = json_loads(top_result)
                        except Exception:
                            pass
            if isinstance(top_result, dict):
                if ('success' in top_result and not top_result['success']) or (
                        'is_success' in top_result and not top_result['is_success']):
                    logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                                 url, kwargs.get('params', ''), kwargs.get('data', ''), result)
                    raise DingTalkClientException(
                        top_result.get('ding_open_errcode', -1),
                        top_result.get('error_msg', ''),
                        client=self,
                        request=res.request,
                        response=res
                    )
            result = top_result
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
        if not uri.startswith(('http://', 'https://')):
            uri = urljoin('https://eco.taobao.com', uri)
        return params, uri

    def _handle_request_except(self, e, func, *args, **kwargs):
        raise e

    def request(self, method, uri, **kwargs):
        method, uri_with_access_token, kwargs = self._handle_pre_request(method, uri, kwargs)
        try:
            return self._request(method, uri_with_access_token, **kwargs)
        except DingTalkClientException as e:
            return self._handle_request_except(e, self.request, method, uri, **kwargs)

    def top_request(self, method, params=None, format_='json', v='2.0',
                    simplify='false', partner_id=None, url=None, **kwargs):
        """
        top 接口请求

        :param method: API接口名称。
        :param params: 请求参数 （dict 格式）
        :param format_: 响应格式（默认json，如果使用xml，需要自己对返回结果解析）
        :param v: API协议版本，可选值：2.0。
        :param simplify: 是否采用精简JSON返回格式
        :param partner_id: 合作伙伴身份标识。
        :param url: 请求url，默认为 https://eco.taobao.com/router/rest
        """
        from datetime import datetime

        reqparams = {}
        if params is not None:
            for key, value in params.items():
                reqparams[key] = value if not isinstance(value, (dict, list, tuple)) else json.dumps(value)
        reqparams['method'] = method
        reqparams['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        reqparams['format'] = format_
        reqparams['v'] = v

        if format_ == 'json':
            reqparams['simplify'] = simplify
        if partner_id:
            reqparams['partner_id'] = partner_id
        base_url = url or '/router/rest'

        reqparams, base_url = self._handle_pre_top_request(reqparams, base_url)

        if not base_url.startswith(('http://', 'https://')):
            base_url = urljoin(self.API_BASE_URL, base_url)
        response_key = method.replace('.', '_') + "_response"
        try:
            return self._request('POST', base_url, params=reqparams, top_response_key=response_key, **kwargs)
        except DingTalkClientException as e:
            return self._handle_request_except(e, self.request,
                                               method, format_, v, simplify, partner_id, url, params, **kwargs)

    def get(self, uri, params=None, **kwargs):
        """
        get 接口请求

        :param uri: 请求url
        :param params: get 参数（dict 格式）
        """
        if params is not None:
            kwargs['params'] = params
        return self.request('GET', uri, **kwargs)

    def post(self, uri, data=None, params=None, **kwargs):
        """
        post 接口请求

        :param uri: 请求url
        :param data: post 数据（dict 格式会自动转换为json）
        :param params: post接口中url问号后参数（dict 格式）
        """
        if data is not None:
            kwargs['data'] = data
        if params is not None:
            kwargs['params'] = params
        return self.request('POST', uri, **kwargs)
