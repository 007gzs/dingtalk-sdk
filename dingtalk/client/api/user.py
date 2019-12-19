# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class User(DingTalkBaseAPI):

    def auth_scopes(self):
        """
        获取CorpSecret授权范围

        :return:
        """
        return self._get('/auth/scopes')

    def get_org_user_count(self, only_active):
        """
        获取企业员工人数

        :param only_active: 是否包含未激活钉钉的人员数量
        :return: 企业员工数量
        """
        return self._get(
            '/user/get_org_user_count',
            {'onlyActive': 0 if only_active else 1},
            result_processor=lambda x: x['count']
        )

    def getuserinfo(self, code):
        """
        通过CODE换取用户身份

        :param code: requestAuthCode接口中获取的CODE
        :return:
        """
        return self._get(
            '/user/getuserinfo',
            {'code': code}
        )

    def get(self, userid, lang='zh_CN'):
        """
        获取成员详情

        :param userid: 员工在企业内的UserID，企业用来唯一标识用户的字段
        :param lang: 通讯录语言(默认zh_CN，未来会支持en_US)
        :return:
        """
        return self._get(
            '/user/get',
            {'userid': userid, 'lang': lang}
        )

    def create(self, user_data):
        """
        创建成员

        :param user_data: 用户信息
        :return: userid
        """
        return self._post(
            '/user/create',
            user_data,
            result_processor=lambda x: x['userid']

        )

    def update(self, user_data):
        """
        更新成员

        :param user_data: 用户信息
        :return:
        """
        return self._post(
            '/user/update',
            user_data
        )

    def delete(self, userid):
        """
        删除成员

        :param userid: 员工在企业内的UserID，企业用来唯一标识用户的字段
        :return:
        """
        return self._get(
            '/user/delete',
            {'userid': userid}
        )

    def batchdelete(self, user_ids):
        """
        批量删除成员

        :param user_ids: 员工UserID列表。列表长度在1到20之间
        :return:
        """
        return self._post(
            '/user/delete',
            {'useridlist': list(user_ids)}
        )

    def simple_list(self, department_id, offset=0, size=100, order='custom', lang='zh_CN'):
        """
        获取部门成员

        :param department_id: 获取的部门id
        :param offset: 偏移量
        :param size: 表分页大小，最大100
        :param order: 排序规则
                      entry_asc     代表按照进入部门的时间升序
                      entry_desc    代表按照进入部门的时间降序
                      modify_asc    代表按照部门信息修改时间升序
                      modify_desc   代表按照部门信息修改时间降序
                      custom        代表用户定义排序
        :param lang: 通讯录语言(默认zh_CN另外支持en_US)
        :return:
        """
        return self._get(
            '/user/simplelist',
            {
                'department_id': department_id,
                'offset': offset,
                'size': size,
                'order': order,
                'lang': lang
            }
        )

    def list(self, department_id, offset=0, size=100, order='custom', lang='zh_CN'):
        """
        获取部门成员（详情）

        :param department_id: 获取的部门id
        :param offset: 偏移量
        :param size: 表分页大小，最大100
        :param order: 排序规则
                      entry_asc     代表按照进入部门的时间升序
                      entry_desc    代表按照进入部门的时间降序
                      modify_asc    代表按照部门信息修改时间升序
                      modify_desc   代表按照部门信息修改时间降序
                      custom        代表用户定义排序
        :param lang: 通讯录语言(默认zh_CN另外支持en_US)
        :return:
        """
        return self._get(
            '/user/list',
            {
                'department_id': department_id,
                'offset': offset,
                'size': size,
                'order': order,
                'lang': lang
            }
        )

    def get_admin(self):
        """
        获取管理员列表

        :return: sys_level	管理员角色 1:主管理员,2:子管理员
        """
        return self._get(
            '/user/get_admin',
            result_processor=lambda x: x['admin_list']
        )

    def can_access_microapp(self, app_id, user_id):
        """
        获取管理员的微应用管理权限

        :param app_id: 微应用id
        :param user_id: 员工唯一标识ID
        :return: 是否能管理该微应用
        """
        return self._get(
            '/user/can_access_microapp',
            {'appId': app_id, 'userId': user_id},
            result_processor=lambda x: x['canAccess']
        )

    def get_userid_by_unionid(self, unionid):
        """
        根据unionid获取成员的userid

        :param unionid: 用户在当前钉钉开放平台账号范围内的唯一标识
        :return:
        """
        return self._get(
            '/user/getUseridByUnionid',
            {'unionid': unionid}
        )

    def get_dept_member(self, dept_id):
        """
        获取部门用户userid列表

        :param dept_id: 用户在当前钉钉开放平台账号范围内的唯一标识
        :return 部门userid列表:
        """
        return self._get(
            '/user/getDeptMember',
            {'deptId': dept_id},
            result_processor=lambda x: x['userIds']
        )

    def listbypage(self, department_id, offset=0, size=100, order='custom', lang='zh_CN'):
        """
        获取部门用户

        :param department_id: 获取的部门id
        :param offset: 偏移量
        :param size: 表分页大小，最大100
        :param order: 排序规则
                      entry_asc     代表按照进入部门的时间升序
                      entry_desc    代表按照进入部门的时间降序
                      modify_asc    代表按照部门信息修改时间升序
                      modify_desc   代表按照部门信息修改时间降序
                      custom        代表用户定义排序
        :param lang: 通讯录语言(默认zh_CN另外支持en_US)
        :return:
        """
        return self._get(
            '/user/list',
            {
                'department_id': department_id,
                'offset': offset,
                'size': size,
                'order': order,
                'lang': lang
            }
        )

    def get_admin_scope(self, userid):
        """
        查询管理员通讯录权限范围

        :param userid: 用户id
        """
        return self._top_request(
            "dingtalk.oapi.user.get_admin_scope",
            {"userid": userid},
            result_processor=lambda x: x['dept_ids']
        )
