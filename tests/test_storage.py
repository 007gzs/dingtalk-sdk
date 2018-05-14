# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest


class WeChatSessionTestCase(unittest.TestCase):

    def test_dingtalk_cache(self, storage=None):
        from dingtalk.storage.cache import DingTalkCache
        if storage is None:
            return
        cache = DingTalkCache(storage)
        cache.access_token.set('crop', 'test1', 7200)
        cache.jsapi_ticket.set('crop', 'test2', 7200)

        self.assertEqual('test1', cache.access_token.get('crop'))
        self.assertEqual('test2', cache.jsapi_ticket.get('crop'))

    def test_channel_cache(self, storage=None):
        from dingtalk.storage.cache import ChannelCache
        if storage is None:
            return
        cache = ChannelCache(storage)
        cache.channel_token.set('crop', 'test3', 7200)
        cache.jsapi_ticket.set('crop', 'test4', 7200)

        self.assertEqual('test3', cache.channel_token.get('crop'))
        self.assertEqual('test4', cache.jsapi_ticket.get('crop'))

    def test_isv_cache(self, storage=None):
        from dingtalk.storage.cache import ISVCache
        if storage is None:
            return
        cache = ISVCache(storage)
        cache.suite_ticket.set('crop', 'test5', 7200)
        cache.suite_access_token.set('crop', 'test6', 7200)
        cache.permanent_code.set('crop', 'test7', 7200)
        cache.ch_permanent_code.set('crop', 'test8', 7200)

        self.assertEqual('test5', cache.suite_ticket.get('crop'))
        self.assertEqual('test6', cache.suite_access_token.get('crop'))
        self.assertEqual('test7', cache.permanent_code.get('crop'))
        self.assertEqual('test8', cache.ch_permanent_code.get('crop'))

    def test_caches(self, storage=None):
        if storage is None:
            return
        self.test_dingtalk_cache(storage)
        self.test_channel_cache(storage)
        self.test_isv_cache(storage)

    def test_memory_storage(self):
        from dingtalk.storage.memorystorage import MemoryStorage

        storage = MemoryStorage()
        self.test_caches(storage)

    def test_redis_storage(self):
        from redis import Redis
        from dingtalk.storage.kvstorage import KvStorage
        redis = Redis()
        storage = KvStorage(redis)
        self.test_caches(storage)

    def test_memcache_storage(self):
        from pymemcache.client import Client
        from dingtalk.storage.kvstorage import KvStorage
        servers = ("127.0.0.1", 11211)
        memcached = Client(servers)
        storage = KvStorage(memcached)
        self.test_caches(storage)
