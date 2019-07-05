# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class BlackBoard(DingTalkBaseAPI):

    def listtopten(self, userid):
        """
        列出用户的公告列表

        :param userid: 用户id
        """
        return self._top_request(
            "dingtalk.oapi.blackboard.listtopten",
            {"userid": userid}
        )
