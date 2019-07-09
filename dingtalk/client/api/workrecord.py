# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import datetime
import time

from dingtalk.client.api.base import DingTalkBaseAPI


class WorkRecord(DingTalkBaseAPI):

    def add(self, userid, create_time, title, url, form_item_dict, originator_user_id='', source_name=''):
        """
        新增待办事项

        :param userid: 用户id
        :param create_time: 待办时间。Unix时间戳
        :param title: 标题
        :param url: 待办跳转url
        :param form_item_dict: 表单列表 OrderedDict((('标题1', '内容1'),('标题2', '内容2')))
        :param originator_user_id: manager7078
        :param source_name: 待办来源名称
        """

        if isinstance(create_time, (datetime.date, datetime.datetime)):
            create_time = int(time.mktime(create_time.timetuple()) * 1000)
        form_item_list = [{'title': k, 'content': v}for k, v in form_item_dict.items()]
        return self._top_request(
            "dingtalk.oapi.workrecord.add",
            {
                "userid": userid,
                "create_time": create_time,
                "title": title,
                "url": url,
                "formItemList": form_item_list,
                "originator_user_id": originator_user_id,
                "source_name": source_name
            },
            result_processor=lambda x: x['record_id']
        )

    def update(self, userid, record_id):
        """
        更新待办事项状态

        :param userid: 用户id
        :param record_id: 待办事项唯一id
        """
        return self._top_request(
            "dingtalk.oapi.workrecord.update",
            {"userid": userid, "record_id": record_id}
        )

    def getbyuserid(self, userid, status, offset=0, limit=50):
        """
        获取用户的待办事项

        :param userid: 用户唯一ID
        :param offset: 分页游标，从0开始，如返回结果中has_more为true，则表示还有数据，offset再传上一次的offset+limit
        :param limit: 分页大小，最多50
        :param status: 待办事项状态，0表示未完成，1表示完成
        """
        return self._top_request(
            "dingtalk.oapi.workrecord.getbyuserid",
            {
                "userid": userid,
                "offset": offset,
                "limit": limit,
                "status": status
            },
            result_processor=lambda x: x['records']
        )
