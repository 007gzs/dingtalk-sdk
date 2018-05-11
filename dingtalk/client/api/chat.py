# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.model.message import BodyBase


class Chat(DingTalkBaseAPI):

    def create(self, name, owner, useridlist, show_history_type=False):
        """
        创建会话

        :param name: 群名称。长度限制为1~20个字符
        :param owner: 群主userId，员工唯一标识ID；必须为该会话useridlist的成员之一
        :param useridlist: 群成员列表，每次最多支持40人，群人数上限为1000
        :param show_history_type: 新成员是否可查看聊天历史消息（新成员入群是否可查看最近100条聊天记录）
        :return: 群会话的id
        """
        return self._post(
            '/chat/create',
            {
                'name': name,
                'owner': owner,
                'useridlist': useridlist,
                'showHistoryType': 1 if show_history_type else 0
            },
            result_processor=lambda x: x['chatid']
        )

    def update(self, chatid, name=None, owner=None, add_useridlist=(), del_useridlist=()):
        """
        修改会话

        :param chatid: 群会话的id
        :param name: 群名称。长度限制为1~20个字符，不传则不修改
        :param owner: 群主userId，员工唯一标识ID；必须为该会话成员之一；不传则不修改
        :param add_useridlist: 添加成员列表，每次最多支持40人，群人数上限为1000
        :param del_useridlist: 删除成员列表，每次最多支持40人，群人数上限为1000
        :return:
        """
        return self._post(
            '/chat/update',
            {
                'chatid': chatid,
                'name': name,
                'owner': owner,
                'add_useridlist': add_useridlist,
                'del_useridlist': del_useridlist
            }
        )

    def get(self, chatid):
        """
        获取会话

        :param chatid: 群会话的id
        :return: 群会话信息
        """
        return self._post(
            '/chat/get',
            {'chatid': chatid},
            result_processor=lambda x: x['chat_info']
        )

    def send(self, chatid, msg_body):
        """
        发送群消息

        :param chatid: 群会话的id
        :param msg_body: BodyBase 消息体
        :return: 加密的消息id
        """
        if isinstance(msg_body, BodyBase):
            msg_body = msg_body.get_dict()
        msg_body['chatid'] = chatid
        return self._post(
            '/chat/send',
            msg_body,
            result_processor=lambda x: x['messageId']
        )

    def get_read_list(self, message_id, cursor=0, size=100):
        """
        查询群消息已读人员列表

        :param message_id: 发送群消息接口返回的加密消息id
        :param cursor: 分页查询的游标，第一次传0，后续传返回结果中的next_cursor。返回结果中没有next_cursor时，表示没有后续的数据了
        :param size: 分页查询的大小，最大可以传100
        :return:
        """
        return self._post(
            '/chat/getReadList',
            {"messageId": message_id, "cursor": cursor, "size": size}
        )
