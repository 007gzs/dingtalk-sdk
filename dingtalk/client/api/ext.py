# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from dingtalk.client.api.base import DingTalkBaseAPI
from dingtalk.core.utils import json_loads


class Ext(DingTalkBaseAPI):

    def listlabelgroups(self, offset=0, size=100):
        """
        标签列表

        :param offset: 偏移位置
        :param size: 分页大小,最大100
        :return:
        """
        return self._top_request(
            'dingtalk.corp.ext.listlabelgroups',
            {'offset': offset, 'size': size},
            result_processor=lambda x: json_loads(x) if isinstance(x, six.string_types) else x
        )

    def list(self, offset=0, size=100):
        """
        外部联系人列表

        :param offset: 偏移位置
        :param size: 分页大小,最大100
        :return:
        """
        return self._top_request(
            'dingtalk.corp.ext.list',
            {'offset': offset, 'size': size},
            result_processor=lambda x: json_loads(x) if isinstance(x, six.string_types) else x
        )

    def add(self, name, follower_userid, label_ids, mobile, state_code='86',
            title=None, share_deptids=(), remark=None, address=None, company_name=None, share_userids=()):
        """
        添加企业外部联系人

        :param name: 名称
        :param follower_userid: 负责人userId
        :param state_code: 手机号国家码
        :param mobile: 手机号
        :param label_ids: 标签列表
        :param title: 职位
        :param share_deptids: 共享给的部门ID
        :param remark: 备注
        :param address: 地址
        :param company_name: 企业名
        :param share_userids: 共享给的员工userId列表
        :return:
        """

        return self._top_request(
            'dingtalk.corp.ext.add',
            {
                'contact': {
                    'name': name,
                    'follower_user': follower_userid,
                    'state_code': state_code,
                    'mobile': mobile,
                    'label_ids': label_ids,
                    'title': title,
                    'share_deptids': share_deptids,
                    'remark': remark,
                    'address': address,
                    'company_name': company_name,
                    'share_userid': share_userids
                }
            },
            result_processor=lambda x: x['userid']
        )
