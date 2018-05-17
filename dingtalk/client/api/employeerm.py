# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime

from dingtalk.client.api.base import DingTalkBaseAPI


class Employeerm(DingTalkBaseAPI):

    def get(self, userid):
        """
        获取智能人事员工花名册详细数据

        :param userid: 查询用户userid
        :return:
        """
        return self._top_request(
            'dingtalk.corp.hrm.employee.get',
            {'userid': userid},
            result_processor=lambda x: x['group_list']
        )

    def getdismissionlist(self, op_userid, current=1, page_size=100):
        """
        获取离职人员信息

        :param op_userid: 操作人userid
        :param current: 第几页，从1开始
        :param page_size: 一页多少数据，在1-100之间
        :return:
        """
        return self._top_request(
            'dingtalk.corp.hrm.employee.getdismissionlist',
            {'op_userid': op_userid, 'current': current, 'page_size': page_size},
            result_processor=lambda x: x['page']
        )

    def setuserworkdata(self, op_userid, userid, data_value, data_desc=None):
        """
        更新用户绩效数据

        :param op_userid: 操作人userid，必须是拥有被操作人操作权限的管理员userid
        :param userid: 被操作人userid
        :param data_value: 数据值,可以为数值或者字符串
        :param data_desc: 数据项描述信息
        :return:
        """
        hrm_api_user_data_model = {'userid': userid, 'data_value': data_value, 'data_desc': data_desc}
        return self._top_request(
            'dingtalk.corp.hrm.employee.getdismissionlist',
            {'op_userid': op_userid, 'hrm_api_user_data_model': hrm_api_user_data_model}
        )

    def modjobinfo(self, op_userid, userid, employee_type=None, employee_status=None, confirm_join_time=None,
                   probation_period_type=None, regular_time=None, join_working_time=None, birth_time=None):
        """
        更新员工工作信息

        :param op_userid: 操作人userid，必须是拥有被操作人操作权限的管理员userid
        :param userid: 被操作人userid
        :param employee_type: 员工类型（1:全职，2:兼职，3:实习，4:劳务派遣，5:退休返聘，6:劳务外包）
        :param employee_status: 员工状态（2:试用，3:正式）
        :param confirm_join_time: 入职日期
        :param probation_period_type: 试用期（1:无试用期，2:1个月，3:2个月，4:3个月，5:4个月，6:5个月，7:6个月，8:其他）
        :param regular_time: 转正时间
        :param join_working_time: 首次参加工作时间
        :param birth_time: 生日日期
        :return:
        """
        if confirm_join_time is not None and isinstance(confirm_join_time, (datetime.date, datetime.datetime)):
            confirm_join_time = confirm_join_time.strftime('%Y-%m-%d %H:%M:%S')
        if regular_time is not None and isinstance(regular_time, (datetime.date, datetime.datetime)):
            regular_time = regular_time.strftime('%Y-%m-%d %H:%M:%S')
        if join_working_time is not None and isinstance(join_working_time, (datetime.date, datetime.datetime)):
            join_working_time = join_working_time.strftime('%Y-%m-%d %H:%M:%S')
        if birth_time is not None and isinstance(birth_time, (datetime.date, datetime.datetime)):
            birth_time = birth_time.strftime('%Y-%m-%d %H:%M:%S')
        hrm_api_job_model = {
            'userid': userid,
            'employee_type': employee_type,
            'employee_status': employee_status,
            'confirm_join_time': confirm_join_time,
            'probation_period_type': probation_period_type,
            'regular_time': regular_time,
            'join_working_time': join_working_time,
            'birth_time': birth_time
        }
        return self._top_request(
            'dingtalk.corp.hrm.employee.modjobinfo',
            {'op_userid': op_userid, 'hrm_api_job_model': hrm_api_job_model}
        )
