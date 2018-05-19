# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six
from dingtalk.core.utils import to_text, json_loads

from dingtalk.client.api.base import DingTalkBaseAPI


class Cspace(DingTalkBaseAPI):

    def add_to_single_chat(self, agent_id, userid, media_id, file_name):
        """
        发送文件给指定用户

        :param agent_id: 文件发送者微应用的agentId
        :param userid: 文件接收人的userid
        :param media_id: 调用钉盘上传文件接口得到的mediaid
        :param file_name: 文件名(需包含含扩展名)
        :return:
        """
        return self._post(
            '/cspace/add_to_single_chat',
            params={
                'agent_id': agent_id,
                'userid': userid,
                'media_id': media_id,
                'file_name': file_name
            }
        )

    def add(self, code, media_id, space_id, folder_id, name, agent_id=None, overwrite=False):
        """
        新增文件到用户钉盘

        :param code: 如果是微应用，code值为微应用免登授权码,如果是服务窗应用，code值为服务窗免登授权码
                     code为临时授权码，只能消费一次，下次请求需要重新获取新的code。
        :param media_id: 调用钉盘上传文件接口得到的mediaid
        :param space_id: 调用云盘选择控件后获取的用户钉盘空间ID
        :param folder_id: 调用云盘选择控件后获取的用户钉盘文件夹ID
        :param name: 上传文件的名称，不能包含非法字符
        :param agent_id: 微应用的agentId
        :param overwrite: 到同名文件是否覆盖，若不覆盖，则会自动重命名本次新增的文件
        :return:
        """
        return self._get(
            '/cspace/add',
            {
                'agent_id': agent_id,
                'code': code,
                'media_id': media_id,
                'space_id': space_id,
                'folder_id': folder_id,
                'name': name,
                'overwrite': overwrite
            },
            result_processor=lambda x:
                json_loads(x['dentry']) if isinstance(x['dentry'], six.string_types) else x['dentry']
        )

    def get_custom_space(self, domain=None, agent_id=None):
        """
        获取企业下的自定义空间

        :param domain: 企业调用时传入，需要为10个字节以内的字符串，仅可包含字母和数字，大小写不敏感
        :param agent_id: ISV调用时传入，微应用agentId
        :return: 申请到的空间id
        """
        return self._get(
            '/cspace/get_custom_space',
            {
                'agent_id': agent_id,
                'domain': domain
            },
            result_processor=lambda x: x['spaceid']
        )

    def grant_custom_space(self, isdownload, userid, agent_id=None, domain=None, duration=30, path=None, fileids=()):
        """
        授权用户访问企业下的自定义空间

        :param isdownload: 权限类型，true为下载，false为上传
        :param userid: 企业用户userid
        :param agent_id: ISV调用时传入，授权访问指定微应用的自定义空间
        :param domain: 企业调用时传入，授权访问该domain的自定义空间
        :param duration: 权限有效时间，有效范围为0~3600秒，超出此范围或不传默认为30秒
        :param path: 授权访问的路径
        :param fileids: 授权访问的文件id列表
        :return:
        """
        _type = 'download' if isdownload else 'add'
        fileids = ','.join(map(to_text, fileids))
        return self._get(
            '/cspace/grant_custom_space',
            {
                'type': _type,
                'agent_id': agent_id,
                'domain': domain,
                'userid': userid,
                'duration': duration,
                'path': path,
                'fileids': fileids
            },
            result_processor=lambda x: x['spaceid']
        )

    def file_upload_transaction(self, agent_id, file_size, chunk_numbers, upload_id=None):
        """
        开启/提交 文件上传事务

        :param agent_id: 微应用的agentId
        :param file_size: 文件大小
        :param chunk_numbers: 文件总块数
        :param upload_id: 上传事务id 不传该值为开启事务，传该值为提交事务
        :return: 开启事务：上传事务id； 提交事务：文件存储id
        """
        return self._get(
            '/file/upload/transaction',
            {
                'agent_id': agent_id,
                'file_size': file_size,
                'chunk_numbers': chunk_numbers,
                'upload_id': upload_id
            },
            result_processor=lambda x: x['upload_id'] if upload_id is None else x['media_id']
        )

    def file_upload_chunk(self, agent_id, upload_id, chunk_sequence, file_chunk):
        """
        上传文件块

        :param agent_id: 微应用的agentId
        :param upload_id: 上传事务id
        :param chunk_sequence: 文件块号，从1开始计数
        :param file_chunk: 要上传的文件块，一个 File-object
        :return:
        """
        return self._post(
            '/file/upload/chunk',
            params={
                'agent_id': agent_id,
                'upload_id': upload_id,
                'chunk_sequence': chunk_sequence
            },
            files={
                'file': file_chunk
            }
        )

    def file_upload_single(self, agent_id, file_size, media_file):
        """
        单步文件上传

        :param agent_id: 微应用的agentId
        :param file_size: 文件大小
        :param media_file: 要上传的文件，一个 File-object
        :return:
        """
        return self._post(
            '/file/upload/single',
            params={
                'agent_id': agent_id,
                'file_size': file_size
            },
            files={
                'file': media_file
            },
            result_processor=lambda x: x['media_id']
        )
