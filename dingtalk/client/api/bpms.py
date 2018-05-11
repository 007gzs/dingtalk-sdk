# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
import datetime
import json

import six

from dingtalk.core.utils import to_text

from dingtalk.client.api.base import DingTalkBaseAPI


class Bpms(DingTalkBaseAPI):

    def process_copy(self, agent_id, process_code, biz_category_id=None, process_name=None, description=None):
        """
        复制审批流

        :param agent_id: 企业微应用标识
        :param process_code: 审批流的唯一码
        :param biz_category_id: 业务分类标识
        :param process_name: 审批流名称
        :param description: 审批流描述
        :return:
        """

        return self._top_request(
            'dingtalk.smartwork.bpms.process.copy',
            {
                'agent_id': agent_id,
                'process_code': process_code,
                'biz_category_id': biz_category_id,
                'process_name': process_name,
                'description': description
            },
            result_processor=lambda x: x['result']
        )

    def process_sync(self, agent_id, src_process_code, target_process_code, biz_category_id=None, process_name=None):
        """
        更新审批流

        :param agent_id: 企业微应用标识
        :param src_process_code: 源审批流的唯一码
        :param target_process_code: 目标审批流的唯一码
        :param biz_category_id: 业务分类标识
        :param process_name: 审批流名称
        :return:
        """

        return self._top_request(
            'dingtalk.smartwork.bpms.process.sync',
            {
                'agent_id': agent_id,
                'src_process_code': src_process_code,
                'target_process_code': target_process_code,
                'biz_category_id': biz_category_id,
                'process_name': process_name
            }
        )

    def processinstance_create(self, process_code, originator_user_id, dept_id, approvers, form_component_values,
                               agent_id=None, cc_list=(), cc_start=False, cc_finish=False):
        """
        发起审批实例

        :param process_code: 审批流的唯一码
        :param originator_user_id: 审批实例发起人的userid
        :param dept_id: 发起人所在的部门
        :param approvers: 审批人userid列表
        :param form_component_values: 审批流表单参数 name: 表单每一栏的名称 value: 表单每一栏的值, ext_value: 扩展值
                                      例：OrderedDict({name1: value1, name2: (value2, ext_value2), name3: (value3, )})
        :param agent_id:
        :param cc_list: 抄送人userid列表
        :param cc_start: 开始时抄送
        :param cc_finish: 结束时抄送
        :return:
        """
        cc_position = 'START' if cc_start else ''
        if cc_finish:
            if cc_position:
                cc_position += '_'
            cc_position += 'FINISH'
        if isinstance(approvers, (list, tuple, set)):
            approvers = ','.join(map(to_text, approvers))
        form_component_value_list = []
        for name, value in form_component_values.item():
            data = {'name': name}
            if isinstance(value, (list, tuple)):
                if len(value) > 1:
                    data['ext_value'] = value[1]
                value = value[0]
            data['value'] = value
            form_component_value_list.append(data)

        return self._top_request(
            'dingtalk.smartwork.bpms.processinstance.create',
            {
                'process_code': process_code,
                'originator_user_id': originator_user_id,
                'dept_id': dept_id,
                'approvers': approvers,
                'agent_id': agent_id,
                'cc_list': cc_list,
                'cc_position': cc_position,
                'form_component_values': json.dumps(form_component_value_list)
            },
            result_processor=lambda x: x['process_instance_id']
        )

    def processinstance_list(self, process_code, start_time, end_time=None, cursor=0, size=10, userid_list=()):
        """
        获取审批实例列表

        :param process_code: 流程模板唯一标识，可在oa后台编辑审批表单部分查询
        :param start_time: 	审批实例开始时间
        :param end_time: 审批实例结束时间，默认取当前值
        :param cursor: 每页大小，最多传10
        :param size: 分页查询的游标，最开始传0，后续传返回参数中的next_cursor值
        :param userid_list: 发起人用户id列表
        :return:
        """
        userid_list = ','.join(map(to_text, userid_list))

        if isinstance(start_time, datetime.date):
            start_time = int(time.mktime(start_time.timetuple()) * 1000)

        if isinstance(end_time, datetime.date):
            end_time = int(time.mktime(end_time.timetuple()) * 1000)

        assert isinstance(start_time, six.integer_types)
        assert end_time is None or isinstance(end_time, six.integer_types)

        return self._top_request(
            'dingtalk.smartwork.bpms.processinstance.list',
            {
                'process_code': process_code,
                'start_time': start_time,
                'end_time': end_time,
                'cursor': cursor,
                'size': size,
                'userid_list': userid_list
            },
            result_processor=lambda x: x['result']
        )

    def processinstance_get(self, process_instance_id):
        """
        获取单个审批实例详情

        :param process_instance_id: 审批实例id
        :return:
        """
        return self._top_request(
            'dingtalk.smartwork.bpms.processinstance.get',
            {'process_instance_id': process_instance_id},
            result_processor=lambda x: x['process_instance']
        )

    def process_listbyuserid(self, userid, offset=0, size=100):
        """
        根据用户id获取可见审批模板列表

        :param userid: 用户id
        :param offset: 分页游标，从0开始。根据返回结果中next_cursor是否为空判断是否有下一页，且再次调用offset设置成next_cursor的值
        :param size: 分页大小，最大可设置成100
        :return:
        """
        return self._top_request(
            'dingtalk.oapi.process.listbyuserid',
            {
                'userid': userid,
                'offset': offset,
                'size': size
            }
        )
