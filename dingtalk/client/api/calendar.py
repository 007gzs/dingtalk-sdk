# encoding: utf-8
from __future__ import absolute_import, unicode_literals


from dingtalk.client.api.base import DingTalkBaseAPI


class Calendar(DingTalkBaseAPI):

    def create(self, create_vo):
        """
        创建日程

        :param create_vo: 创建日程实体
        """
        return self._top_request(
            "dingtalk.oapi.calendar.create",
            {"create_vo": create_vo}
        )

    def list(
            self,
            user_id,
            calendar_folder_id='',
            time_min=None,
            i_cal_uid='',
            single_events='',
            page_token='',
            max_results=250,
            time_max=None
    ):
        """
        日程查询

        :param user_id: 员工ID
        :param calendar_folder_id: 钉钉日历文件夹的对外id，默认是自己的默认文件夹
        :param time_min: 查询时间下限
        :param i_cal_uid: 日程跨域唯一id，用于唯一标识一组关联日程事件
        :param single_events: 是否需要展开循环日程
        :param page_token: 查询对应页，值有上一次请求返回的结果里对应nextPageToken
        :param max_results: 结果返回的最多数量，默认250，最多返回2500
        :param time_max: 查询时间上限
        """
        return self._top_request(
            "dingtalk.oapi.calendar.list",
            {
                "user_id": user_id,
                "calendar_folder_id": calendar_folder_id,
                "time_min": time_min,
                "i_cal_uid": i_cal_uid,
                "single_events": single_events,
                "page_token": page_token,
                "max_results": max_results,
                "time_max": time_max
            }
        )

    def delete(self, userid='', calendar_id=''):
        """
        日程删除

        :param userid: 员工id
        :param calendar_id: 日程id
        """
        return self._top_request(
            "dingtalk.oapi.calendar.delete",
            {
                "userid": userid,
                "calendar_id": calendar_id
            }
        )
