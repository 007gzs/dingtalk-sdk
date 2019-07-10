# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import json

from optionaldict import optionaldict

from dingtalk.core.utils import to_text
from dingtalk.client.api.base import DingTalkBaseAPI


class Employeerm(DingTalkBaseAPI):

    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

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

    def list(self, userid_list, field_filter_list=()):
        """
        批量获取员工花名册字段信息
        智能人事业务，企业/ISV根据员工id批量访问员工花名册信息

        :param userid_list: 员工id列表
        :param field_filter_list: 需要获取的花名册字段信息
        """
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))
        if isinstance(field_filter_list, (list, tuple, set)):
            field_filter_list = ','.join(map(to_text, field_filter_list))
        return self._top_request(
            "dingtalk.oapi.smartwork.hrm.employee.list",
            {
                "userid_list": userid_list,
                "field_filter_list": field_filter_list
            }
        )

    def querypreentry(self, offset=0, size=50):
        """
        智能人事查询公司待入职员工列表
        智能人事业务，企业/ISV分页查询公司待入职员工id列表

        :param offset: 分页起始值，默认0开始
        :param size: 分页大小，最大50
        """
        return self._top_request(
            "dingtalk.oapi.smartwork.hrm.employee.querypreentry",
            {
                "offset": offset,
                "size": size
            }
        )

    def queryonjob(self, status_list=(), offset=0, size=50):
        """
        智能人事查询公司在职员工列表
        智能人事业务，提供企业/ISV按在职状态分页查询公司在职员工id列表

        :param status_list: 在职员工子状态筛选。2，试用期；3，正式；5，待离职；-1，无状态
        :param offset: 分页起始值，默认0开始
        :param size: 分页大小，最大50
        """
        if isinstance(status_list, (list, tuple, set)):
            status_list = ','.join(map(to_text, status_list))
        return self._top_request(
            "dingtalk.oapi.smartwork.hrm.employee.queryonjob",
            {
                "status_list": status_list,
                "offset": offset,
                "size": size
            }
        )

    def querydimission(self, offset=0, size=50):
        """
        智能人事查询公司离职员工列表
        智能人事业务，提供企业/ISV分页查询公司离职员工id列表

        :param offset: 分页游标，从0开始。根据返回结果里的next_cursor是否为空来判断是否还有下一页，且再次调用时offset设置成next_cursor的值
        :param size: 分页大小，最大50
        """
        return self._top_request(
            "dingtalk.oapi.smartwork.hrm.employee.querydimission",
            {
                "offset": offset,
                "size": size
            }
        )

    def listdimission(self, userid_list=()):
        """
        批量获取员工离职信息
        根据传入的staffId列表，批量查询员工的离职信息

        :param userid_list: 员工id
        """
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))
        return self._top_request(
            "dingtalk.oapi.smartwork.hrm.employee.listdimission",
            {
                "userid_list": userid_list
            }
        )

    def addpreentry(self, name, mobile, pre_entry_time=None, op_userid=None, extend_info=None):
        """
        智能人事添加企业待入职员工

        :param name: 员工姓名
        :param mobile: 手机号
        :param pre_entry_time: 预期入职时间
        :param op_userid: 操作人userid
        :param extend_info: 扩展信息
        :return:
        """
        if isinstance(pre_entry_time, (datetime.date, datetime.datetime)):
            pre_entry_time = pre_entry_time.strftime(self.DATE_TIME_FORMAT)
        if isinstance(extend_info, dict):
            extend_info = json.dumps(extend_info)

        return self._top_request(
            "dingtalk.oapi.smartwork.hrm.employee.addpreentry",
            {
                "param": optionaldict({
                    "name": name,
                    "mobile": mobile,
                    "pre_entry_time": pre_entry_time,
                    "op_userid": op_userid,
                    "extend_info": extend_info
                })
            }
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
