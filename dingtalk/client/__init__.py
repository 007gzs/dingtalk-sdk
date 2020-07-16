# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import time

from dingtalk.client import api
from dingtalk.client.api.taobao import TaobaoMixin
from dingtalk.client.base import BaseClient
from dingtalk.core.utils import DingTalkSigner, random_string
from dingtalk.crypto import DingTalkCrypto
from dingtalk.storage.cache import DingTalkCache

logger = logging.getLogger(__name__)


class DingTalkClient(BaseClient, TaobaoMixin):

    attendance = api.Attendance()
    blackboard = api.BlackBoard()
    bpms = api.Bpms()
    calendar = api.Calendar()
    callback = api.Callback()
    chat = api.Chat()
    checkin = api.Checkin()
    cspace = api.Cspace()
    department = api.Department()
    ext = api.Ext()
    extcontact = api.ExtContact()
    employeerm = api.Employeerm()
    health = api.Health()
    message = api.Message()
    microapp = api.MicroApp()
    report = api.Report()
    role = api.Role()
    user = api.User()
    workrecord = api.WorkRecord()

    def __init__(self, corp_id, prefix='client', storage=None, timeout=None, auto_retry=True):
        super(DingTalkClient, self).__init__(storage, timeout, auto_retry)
        self.corp_id = corp_id
        self.cache = DingTalkCache(self.storage, "%s:%s" % (prefix, self.get_access_token_key()))

    def get_access_token_key(self):
        return "corp_id:%s" % self.corp_id

    @property
    def access_token(self):
        token = self.cache.access_token.get()
        if token is None:
            ret = self.get_access_token()
            token = ret['access_token']
            expires_in = ret.get('expires_in', 7200)
            self.cache.access_token.set(value=token, ttl=expires_in)
        return token

    @property
    def jsapi_ticket(self):
        ticket = self.cache.jsapi_ticket.get()
        if ticket is None:
            ret = self.get_jsapi_ticket()
            ticket = ret['ticket']
            expires_in = ret.get('expires_in', 7200)
            self.cache.jsapi_ticket.set(value=ticket, ttl=expires_in)
        return ticket

    def get_jsapi_params(self, url, noncestr=None, timestamp=None):
        if not noncestr:
            noncestr = random_string()
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        data = [
            'noncestr={noncestr}'.format(noncestr=noncestr),
            'jsapi_ticket={ticket}'.format(ticket=self.jsapi_ticket),
            'timestamp={timestamp}'.format(timestamp=timestamp),
            'url={url}'.format(url=url),
        ]
        signer = DingTalkSigner(delimiter=b'&')
        signer.add_data(*data)

        ret = {
            'corpId': self.corp_id,
            'timeStamp': timestamp,
            'nonceStr': noncestr,
            'signature': signer.signature
        }
        return ret

    def _handle_pre_request(self, method, uri, kwargs):
        if 'access_token=' in uri or 'access_token' in kwargs.get('params', {}):
            raise ValueError("uri参数中不允许有access_token: " + uri)
        uri = '%s%saccess_token=%s' % (uri, '&' if '?' in uri else '?', self.access_token)
        return method, uri, kwargs

    def _handle_pre_top_request(self, params, uri):
        if 'session=' in uri or 'session' in params:
            raise ValueError("uri参数中不允许有session: " + uri)
        params['session'] = self.access_token

        return super(DingTalkClient, self)._handle_pre_top_request(params, uri)

    def _handle_request_except(self, e, func, *args, **kwargs):
        if e.errcode in (33001, 40001, 42001, 40014):
            self.cache.access_token.delete()
            if self.auto_retry:
                return func(*args, **kwargs)
        raise e

    def get_jsapi_ticket(self):
        return self.get('/get_jsapi_ticket')

    def get_access_token(self):
        raise NotImplementedError


class SecretClient(DingTalkClient):

    def __init__(self, corp_id, corp_secret, token=None, aes_key=None, storage=None, timeout=None, auto_retry=True):
        super(SecretClient, self).__init__(corp_id, 'secret:'+corp_id, storage, timeout, auto_retry)
        self.corp_secret = corp_secret
        self.crypto = DingTalkCrypto(token, aes_key, corp_id)

    def get_access_token(self):
        return self._request(
            'GET',
            '/gettoken',
            params={'corpid': self.corp_id, 'corpsecret': self.corp_secret}
        )


class AppKeyClient(DingTalkClient):

    def __init__(self, corp_id, app_key, app_secret, token=None, aes_key=None, storage=None, timeout=None,
                 auto_retry=True):
        self.app_key = app_key
        self.app_secret = app_secret
        super(AppKeyClient, self).__init__(corp_id, 'secret:' + corp_id, storage, timeout, auto_retry)
        self.crypto = DingTalkCrypto(token, aes_key, corp_id)

    def get_access_token_key(self):
        return "app_key:%s" % self.app_key

    def get_access_token(self):
        return self._request(
            'GET',
            '/gettoken',
            params={'appkey': self.app_key, 'appsecret': self.app_secret}
        )
