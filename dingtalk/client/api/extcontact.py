# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class ExtContact(DingTalkBaseAPI):

    def listlabelgroups(self, offset=0, size=100):
        """
        获取外部联系人标签列表

        :param size: 分页大小,最大100
        :param offset: 偏移位置
        """
        return self._top_request(
            "dingtalk.oapi.extcontact.listlabelgroups",
            {"size": size, "offset": offset}
        )

    def list(self, offset=0, size=100):
        """
        获取外部联系人列表

        :param size: 分页大小, 最大100
        :param offset: 偏移位置
        """
        return self._top_request(
            "dingtalk.oapi.extcontact.list",
            {"size": size, "offset": offset}
        )

    def get(self, user_id):
        """
        获取企业外部联系人详情

        :param user_id: userId
        """
        return self._top_request(
            "dingtalk.oapi.extcontact.get",
            {"user_id": user_id}
        )

    def create(self, name, follower_user_id, label_ids, mobile, state_code='86',
               title=None, share_dept_ids=(), remark=None, address=None, company_name=None, share_user_ids=()):
        """
        添加外部联系人

        :param name: 名称
        :param follower_user_id: 负责人userId
        :param state_code: 手机号国家码
        :param mobile: 手机号
        :param label_ids: 标签列表
        :param title: 职位
        :param share_dept_ids: 共享给的部门ID
        :param remark: 备注
        :param address: 地址
        :param company_name: 企业名
        :param share_user_ids: 共享给的员工userId列表
        :return:
        """
        if not isinstance(label_ids, (list, tuple, set)):
            label_ids = (label_ids, )
        if not isinstance(share_dept_ids, (list, tuple, set)):
            share_dept_ids = (share_dept_ids, )
        if not isinstance(share_user_ids, (list, tuple, set)):
            share_user_ids = (share_user_ids, )
        return self._top_request(
            "dingtalk.oapi.extcontact.create",
            {
                "contact": {
                    'name': name,
                    'follower_user_id': follower_user_id,
                    'state_code': state_code,
                    'mobile': mobile,
                    'label_ids': label_ids,
                    'title': title,
                    'share_dept_ids': share_dept_ids,
                    'remark': remark,
                    'address': address,
                    'company_name': company_name,
                    'share_user_ids': share_user_ids
                }
            },
            result_processor=lambda x: x['userid']
        )

    def update(self, user_id, name, follower_user_id, label_ids, mobile, state_code='86',
               title=None, share_dept_ids=(), remark=None, address=None, company_name=None, share_user_ids=()):
        """
        更新外部联系人

        :param user_id: 该外部联系人的userId
        :param name: 名称
        :param follower_user_id: 负责人userId
        :param state_code: 手机号国家码
        :param mobile: 手机号
        :param label_ids: 标签列表
        :param title: 职位
        :param share_dept_ids: 共享给的部门ID
        :param remark: 备注
        :param address: 地址
        :param company_name: 企业名
        :param share_user_ids: 共享给的员工userId列表
        :return:
        """
        if not isinstance(label_ids, (list, tuple, set)):
            label_ids = (label_ids, )
        if not isinstance(share_dept_ids, (list, tuple, set)):
            share_dept_ids = (share_dept_ids, )
        if not isinstance(share_user_ids, (list, tuple, set)):
            share_user_ids = (share_user_ids, )
        return self._top_request(
            "dingtalk.oapi.extcontact.update",
            {
                "contact": {
                    "user_id": user_id,
                    'name': name,
                    'follower_user_id': follower_user_id,
                    'state_code': state_code,
                    'mobile': mobile,
                    'label_ids': label_ids,
                    'title': title,
                    'share_dept_ids': share_dept_ids,
                    'remark': remark,
                    'address': address,
                    'company_name': company_name,
                    'share_user_ids': share_user_ids
                }
            }
        )

    def delete(self, user_id):
        """
        删除外部联系人

        :param user_id: 用户id
        """
        return self._top_request(
            "dingtalk.oapi.extcontact.delete",
            {"user_id": user_id}
        )
