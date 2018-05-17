# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime

from dingtalk.client.api.base import DingTalkBaseAPI


class Attendance(DingTalkBaseAPI):

    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def list_record(self, user_ids, check_date_from, check_date_to):
        """
        考勤打卡记录开放

        :param user_ids: 企业内的员工id列表，最多不能超过50个
        :param check_date_from: 查询考勤打卡记录的起始工作日
        :param check_date_to: 查询考勤打卡记录的结束工作日。注意，起始与结束工作日最多相隔7天
        :return:
        """
        if isinstance(check_date_from, (datetime.date, datetime.datetime)):
            check_date_from = check_date_from.strftime(self.DATE_TIME_FORMAT)
        if isinstance(check_date_to, (datetime.date, datetime.datetime)):
            check_date_to = check_date_to.strftime(self.DATE_TIME_FORMAT)

        return self._post(
            '/attendance/listRecord',
            {
                "userIds": user_ids,
                "checkDateFrom": check_date_from,
                "checkDateTo": check_date_to
            },
            result_processor=lambda x: x['recordresult']
        )

    def list(self, work_date_from, work_date_to, user_ids=(), offset=0, limit=50):
        """
        考勤打卡数据开放

        :param work_date_from: 查询考勤打卡记录的起始工作日
        :param work_date_to: 查询考勤打卡记录的结束工作日
        :param user_ids: 员工在企业内的UserID列表，企业用来唯一标识用户的字段
        :param offset: 表示获取考勤数据的起始点，第一次传0，如果还有多余数据，下次获取传的offset值为之前的offset+limit
        :param limit: 表示获取考勤数据的条数，最大不能超过50条
        :return:
        """
        if isinstance(work_date_from, (datetime.date, datetime.datetime)):
            work_date_from = work_date_from.strftime(self.DATE_TIME_FORMAT)
        if isinstance(work_date_to, (datetime.date, datetime.datetime)):
            work_date_to = work_date_to.strftime(self.DATE_TIME_FORMAT)

        return self._post(
            '/attendance/listRecord',
            {
                "workDateFrom": work_date_from,
                "workDateTo": work_date_to,
                "userIdList": user_ids,
                "offset": offset,
                "limit": limit
            }
        )

    def listschedule(self, work_date, offset=0, size=200):
        """
        考勤排班信息按天全量查询接

        :param work_date: 排班时间
        :param offset: 偏移位置
        :param size: 分页大小，最大200
        :return:
        """
        if isinstance(work_date, (datetime.date, datetime.datetime)):
            work_date = work_date.strftime(self.DATE_TIME_FORMAT)
        return self._top_request(
            'dingtalk.smartwork.attends.getsimplegroups',
            {
                "work_date": work_date,
                "offset": offset,
                "size": size
            },
            result_processor=lambda x: x['result']
        )

    def getsimplegroups(self, offset=0, size=10):
        """
        获取考勤组列表详情

        :param offset: 偏移位置
        :param size: 分页大小，最大10
        :return:
        """
        return self._top_request(
            'dingtalk.smartwork.attends.getsimplegroups',
            {
                "offset": offset,
                "size": size
            },
            result_processor=lambda x: x['result']
        )

    def getleaveapproveduration(self, userid, from_date, to_date):
        """
        计算请假时长

        :param userid: 员工在企业内的UserID，企业用来唯一标识用户的字段。
        :param from_date: 请假开始时间
        :param to_date: 请假结束时间
        :return: 请假时长（单位分钟）
        """
        if isinstance(from_date, (datetime.date, datetime.datetime)):
            from_date = from_date.strftime(self.DATE_TIME_FORMAT)
        if isinstance(to_date, (datetime.date, datetime.datetime)):
            to_date = to_date.strftime(self.DATE_TIME_FORMAT)

        return self._top_request(
            'dingtalk.smartwork.attends.getleaveapproveduration',
            {
                "userid": userid,
                "from_date": from_date,
                "to_date": to_date
            },
            result_processor=lambda x: x['result']['duration_in_minutes']
        )

    def getusergroup(self, userid):
        """
        获取用户考勤组

        :param userid: 员工在企业内的UserID，企业用来唯一标识用户的字段。
        :return:
        """
        return self._top_request(
            'dingtalk.smartwork.attends.getusergroup',
            {"userid": userid},
            result_processor=lambda x: x['result']
        )
