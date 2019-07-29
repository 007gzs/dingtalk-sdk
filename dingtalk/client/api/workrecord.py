# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import datetime
import time

from optionaldict import optionaldict

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.model.field import FieldBase


class WorkRecord(DingTalkBaseAPI):

    def add(self, userid, create_time, title, url, form_item_dict, originator_user_id='', source_name=''):
        """
        新增待办事项

        :param userid: 用户id
        :param create_time: 待办时间。Unix时间戳
        :param title: 标题
        :param url: 待办跳转url
        :param form_item_dict: 表单列表 OrderedDict((('标题1', '内容1'),('标题2', '内容2')))
        :param originator_user_id: manager7078
        :param source_name: 待办来源名称
        """

        if isinstance(create_time, (datetime.date, datetime.datetime)):
            create_time = int(time.mktime(create_time.timetuple()) * 1000)
        form_item_list = [{'title': k, 'content': v}for k, v in form_item_dict.items()]
        return self._top_request(
            "dingtalk.oapi.workrecord.add",
            {
                "userid": userid,
                "create_time": create_time,
                "title": title,
                "url": url,
                "formItemList": form_item_list,
                "originator_user_id": originator_user_id,
                "source_name": source_name
            },
            result_processor=lambda x: x['record_id']
        )

    def update(self, userid, record_id):
        """
        更新待办事项状态

        :param userid: 用户id
        :param record_id: 待办事项唯一id
        """
        return self._top_request(
            "dingtalk.oapi.workrecord.update",
            {"userid": userid, "record_id": record_id}
        )

    def getbyuserid(self, userid, status, offset=0, limit=50):
        """
        获取用户的待办事项

        :param userid: 用户唯一ID
        :param offset: 分页游标，从0开始，如返回结果中has_more为true，则表示还有数据，offset再传上一次的offset+limit
        :param limit: 分页大小，最多50
        :param status: 待办事项状态，0表示未完成，1表示完成
        """
        return self._top_request(
            "dingtalk.oapi.workrecord.getbyuserid",
            {
                "userid": userid,
                "offset": offset,
                "limit": limit,
                "status": status
            },
            result_processor=lambda x: x['records']
        )

    def process_save(self, name, description, form_component_list=(), process_code=None, agentid=None):
        """
        保存审批模板

        :param name: 模板名称
        :param description: 模板描述
        :param form_component_list: 表单列表
        :param process_code: 模板的唯一码
        :param agentid: 企业微应用标识
        """
        form_component_list = [form.get_dict() if isinstance(form, FieldBase) else form for form in form_component_list]

        return self._top_request(
            "dingtalk.oapi.process.save",
            {
                "saveProcessRequest": optionaldict({
                    "agentid": agentid,
                    "process_code": process_code,
                    "name": name,
                    "description": description,
                    "fake_mode": True,
                    "form_component_list": form_component_list
                })
            },
            result_processor=lambda x: x['process_code']
        )

    def process_delete(self, process_code, agentid=''):
        """
        删除创建的审批模板

        :param process_code: 模板的唯一码
        :param agentid: 微应用agentId，ISV必填
        """
        return self._top_request(
            "dingtalk.oapi.process.delete",
            {
                "request": {
                    "process_code": process_code,
                    "agentid": agentid
                }
            }
        )

    def process_workrecord_create(
            self,
            process_code,
            originator_user_id,
            form_component_values,
            url,
            agentid='',
            title=''
    ):
        """
        发起不带流程的审批实例

        :param process_code: 审批模板唯一码
        :param originator_user_id: 审批发起人
        :param form_component_values: 表单参数列表
        :param url: 实例跳转链接
        :param agentid: 应用id
        :param title: 实例标题
        """
        if isinstance(form_component_values, dict):
            form_component_values = [{"name": name, "value": value} for name, value in form_component_values.items()]
        return self._top_request(
            "dingtalk.oapi.process.workrecord.create",
            {
                "request": {
                    "process_code": process_code,
                    "originator_user_id": originator_user_id,
                    "form_component_values": form_component_values,
                    "url": url,
                    "agentid": agentid,
                    "title": title
                }
            },
            result_processor=lambda x: x['process_instance_id']
        )

    def process_workrecord_update(
            self,
            process_instance_id,
            status,
            result,
            agentid=''
    ):
        """
        同步待办实例状态

        :param process_instance_id: 实例id
        :param status: 实例状态，分为COMPLETED, TERMINATED
        :param result: 实例结果, 如果实例状态是COMPLETED，需要设置result，分为agree和refuse
        :param agentid: 应用id
        """
        return self._top_request(
            "dingtalk.oapi.process.workrecord.update",
            {
                "request": {
                    "process_instance_id": process_instance_id,
                    "status": status,
                    "result": result,
                    "agentid": agentid
                }
            }
        )

    def process_workrecord_task_create(
            self,
            process_instance_id,
            tasks,
            agentid='',
            activity_id=''
    ):
        """
        创建待办任务

        :param process_instance_id: 实例id
        :param tasks: 任务列表
        :param agentid: 应用id
        :param activity_id: 节点id
        """
        return self._top_request(
            "dingtalk.oapi.process.workrecord.task.create",
            {
                "request": {
                    "process_instance_id": process_instance_id,
                    "tasks": tasks,
                    "agentid": agentid,
                    "activity_id": activity_id
                }
            },
            result_processor=lambda x: x['tasks']
        )

    def dingtalk_oapi_process_workrecord_task_update(
            self,
            process_instance_id,
            tasks,
            agentid=''
    ):
        """
        更新待办任务状态

        :param process_instance_id: 实例id
        :param tasks: 任务列表
        :param agentid: 应用id
        """
        return self._top_request(
            "dingtalk.oapi.process.workrecord.task.update",
            {
                "request": {
                    "process_instance_id": process_instance_id,
                    "tasks": tasks,
                    "agentid": agentid
                }
            },
            result_processor=lambda x: x['tasks']
        )

    def process_workrecord_taskgroup_cancel(
            self,
            process_instance_id,
            activity_id,
            agentid=''
    ):
        """
        批量取消任务

        :param process_instance_id: 实例id
        :param activity_id: 任务组id
        :param agentid: 应用id
        """
        return self._top_request(
            "dingtalk.oapi.process.workrecord.taskgroup.cancel",
            {
                "request": {
                    "process_instance_id": process_instance_id,
                    "activity_id": activity_id,
                    "agentid": agentid
                }
            }
        )
