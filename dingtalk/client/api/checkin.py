# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
import datetime

import six
from dingtalk.core.utils import to_text

from dingtalk.client.api.base import DingTalkBaseAPI


class Checkin(DingTalkBaseAPI):

    def record(self, department_id, start_time, end_time, offset=0, size=100, order_asc=True):
        """
        获得签到数据

        :param department_id: 部门id（1 表示根部门）
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param offset: 偏移量
        :param size: 分页大小
        :param order_asc: 是否正序排列
        :return:
        """

        if isinstance(start_time, (datetime.date, datetime.datetime)):
            start_time = int(time.mktime(start_time.timetuple()) * 1000)

        if isinstance(end_time, (datetime.date, datetime.datetime)):
            end_time = int(time.mktime(end_time.timetuple()) * 1000)

        assert isinstance(start_time, six.integer_types) and isinstance(end_time, six.integer_types)
        return self._get(
            '/checkin/record',
            {
                'department_id': department_id,
                'start_time': start_time,
                'end_time': end_time,
                'offset': offset,
                'size': size,
                'order_asc': 'asc' if order_asc else 'desc'
            },
            result_processor=lambda x: x['data']
        )

    def record_get(self, userid_list, start_time, end_time, offset=0, size=100):
        """
        获取多个用户的签到记录 (如果是取1个人的数据，时间范围最大到10天，如果是取多个人的数据，时间范围最大1天。)

        :param userid_list: 需要查询的用户列表
        :param start_time: 起始时间
        :param end_time: 截止时间
        :param offset: 偏移量
        :param size: 分页大小
        :return:
        """
        if isinstance(start_time, (datetime.date, datetime.datetime)):
            start_time = int(time.mktime(start_time.timetuple()) * 1000)

        if isinstance(end_time, (datetime.date, datetime.datetime)):
            end_time = int(time.mktime(end_time.timetuple()) * 1000)

        assert isinstance(start_time, six.integer_types) and isinstance(end_time, six.integer_types)
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))

        return self._top_request(
            'dingtalk.smartwork.checkin.record.get',
            {
                'userid_list': userid_list,
                'start_time': start_time,
                'end_time': end_time,
                'offset': offset,
                'size': size
            }
        )
