# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import datetime
import time

from dingtalk.client.api.base import DingTalkBaseAPI


class Report(DingTalkBaseAPI):

    def list(self, start_time, end_time, cursor=0, size=20, template_name='', userid=''):
        """
        查询企业员工发出的日志列表

        :param start_time: 查询起始时间
        :param end_time: 查询截止时间
        :param cursor: 查询游标，初始传入0，后续从上一次的返回值中获取
        :param size: 每页数据量
        :param template_name: 要查询的模板名称
        :param userid: 员工的userid
        """
        if isinstance(start_time, (datetime.date, datetime.datetime)):
            start_time = int(time.mktime(start_time.timetuple()) * 1000)
        if isinstance(end_time, (datetime.date, datetime.datetime)):
            end_time = int(time.mktime(end_time.timetuple()) * 1000)
        return self._top_request(
            "dingtalk.oapi.report.list",
            {
                "start_time": start_time,
                "end_time": end_time,
                "cursor": cursor,
                "size": size,
                "template_name": template_name,
                "userid": userid
            }
        )

    def statistics(self, report_id):
        """
        获取日志统计数据

        :param report_id: 日志id
        """
        return self._top_request(
            "dingtalk.oapi.report.statistics",
            {
                "report_id": report_id
            }
        )

    def statistics_listbytype(self, report_id, _type, offset=0, size=100):
        """
        根据类型获取日志相关人员列表

        :param report_id: 日志id
        :param _type: 查询类型 0:已读人员列表 1:评论人员列表 2:点赞人员列表
        :param offset: 分页查询的游标，最开始传0，后续传返回参数中的next_cursor值，默认值为0
        :param size: 分页参数，每页大小，最多传100，默认值为100
        """
        return self._top_request(
            "dingtalk.oapi.report.statistics.listbytype",
            {
                "report_id": report_id,
                "type": _type,
                "offset": offset,
                "size": size
            }
        )

    def receiver_list(self, report_id, offset=0, size=100):
        """
        获取日志分享人员列表

        :param report_id: 日志id
        :param offset: 分页查询的游标，最开始传0，后续传返回参数中的next_cursor值，默认值为0
        :param size: 分页参数，每页大小，最多传100，默认值为100
        """
        return self._top_request(
            "dingtalk.oapi.report.receiver.list",
            {
                "report_id": report_id,
                "offset": offset,
                "size": size
            }
        )

    def comment_list(self, report_id, offset=0, size=20):
        """
        获取日志评论详情

        :param report_id: 日志id
        :param offset: 分页查询的游标，最开始传0，后续传返回参数中的next_cursor值，默认值为0
        :param size: 分页参数，每页大小，最多传20，默认值为20
        """
        return self._top_request(
            "dingtalk.oapi.report.comment.list",
            {
                "report_id": report_id,
                "offset": offset,
                "size": size
            }
        )

    def getunreadcount(self, userid=''):
        """
        查询企业员工的日志未读数

        :param userid: 员工id
        """
        return self._top_request(
            "dingtalk.oapi.report.getunreadcount",
            {"userid": userid},
            result_processor=lambda x: x['count']
        )

    def template_listbyuserid(self, userid='', offset=0, size=100):
        """
        根据用户id获取可见的日志模板列表

        :param userid: 员工userId, 不传递表示获取所有日志模板
        :param offset: 分页游标，从0开始。根据返回结果里的next_cursor是否为空来判断是否还有下一页，且再次调用时offset设置成next_cursor的值
        :param size: 分页大小，最大可设置成100
        """
        return self._top_request(
            "dingtalk.oapi.report.template.listbyuserid",
            {
                "userid": userid,
                "offset": offset,
                "size": size
            }
        )
