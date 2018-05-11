# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client.api.base import DingTalkBaseAPI


class MicroApp(DingTalkBaseAPI):

    def create(self, app_icon, app_name, app_desc, homepage_url, pc_homepage_url=None, omp_link=None):
        """
        创建微应用

        :param app_icon: 微应用的图标。需要调用上传接口将图标上传到钉钉服务器后获取到的mediaId
        :param app_name: 微应用的名称。长度限制为1~10个字符
        :param app_desc: 微应用的描述。长度限制为1~20个字符
        :param homepage_url: 微应用的移动端主页，必须以http开头或https开头
        :param pc_homepage_url: 微应用的PC端主页，必须以http开头或https开头，如果不为空则必须与homepageUrl的域名一致
        :param omp_link: 微应用的OA后台管理主页，必须以http开头或https开头。
        :return: 微应用实例化id
        """
        return self._post(
            '/microapp/create',
            {
                "appIcon": app_icon,
                "appName": app_name,
                "appDesc": app_desc,
                "homepageUrl": homepage_url,
                "pcHomepageUrl": pc_homepage_url,
                "ompLink": omp_link
            },
            result_processor=lambda x: x['agentId']
        )

    def update(self, agent_id, app_icon=None, app_name=None, app_desc=None,
               homepage_url=None, pc_homepage_url=None, omp_link=None):
        """
        更新微应用

        :param agent_id: 微应用实例化id
        :param app_icon: 微应用的图标。需要调用上传接口将图标上传到钉钉服务器后获取到的mediaId
        :param app_name: 微应用的名称。长度限制为1~10个字符
        :param app_desc: 微应用的描述。长度限制为1~20个字符
        :param homepage_url: 微应用的移动端主页，必须以http开头或https开头
        :param pc_homepage_url: 微应用的PC端主页，必须以http开头或https开头，如果不为空则必须与homepageUrl的域名一致
        :param omp_link: 微应用的OA后台管理主页，必须以http开头或https开头。
        :return: 微应用实例化id
        """
        return self._post(
            '/microapp/update',
            {
                "agentId": agent_id,
                "appIcon": app_icon,
                "appName": app_name,
                "appDesc": app_desc,
                "homepageUrl": homepage_url,
                "pcHomepageUrl": pc_homepage_url,
                "ompLink": omp_link
            },
            result_processor=lambda x: x['agentId']
        )

    def delete(self, agent_id):
        """
        删除微应用

        :param agent_id: 微应用实例化id，企业只能删除自建微应用
        :return:
        """
        return self._post(
            '/microapp/delete',
            {'agentId': agent_id}
        )

    def list(self):
        """
        列出微应用

        :return: 微应用列表
        """
        return self._post(
            '/microapp/list',
            result_processor=lambda x: x['appList']
        )

    def list_by_userid(self, userid):
        """
        列出员工可见的微应用

        :return: 微应用列表
        """
        return self._get(
            '/microapp/list_by_userid',
            {'userid': userid},
            result_processor=lambda x: x['appList']
        )

    def visible_scopes(self, agent_id):
        """
        删除微应用

        :param agent_id: 需要查询的微应用实例化agentId
        :return:
        """
        return self._post(
            '/microapp/visible_scopes',
            {'agentId': agent_id}
        )

    def set_visible_scopes(self, agent_id, is_hidden=False, dept_visible_scopes=(), user_visible_scopes=()):
        """
        设置微应用的可见范围

        :param agent_id: 微应用实例化id
        :param is_hidden: 是否仅限管理员可见，true代表仅限管理员可见
        :param dept_visible_scopes: 设置可见的部门id列表
        :param user_visible_scopes: 设置可见的员工id列表
        :return:
        """
        return self._post(
            '/microapp/set_visible_scopes',
            {
                "agentId": agent_id,
                "isHidden": is_hidden,
                "deptVisibleScopes": dept_visible_scopes,
                "userVisibleScopes": user_visible_scopes
            }
        )
