# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect

from dingtalk.storage import BaseStorage


def _is_cache_item(obj):
    return isinstance(obj, DingTalkCacheItem)


class DingTalkCacheItem(object):

    def __init__(self, cache=None, name=None):
        self.cache = cache
        self.name = name

    def key_name(self, key):
        if isinstance(key, (tuple, list)):
            key = ':'.join(key)

        k = '{0}:{1}'.format(self.cache.prefix, self.name)
        if key is not None:
            k = '{0}:{1}'.format(k, key)
        return k

    def get(self, key=None, default=None):
        return self.cache.storage.get(self.key_name(key), default)

    def set(self, key=None, value=None, ttl=None):
        return self.cache.storage.set(self.key_name(key), value, ttl)

    def delete(self, key=None):
        return self.cache.storage.delete(self.key_name(key))


class BaseCache(object):

    def __new__(cls, *args, **kwargs):
        self = super(BaseCache, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_cache_item)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self, name)
            setattr(self, name, api)
        return self

    def __init__(self, storage, prefix='client'):
        assert isinstance(storage, BaseStorage)
        self.storage = storage
        self.prefix = prefix


class DingTalkCache(BaseCache):
    access_token = DingTalkCacheItem()
    jsapi_ticket = DingTalkCacheItem()


class ChannelCache(BaseCache):
    channel_token = DingTalkCacheItem()
    jsapi_ticket = DingTalkCacheItem()


class ISVCache(BaseCache):
    suite_ticket = DingTalkCacheItem()
    suite_access_token = DingTalkCacheItem()
    permanent_code = DingTalkCacheItem()
    ch_permanent_code = DingTalkCacheItem()
