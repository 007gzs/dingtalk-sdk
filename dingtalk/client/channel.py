# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import time

from dingtalk.client.base import BaseClient
from dingtalk.core.utils import random_string, DingTalkSigner
from dingtalk.storage.cache import ChannelCache

logger = logging.getLogger(__name__)


class ChannelClient(BaseClient):

    def __init__(self, corp_id, prefix='channel', storage=None, timeout=None, auto_retry=True):
        super(ChannelClient, self).__init__(storage, timeout, auto_retry)
        self.corp_id = corp_id
        self.cache = ChannelCache(self.storage, prefix)

    def _handle_pre_request(self, method, uri, kwargs):
        if 'access_token=' in uri or 'access_token' in kwargs.get('params', {}):
            raise ValueError("access_token: " + uri)
        uri = '%s%access_token=%s' % (uri, '&' if '?' in uri else '?', self.channel_token)
        return method, uri, kwargs

    def _handle_request_except(self, e, func, *args, **kwargs):
        if e.errcode in (33001, 40001, 42001, 40014):
            self.cache.channel_token.delete()
            if self.auto_retry:
                return func(*args, **kwargs)
        raise e

    @property
    def channel_token(self):
        self.cache.channel_token.get()
        token = self.cache.channel_token.get()
        if token is None:
            ret = self.get_channel_token()
            token = ret['access_token']
            expires_in = ret.get('expires_in', 7200)
            self.cache.channel_token.set(value=token, ttl=expires_in)
        return token

    @property
    def channel_jsapi_ticket(self):
        ticket = self.cache.jsapi_ticket.get()
        if ticket is None:
            ret = self.get_channel_jsapi_ticket()
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
            'jsapi_ticket={ticket}'.format(ticket=self.channel_jsapi_ticket),
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

    def get_channel_token(self):
        raise NotImplementedError

    def get_channel_jsapi_ticket(self):
        """
        获取企业服务窗JSAPI鉴权ticket

        :return:
        """
        return self.get('/channel/get_channel_jsapi_ticket')

    def get_user_list(self, offset=0, size=100):
        """
        获取服务窗关注者列表

        :param offset: 偏移量,必须大于等于0
        :param size: 获取数量,大于等于0,小于等于100
        :return:
        """
        return self.get(
            '/channel/user/list',
            {"offset": offset, "size": size}
        )

    def get_by_openid(self, openid):
        """
        获取关注者详情

        :param openid: 在本服务窗运营服务商 范围内,唯一标识关注者身份的id
        :return:
        """
        return self.get(
            '/channel/user/get_by_openid',
            {"openid": openid}
        )

    def get_by_code(self, code):
        """
        关注者免登接口

        :param code: 服务窗关注者在服务窗应用中免登时生成的临时授权码
        :return:
        """
        return self.get(
            '/channel/user/get_by_code',
            {"code": code}
        )


class SecretChannelClient(ChannelClient):
    def __init__(self, corp_id, channel_secret, storage=None, timeout=None, auto_retry=True):
        super(SecretChannelClient, self).__init__(corp_id, storage, timeout, auto_retry)
        self.channel_secret = channel_secret
        self.cache = ChannelCache(self.storage, 'channelsecret:' + self.corp_id)

    def get_channel_token(self):
        """
        获取服务窗ChannelToken

        :return:
        """
        return self.get(
            '/channel/get_channel_token',
            {"corpid": self.corp_id, "channel_secret": self.channel_secret}
        )
