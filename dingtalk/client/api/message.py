# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import copy
import json

import six

from dingtalk.client.api.base import DingTalkBaseAPI


class Message(DingTalkBaseAPI):
    def media_upload(self, media_type, media_file):
        """
        上传媒体文件
        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、普通文件(file)
        :param media_file: 要上传的文件，一个 File-object
        :return:
        """
        return self._post('/media/upload', params={'type': media_type}, files={'media': media_file})

    def media_download_file(self, media_id):
        """
        获取媒体文件
        :param media_id: 媒体文件的唯一标示
        :return: requests 的 Response 实例
        """
        return self._get('/media/downloadFile', {'media_id': media_id})

    def send_to_conversation(self, msg_body):
        """
        发送普通消息
        :param msg_body: 消息体
        :return:
        """
        return self._get('/message/send_to_conversation', msg_body)

    def send(self, msg_body):
        """
        发送企业通知消息
        :param msg_body:
        :return: 消息体
        """
        return self._post('/message/send', msg_body)

    def list_message_status(self, message_id):
        """
        获取企业通知消息已读未读状态
        :param message_id: 消息id
        :return:
        """
        return self._get('/message/list_message_status', {"messageId": message_id})

    def send_by_code(self, msg_body):
        """
        企业通知消息接口（用户反馈式）
        :param msg_body: 消息体
        :return:
        """
        return self._get('/message/sendByCode', msg_body)

    def asyncsend(self, msgtype, agent_id, msgcontent, userid_list=(), dept_id_list=(), to_all_user=False):
        """
        企业会话消息异步发送
        :param msgtype: 消息类型,如text、file、oa等，具体见文档
        :param agent_id: 微应用的id
        :param msgcontent: 与msgtype对应的消息体
        :param userid_list: 接收者的用户userid列表
        :param dept_id_list: 接收者的部门id列表
        :param to_all_user: 是否发送给企业全部用户
        :return:
        """
        userid_list = "|".join(userid_list)
        dept_id_list = "|".join(dept_id_list)
        if not isinstance(msgcontent, six.string_types):
            msgcontent = json.dumps(msgcontent)
        return self._top_request('dingtalk.corp.message.corpconversation.asyncsend',
                                 msgtype=msgtype, agent_id=agent_id, msgcontent=msgcontent,
                                 userid_list=userid_list, dept_id_list=dept_id_list, to_all_user=to_all_user)

    def getsendprogress(self, agent_id, task_id):
        """
        获取异步发送企业会话消息的发送进度
        :param agent_id: 发送消息时使用的微应用的id
        :param task_id: 发送消息时钉钉返回的任务id
        :return:
        """
        return self._top_request('dingtalk.corp.message.corpconversation.getsendprogress',
                                 agent_id=agent_id, task_id=task_id)

    def getsendresult(self, agent_id=None, task_id=None):
        """
        获取异步向企业会话发送消息的结果
        :param agent_id: 微应用的agentid
        :param task_id: 异步任务的id
        :return:
        """
        return self._top_request('dingtalk.corp.message.corpconversation.getsendresult',
                                 agent_id=agent_id, task_id=task_id)

    def asyncsendbycode(self, code, msgtype, agent_id, msgcontent, userid_list=(), dept_id_list=(), to_all_user=False):
        """
        通过用户授权码异步向企业会话发送消息
        :param code: 用户操作产生的授权码
        :param msgtype: 消息类型,如text、file、oa等，具体见文档
        :param agent_id: 微应用的id
        :param msgcontent: 与msgtype对应的消息体
        :param userid_list: 接收者的用户userid列表
        :param dept_id_list: 接收者的部门id列表
        :param to_all_user: 是否发送给企业全部用户
        :return:
        """
        userid_list = "|".join(userid_list)
        dept_id_list = "|".join(dept_id_list)
        if not isinstance(msgcontent, six.string_types):
            msgcontent = json.dumps(msgcontent)
        return self._top_request('dingtalk.corp.message.corpconversation.asyncsendbycode',
                                 msgtype=msgtype, agent_id=agent_id, msgcontent=msgcontent, code=code,
                                 userid_list=userid_list, dept_id_list=dept_id_list, to_all_user=to_all_user)
