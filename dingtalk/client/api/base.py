# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class DingTalkBaseAPI(object):

    API_BASE_URL = None

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, params=None, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, params, **kwargs)

    def _post(self, url, data=None, params=None, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, data, params, **kwargs)

    def _top_request(self, method, params=None, format_='json', v='2.0',
                     simplify='false', partner_id=None, url=None, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.top_request(method, params, format_, v, simplify, partner_id, url, **kwargs)

    @property
    def corp_id(self):
        return self._client.corp_id
