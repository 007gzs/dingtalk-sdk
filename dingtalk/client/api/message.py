# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from optionaldict import optionaldict

from dingtalk.core.utils import to_text
from six.moves.urllib.parse import urlencode

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.model.message import BodyBase


class Message(DingTalkBaseAPI):

    @staticmethod
    def get_pc_url(url, pc_slide=True):
        """
        消息链接能在PC端打开

        :param url: 要打开的链接
        :param pc_slide: 如果为true代表在PC客户端打开，为false或者不写代表用浏览器打开
        :return:
        """
        params = {'url': url}
        if pc_slide:
            params['pc_slide'] = 'true'
        return "dingtalk://dingtalkclient/page/link?%s" % urlencode(params)

    def media_upload(self, media_type, media_file):
        """
        上传媒体文件

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、普通文件(file)
        :param media_file: 要上传的文件，一个 File-object
        :return:
        """
        return self._post(
            '/media/upload',
            params={'type': media_type},
            files={'media': media_file}
        )

    def media_download_file(self, media_id):
        """
        获取媒体文件

        :param media_id: 媒体文件的唯一标示
        :return: requests 的 Response 实例
        """
        return self._get(
            '/media/downloadFile',
            {'media_id': media_id}
        )

    def send_to_conversation(self, sender, cid, msg_body):
        """
        发送普通消息

        :param sender: 消息发送者员工ID
        :param cid: 群消息或者个人聊天会话Id
        :param msg_body: BodyBase 消息体
        :return:
        """
        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        msg_body['sender'] = sender
        msg_body['cid'] = cid
        return self._post('/message/send_to_conversation', msg_body)

    def send(self, agentid, msg_body, touser_list=(), toparty_list=()):
        """
        发送企业通知消息

        :param agentid: 企业应用id，这个值代表以哪个应用的名义发送消息
        :param msg_body: BodyBase 消息体
        :param touser_list: 员工id列表
        :param toparty_list: 部门id列表
        :return:
        """

        touser = "|".join(map(to_text, touser_list))
        toparty = "|".join(map(to_text, toparty_list))
        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        msg_body['touser'] = touser
        msg_body['toparty'] = toparty
        msg_body['agentid'] = agentid
        return self._post('/message/send', msg_body)

    def list_message_status(self, message_id):
        """
        获取企业通知消息已读未读状态

        :param message_id: 消息id
        :return:
        """
        return self._post('/message/list_message_status', {"messageId": message_id})

    def send_by_code(self, code, msg_body):
        """
        企业通知消息接口（用户反馈式）

        :param code: 用户操作产生的授权码
        :param msg_body: BodyBase 消息体
        :return:
        """
        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        msg_body['code'] = code
        return self._post('/message/sendByCode', msg_body)

    def asyncsend(self, msg_body, agent_id, userid_list=(), dept_id_list=(), to_all_user=False):
        """
        企业会话消息异步发送

        :param msg_body: BodyBase 消息体
        :param agent_id: 微应用的id
        :param userid_list: 接收者的用户userid列表
        :param dept_id_list: 接收者的部门id列表
        :param to_all_user: 是否发送给企业全部用户
        :return: 任务id
        """
        userid_list = ",".join(map(to_text, userid_list))
        dept_id_list = ",".join(map(to_text, dept_id_list))

        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        msgtype = msg_body['msgtype']
        msgcontent = json.dumps(msg_body[msgtype])
        return self._top_request(
            'dingtalk.corp.message.corpconversation.asyncsend',
            {
                'msgtype': msgtype,
                'agent_id': agent_id,
                'msgcontent': msgcontent,
                'userid_list': userid_list,
                'dept_id_list': dept_id_list,
                'to_all_user': to_all_user
            },
            result_processor=lambda x: x['task_id']
        )

    def asyncsend_v2(self, msg_body, agent_id, userid_list=(), dept_id_list=(), to_all_user=False):
        """
        企业会话消息异步发送

        :param msg_body: BodyBase 消息体
        :param agent_id: 微应用的id
        :param userid_list: 接收者的用户userid列表
        :param dept_id_list: 接收者的部门id列表
        :param to_all_user: 是否发送给企业全部用户
        :return: 任务id
        """
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ",".join(map(to_text, userid_list))
        if isinstance(dept_id_list, (list, tuple, set)):
            dept_id_list = ",".join(map(to_text, dept_id_list))
        if not userid_list:
            userid_list = None
        if not dept_id_list:
            dept_id_list = None
        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        return self._top_request(
            'dingtalk.oapi.message.corpconversation.asyncsend_v2',
            optionaldict({
                "msg": msg_body,
                'agent_id': agent_id,
                'userid_list': userid_list,
                'dept_id_list': dept_id_list,
                'to_all_user': 'true' if to_all_user else 'false'
            }),
            result_processor=lambda x: x['task_id']
        )

    def recall(self, agent_id, msg_task_id):
        """
        撤回工作通知消息

        :param agent_id: 发送工作通知的微应用agentId
        :param msg_task_id: 发送工作通知返回的taskId
        """
        return self._top_request(
            "dingtalk.oapi.message.corpconversation.recall",
            {"agent_id": agent_id, "msg_task_id": msg_task_id}
        )

    def getsendprogress(self, agent_id, task_id):
        """
        获取异步发送企业会话消息的发送进度

        :param agent_id: 发送消息时使用的微应用的id
        :param task_id: 发送消息时钉钉返回的任务id
        :return:
        """
        return self._top_request(
            'dingtalk.corp.message.corpconversation.getsendprogress',
            {'agent_id': agent_id, 'task_id': task_id},
            result_processor=lambda x: x['progress']
        )

    def getsendresult(self, agent_id=None, task_id=None):
        """
        获取异步向企业会话发送消息的结果

        :param agent_id: 微应用的agentid
        :param task_id: 异步任务的id
        :return:
        """
        return self._top_request(
            'dingtalk.corp.message.corpconversation.getsendresult',
            {'agent_id': agent_id, 'task_id': task_id},
            result_processor=lambda x: x['send_result']
        )

    def asyncsendbycode(self, code, msg_body, agent_id, userid_list=(), dept_id_list=(), to_all_user=False):
        """
        通过用户授权码异步向企业会话发送消息

        :param code: 用户操作产生的授权码
        :param msg_body: BodyBase 消息体
        :param agent_id: 微应用的id
        :param userid_list: 接收者的用户userid列表
        :param dept_id_list: 接收者的部门id列表
        :param to_all_user: 是否发送给企业全部用户
        :return: 任务id
        """
        userid_list = ",".join(map(to_text, userid_list))
        dept_id_list = ",".join(map(to_text, dept_id_list))

        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        msgtype = msg_body['msgtype']
        msgcontent = json.dumps(msg_body[msgtype])

        return self._top_request(
            'dingtalk.corp.message.corpconversation.asyncsendbycode',
            {
                'msgtype': msgtype,
                'code': code,
                'agent_id': agent_id,
                'msgcontent': msgcontent,
                'userid_list': userid_list,
                'dept_id_list': dept_id_list,
                'to_all_user': to_all_user
            },
            result_processor=lambda x: x['task_id']
        )
