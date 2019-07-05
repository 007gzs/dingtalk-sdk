# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import datetime

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.core.utils import to_text


class Health(DingTalkBaseAPI):

    def stepinfo_getuserstatus(self, userid):
        """
        查询用户是否开启了钉钉运动

        :param userid: 用户id
        """
        return self._top_request(
            "dingtalk.oapi.health.stepinfo.getuserstatus",
            {"userid": userid},
            result_processor=lambda x: x['status']
        )

    def stepinfo_list(self, _type, object_id, stat_dates):
        """
        获取个人或部门钉钉运动步数

        :param _type: 0表示取用户步数，1表示取部门步数
        :param object_id: 可以传入用户userid或者部门id
        :param stat_dates: 时间列表
        """
        if not isinstance(stat_dates, (list, tuple, set)):
            stat_dates = [stat_dates]

        stat_dates = ",".join(map(lambda x: x.strftime("%Y%m%d") if isinstance(x, datetime.date) else x, stat_dates))
        return self._top_request(
            "dingtalk.oapi.health.stepinfo.list",
            {
                "type": _type,
                "object_id": object_id,
                "stat_dates": stat_dates
            }
        )

    def stepinfo_listbyuserid(self, userids, stat_date):
        """
        批量查询多个用户的钉钉运动步数

        :param userids: 员工userid列表，最多传50个
        :param stat_date: 时间
        """
        if isinstance(stat_date, datetime.date):
            stat_date = stat_date.strftime("%Y%m%d")
        if isinstance(userids, (list, tuple, set)):
            userids = ",".join(map(to_text, userids))
        return self._top_request(
            "dingtalk.oapi.health.stepinfo.listbyuserid",
            {
                "userids": userids,
                "stat_date": stat_date
            }
        )
