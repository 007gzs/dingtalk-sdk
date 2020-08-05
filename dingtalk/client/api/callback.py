# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class Callback(DingTalkBaseAPI):
    ALL_CALL_BACK_TAGS = (
        'user_add_org', 'user_modify_org', 'user_leave_org', 'user_active_org',
        'org_admin_add', 'org_admin_remove', 'org_dept_create', 'org_dept_modify',
        'org_dept_remove', 'org_change', 'org_remove',
        'label_user_change', 'label_conf_add', 'label_conf_modify', 'label_conf_del',
        'edu_user_insert', 'edu_user_update', 'edu_user_delete',
        'edu_user_relation_insert', 'edu_user_relation_update', 'edu_user_relation_delete',
        'edu_dept_insert', 'edu_dept_update', 'edu_dept_delete',
        'chat_add_member', 'chat_remove_member', 'chat_quit', 'chat_update_owner', 'chat_update_title', 'chat_disband',
        'check_in', 'bpms_task_change', 'bpms_instance_change',
        'attendance_check_record', 'attendance_schedule_change', 'attendance_overtime_duration',
        'meetingroom_book', 'meetingroom_room_info'
    )

    def register_call_back(self, call_back_tags, token, aes_key, url):
        """
        注册事件回调接口

        :param call_back_tags: 需要监听的事件类型
        :param token: 加解密需要用到的token
        :param aes_key: 数据加密密钥
        :param url: 接收事件回调的url
        :return:
        """
        call_back_tag = []
        for k in call_back_tags:
            if k in self.ALL_CALL_BACK_TAGS:
                call_back_tag.append(k)
        return self._post(
            '/call_back/register_call_back',
            {
                "call_back_tag": call_back_tag,
                "token": token,
                "aes_key": aes_key,
                "url": url
            }
        )

    def get_call_back(self):
        """
        查询事件回调接口

        :return:
        """
        return self._get('/call_back/get_call_back')

    def update_call_back(self, call_back_tags, token, aes_key, url):
        """
        更新事件回调接口

        :param call_back_tags: 需要监听的事件类型
        :param token: 加解密需要用到的token
        :param aes_key: 数据加密密钥
        :param url: 接收事件回调的url
        :return:
        """
        call_back_tag = []
        for k in call_back_tags:
            if k in self.ALL_CALL_BACK_TAGS:
                call_back_tag.append(k)
        return self._post(
            '/call_back/update_call_back',
            {
                "call_back_tag": call_back_tag,
                "token": token,
                "aes_key": aes_key,
                "url": url
            }
        )

    def delete_call_back(self):
        """
        删除事件回调接口

        :return:
        """
        return self._get('/call_back/delete_call_back')

    def get_call_back_failed_result(self):
        """
        获取回调失败的结果

        :return:
        """
        return self._get('/call_back/get_call_back_failed_result')
