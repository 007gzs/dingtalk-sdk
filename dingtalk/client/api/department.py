# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class Department(DingTalkBaseAPI):

    def list_ids(self, _id=1):
        """
        获取子部门ID列表

        :param _id: 父部门id(如果不传，默认部门为根部门，根部门ID为1)
        :return: 子部门ID列表数据
        """
        return self._get(
            '/department/list_ids',
            {'id': _id},
            result_processor=lambda x: x['sub_dept_id_list']
        )

    def list(self, _id=1, lang='zh_CN', fetch_child=False):
        """
        获取部门列表

        :param _id: 父部门id(如果不传，默认部门为根部门，根部门ID为1)
        :param lang: 通讯录语言(默认zh_CN，未来会支持en_US)
        :param fetch_child: 是否递归部门的全部子部门，ISV微应用固定传递false。
        :return: 部门列表数据。以部门的order字段从小到大排列
        """
        return self._get(
            '/department/list',
            {'id': _id, 'lang': lang, 'fetch_child': fetch_child},
            result_processor=lambda x: x['department']
        )

    def get(self, _id, lang='zh_CN'):
        """
        获取部门详情

        :param _id: 部门id
        :param lang: 通讯录语言(默认zh_CN，未来会支持en_US)
        :return: 部门列表数据。以部门的order字段从小到大排列
        """
        return self._get(
            '/department/get',
            {'id': _id, 'lang': lang}
        )

    def create(self, department_data):
        """
        创建部门

        :param department_data: 部门信息
        :return: 创建的部门id
        """
        if 'id' in department_data:
            raise AttributeError('不能包含Id')
        return self._post(
            '/department/create',
            department_data,
            result_processor=lambda x: x['id']
        )

    def update(self, department_data):
        """
        更新部门

        :param department_data: 部门信息
        :return: 已经更新的部门id
        """
        if 'id' not in department_data:
            raise AttributeError('必须包含Id')
        return self._post(
            '/department/update',
            department_data,
            result_processor=lambda x: x['id']
        )

    def delete(self, _id):
        """
        删除部门

        :param _id: 部门id。（注：不能删除根部门；不能删除含有子部门、成员的部门）
        :return:
        """
        return self._get(
            '/department/delete',
            {'id': _id}
        )

    def list_parent_depts_by_dept(self, _id):
        """
        查询部门的所有上级父部门路径

        :param _id: 希望查询的部门的id，包含查询的部门本身
        :return: 该部门的所有父部门id列表
        """
        return self._get(
            '/department/list_parent_depts_by_dept',
            {'id': _id},
            result_processor=lambda x: x['parentIds']
        )

    def list_parent_depts(self, user_id):
        """
        查询指定用户的所有上级父部门路径

        :param user_id: 希望查询的用户的id
        :return: 按顺序依次为其所有父部门的ID，直到根部门
        """
        return self._get(
            '/department/list_parent_depts',
            {'userId': user_id},
            result_processor=lambda x: x['department']
        )
