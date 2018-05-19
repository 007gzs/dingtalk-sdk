# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from dingtalk.core.utils import to_text, json_loads
from dingtalk.client import DingTalkClient
from dingtalk.client.base import BaseClient
from dingtalk.client.channel import ChannelClient
from dingtalk.core.constants import SuitePushType
from dingtalk.crypto import DingTalkCrypto
from dingtalk.storage.cache import ISVCache

logger = logging.getLogger(__name__)


class ISVDingTalkClient(DingTalkClient):
    def __init__(self, corp_id, isv_client):
        super(ISVDingTalkClient, self).__init__(corp_id, 'isv_auth:' + isv_client.suite_key,
                                                isv_client.storage, isv_client.timeout, isv_client.auto_retry)
        self.isv_client = isv_client

    def get_access_token(self):
        return self.isv_client.get_access_token_by_corpid(self.corp_id)


class ISVChannelClient(ChannelClient):
    def __init__(self, corp_id, isv_client):
        super(ISVChannelClient, self).__init__(corp_id, 'isv_channel:' + isv_client.suite_key,
                                               isv_client.storage, isv_client.timeout, isv_client.auto_retry)
        self.isv_client = isv_client

    def get_channel_token(self):
        return self.isv_client.get_channel_token_by_corpid(self.corp_id)


class ISVClient(BaseClient):

    def __init__(self, suite_key, suite_secret, token=None, aes_key=None, storage=None, timeout=None, auto_retry=True):
        super(ISVClient, self).__init__(storage, timeout, auto_retry)
        self.suite_key = suite_key
        self.suite_secret = suite_secret
        self.cache = ISVCache(self.storage, 'isv:' + self.suite_key)
        self.crypto = DingTalkCrypto(token, aes_key, suite_key)

    def _handle_pre_request(self, method, uri, kwargs):
        if 'suite_access_token=' in uri or 'suite_access_token' in kwargs.get('params', {}):
            raise ValueError("suite_access_token: " + uri)
        uri = '%s%ssuite_access_token=%s' % (uri, '&' if '?' in uri else '?', self.suite_access_token)
        return method, uri, kwargs

    def _handle_request_except(self, e, func, *args, **kwargs):
        if e.errcode in (33001, 40001, 42001, 40014):
            self.cache.suite_access_token.delete()
            if self.auto_retry:
                return func(*args, **kwargs)
        raise e

    def set_suite_ticket(self, suite_ticket):
        self.cache.suite_ticket.set(value=suite_ticket)

    @property
    def suite_access_token(self):
        self.cache.suite_access_token.get()
        token = self.cache.suite_access_token.get()
        if token is None:
            ret = self.get_suite_access_token()
            token = ret['suite_access_token']
            expires_in = ret.get('expires_in', 7200)
            self.cache.suite_access_token.set(value=token, ttl=expires_in)
        return token

    def _handle_permanent_code(self, permanent_code_data):
        permanent_code = permanent_code_data.get('permanent_code', None)
        ch_permanent_code = permanent_code_data.get('ch_permanent_code', None)
        corp_id = permanent_code_data.get('auth_corp_info', {}).get('corpid', None)
        if corp_id is None:
            return
        if permanent_code is not None:
            self.cache.permanent_code.set(corp_id, permanent_code)
        if ch_permanent_code is not None:
            self.cache.ch_permanent_code.set(corp_id, ch_permanent_code)

    def get_dingtalk_client(self, corp_id):
        return ISVDingTalkClient(corp_id, self)

    def get_channel_client(self, corp_id):
        return ISVChannelClient(corp_id, self)

    def proc_message(self, message):
        if not isinstance(message, dict):
            return
        event_type = message.get('EventType', None)

        if event_type == SuitePushType.SUITE_TICKET.value:
            suite_ticket = message.get('SuiteTicket', None)
            if suite_ticket:
                self.set_suite_ticket(suite_ticket)
            return
        elif event_type == SuitePushType.TMP_AUTH_CODE.value:
            auth_code = message.get('AuthCode')
            permanent_code_data = self.get_permanent_code(auth_code)
            message['__permanent_code_data'] = permanent_code_data
            return
        elif event_type == SuitePushType.SUITE_RELIEVE.value:
            corp_id = message.get('AuthCorpId')
            self.cache.permanent_code.delete(corp_id)
            self.cache.ch_permanent_code.delete(corp_id)
            return
        else:
            return

    def parse_message(self, msg, signature, timestamp, nonce):
        message = self.crypto.decrypt_message(msg, signature, timestamp, nonce)
        try:
            message = json_loads(to_text(message))
            self.proc_message(message)
        except Exception as e:
            logger.error("proc_message error %s %s", message, e)
        return message

    def get_ch_permanent_code_from_cache(self, corp_id):
        return self.cache.ch_permanent_code.get(corp_id)

    def get_permanent_code_from_cache(self, corp_id):
        return self.cache.permanent_code.get(corp_id)

    def get_suite_access_token(self):
        """
        获取应用套件令牌Token

        :return:
        """
        return self._request(
            'post',
            '/service/get_suite_token',
            data={
                "suite_key": self.suite_key,
                "suite_secret": self.suite_secret,
                "suite_ticket": self.cache.suite_ticket.get()
            }
        )

    def get_permanent_code(self, tmp_auth_code):
        """
        获取企业授权的永久授权码

        :param tmp_auth_code: 回调接口（tmp_auth_code）获取的临时授权码
        :return:
        """
        permanent_code_data = self.post(
            '/service/get_permanent_code',
            {'tmp_auth_code': tmp_auth_code}
        )
        self._handle_permanent_code(permanent_code_data)
        return permanent_code_data

    def activate_suite(self, corp_id):
        """
        激活套件

        :param corp_id: 授权方corpid
        :return:
        """
        return self.post(
            '/service/activate_suite',
            {
                'suite_key': self.suite_key,
                'auth_corpid': corp_id,
                'permanent_code': self.cache.permanent_code.get(corp_id)}
        )

    def get_access_token_by_corpid(self, corp_id):
        """
        获取企业授权的凭证

        :param corp_id: 授权方corpid
        :return:
        """
        return self.post(
            '/service/get_corp_token',
            {'auth_corpid': corp_id, 'permanent_code': self.cache.permanent_code.get(corp_id)}
        )

    def get_auth_info(self, corp_id):
        """
        获取企业基本信息

        :param corp_id: 授权方corpid
        :return:
        """
        return self.post(
            '/service/get_auth_info',
            {'auth_corpid': corp_id, 'suite_key': self.suite_key}
        )

    def get_agent(self, corp_id, agent_id):
        """
        获取企业的应用信息

        :param corp_id: 授权方corpid
        :param agent_id: 授权方应用id
        :return:
        """
        return self.post(
            '/service/get_agent',
            {
                'suite_key': self.suite_key,
                'auth_corpid': corp_id,
                'agentid': agent_id,
                'permanent_code': self.get_permanent_code_from_cache(corp_id)
            }
        )

    def get_unactive_corp(self, app_id):
        """
        获取应用未激活的企业列表

        :param app_id: 套件下的微应用ID
        :return:
        """
        return self.post(
            '/service/get_unactive_corp',
            {'app_id': app_id}
        )

    def reauth_corp(self, app_id, corpid_list):
        """
        重新授权未激活应用的企业

        :param app_id: 套件下的微应用ID
        :param corpid_list: 未激活的corpid列表
        :return:
        """
        return self.post(
            '/service/reauth_corp',
            {'app_id': app_id, 'corpid_list': corpid_list}
        )

    def set_corp_ipwhitelist(self, corp_id, ip_whitelist):
        """
        ISV为授权方的企业单独设置IP白名单

        :param corp_id: 授权方corpid
        :param ip_whitelist: 要为其设置的IP白名单,格式支持IP段,用星号表示,注意:仅支持后两段设置为星号
        :return:
        """
        return self.post(
            '/service/set_corp_ipwhitelist',
            {'auth_corpid': corp_id, 'ip_whitelist': ip_whitelist}
        )

    def get_channel_token_by_corpid(self, corp_id):
        """
        ISV获取企业服务窗接口调用TOKEN

        :param corp_id: 授权方corpid
        :return:
        """
        return self.post(
            '/service/get_channel_corp_token',
            {'auth_corpid': corp_id, 'ch_permanent_code': self.get_ch_permanent_code_from_cache(corp_id)}
        )
