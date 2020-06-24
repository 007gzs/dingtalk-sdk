# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.core.utils import to_text

from dingtalk.client.api.base import DingTalkBaseAPI


class Role(DingTalkBaseAPI):

    def simplelist(self, role_id, offset=0, size=20):
        """
        获取角色的员工列表

        :param role_id: 角色ID
        :param offset: 分页大小
        :param size: 分页偏移
        :return:
        """
        return self._top_request(
            'dingtalk.corp.role.simplelist',
            {'role_id': role_id, 'offset': offset, 'size': size}
        )

    def list(self, offset=0, size=20):
        """
        获取企业角色列表

        :param offset: 分页大小
        :param size: 分页偏移
        :return:
        """
        return self._top_request(
            'dingtalk.corp.role.list',
            {'offset': offset, 'size': size}
        )

    def addrolesforemps(self, rolelid_list, userid_list):
        """
        批量为员工增加角色信息

        :param rolelid_list: 角色id list
        :param userid_list: 员工id list
        :return:
        """
        if isinstance(rolelid_list, (list, tuple, set)):
            rolelid_list = ','.join(map(to_text, rolelid_list))
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))
        return self._top_request(
            'dingtalk.corp.role.addrolesforemps',
            {'rolelid_list': rolelid_list, 'userid_list': userid_list}
        )

    def removerolesforemps(self, rolelid_list, userid_list):
        """
        批量删除员工角的色信息

        :param rolelid_list: 角色id list
        :param userid_list: 员工id list
        :return:
        """
        if isinstance(rolelid_list, (list, tuple, set)):
            rolelid_list = ','.join(map(to_text, rolelid_list))
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))
        return self._top_request(
            'dingtalk.corp.role.removerolesforemps',
            {'rolelid_list': rolelid_list, 'userid_list': userid_list}
        )

    def deleterole(self, role_id):
        """
        删除角色信息

        :param role_id: 角色id
        :return:
        """
        return self._top_request(
            'dingtalk.corp.role.deleterole',
            {'role_id': role_id}
        )

    def getrolegroup(self, group_id):
        """
        获取角色组信息

        :param group_id: 角色组的Id
        :return:
        """
        return self._top_request(
            'dingtalk.corp.role.getrolegroup',
            {'group_id': group_id},
            result_processor=lambda x: x['role_group']
        )

    def getrole(self, role_id):
        """
        获取角色详情

        :param role_id: 角色id
        """
        return self._top_request(
            "dingtalk.oapi.role.getrole",
            {
                "roleId": role_id
            }
        )

    def add_role(self, role_name, group_id):
        """
        创建角色

        :param role_name: 角色名称
        :param group_id: 角色组id
        """
        return self.post(
            "/role/add_role",
            {
                "roleName": role_name,
                "groupId": group_id
            }
        )

    def update_role(self, role_name, group_id):
        """
        更新角色

        :param role_name: 角色名称
        :param group_id: 角色组id
        """
        return self.post(
            "/role/update_role",
            {
                "roleName": role_name,
                "groupId": group_id
            }
        )

    def add_role_group(self, name):
        """
        创建角色组

        :param name: 角色组名称
        """
        return self.post(
            "/role/add_role_group",
            {"name": name},
            result_processor=lambda x: x['groupId']
        )
