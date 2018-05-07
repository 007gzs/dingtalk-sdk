# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class User(DingTalkBaseAPI):

    def getuserinfo(self, code):
        """
        通过CODE换取用户身份
        :param code: requestAuthCode接口中获取的CODE
        :return:
        """
        return self._get(
            '/user/getuserinfo',
            {'code': code}
        )
