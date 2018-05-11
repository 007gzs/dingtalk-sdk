# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.core.utils import to_text


class BodyBase(object):

    _msgtype = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if callable(v):
                v = v()
            setattr(self, k, v)

    def get_dict(self):
        assert self._msgtype
        return {'msgtype': self._msgtype, self._msgtype: self.get_data()}

    def get_data(self):
        ret = {}
        for k in dir(self):
            if k.startswith('_'):
                continue
            v = getattr(self, k, None)
            if v is None or hasattr(v, '__call__'):
                continue
            if v is not None:
                if isinstance(v, BodyBase):
                    v = v.get_data()
                ret[k] = v
        return ret


class TextBody(BodyBase):
    _msgtype = 'text'
    content = None  # 消息内容

    def __init__(self, content, **kwargs):
        super(TextBody, self).__init__(content=content, **kwargs)


class FileBody(BodyBase):
    _msgtype = 'text'
    media_id = None  # 媒体文件id，可以调用上传媒体文件接口获取。10MB

    def __init__(self, media_id, **kwargs):
        super(FileBody, self).__init__(media_id=media_id, **kwargs)


class ImageBody(FileBody):
    _msgtype = 'image'


class VoiceBody(FileBody):
    _msgtype = 'voice'
    duration = None  # 正整数，小于60，表示音频时长

    def __init__(self, media_id, duration=None, **kwargs):
        super(VoiceBody, self).__init__(media_id=media_id, duration=duration, **kwargs)


class LinkBody(BodyBase):
    _msgtype = 'link'
    link = None

    def __init__(self, message_url, pic_url, title, text, **kwargs):
        """
        :param message_url: 消息点击链接地址
        :param pic_url: 图片媒体文件id，可以调用上传媒体文件接口获取
        :param title: 消息标题
        :param text: 消息描述
        """
        super(LinkBody, self).__init__(link={'messageUrl': message_url, 'picUrl': pic_url,
                                             'title': title, 'text': text}, **kwargs)


class MarkdownBody(BodyBase):
    _msgtype = "markdown"
    title = None  # 首屏会话透出的展示内容
    text = None  # markdown格式的消息

    def __init__(self, title, text, **kwargs):
        super(MarkdownBody, self).__init__(title=title, text=text, **kwargs)


class OaBodyContent(BodyBase):
    title = None  # 消息体的标题
    _form = None  # 消息体的表单，最多显示6个，超过会被隐藏
    rich = None  # 单行富文本信息
    content = None  # 消息体的内容，最多显示3行
    image = None  # 消息体中的图片media_id
    file_count = None  # 自定义的附件数目。此数字仅供显示，钉钉不作验证
    author = None  # 自定义的作者名字

    def __init__(self, title=None, content=None, author=None, image=None, file_count=None, forms=dict,
                 rich_num=None, rish_unit=None, **kwargs):
        """
        OA消息体
        :param title: 消息体的标题
        :param content: 消息体的内容，最多显示3行
        :param author: 	自定义的作者名字
        :param image: 消息体中的图片media_id
        :param file_count: 自定义的附件数目。此数字仅供显示，钉钉不作验证
        :param forms: 消息体的表单
        :param rich_num: 单行富文本信息的数目
        :param rish_unit: 单行富文本信息的单位
        :param kwargs:
        """
        rich = None
        if rich_num is not None or rish_unit is not None:
            rich = {'num': rich_num, 'unit': rish_unit}
        super(OaBodyContent, self).__init__(title=title, content=content, author=author, image=image,
                                            file_count=file_count, _forms=forms, rich=rich, **kwargs)

    @property
    def form(self):
        if not self._form:
            return None
        ret = []
        for k, v in self._form:
            ret.append({"key": k, "value": v})
        return ret


class OaBody(BodyBase):
    _msgtype = 'oa'
    message_url = None  # 客户端点击消息时跳转到的H5地址
    pc_message_url = None  # PC端点击消息时跳转到的H5地址
    head = None  # 消息头部内容
    body = None  # 消息体

    def __init__(self, message_url, head_bgcolor, head_text, body, pc_message_url=None, **kwargs):
        super(OaBody, self).__init__(message_url=message_url, head={"bgcolor": head_bgcolor, "text": head_text},
                                     body=body, pc_message_url=pc_message_url, **kwargs)


class ActionCardBody(BodyBase):
    _msgtype = 'action_card'
    title = None  # 透出到会话列表和通知的文案
    markdown = None  # 消息内容，支持markdown

    def __init__(self, title, markdown, **kwargs):
        super(ActionCardBody, self).__init__(title=title, markdown=markdown, **kwargs)


class SingleActionCardBody(BodyBase):
    single_title = None  # 使用整体跳转ActionCard样式时的标题
    single_url = None  # 使用整体跳转ActionCard样式时的链接url

    def __init__(self, single_title, single_url, **kwargs):
        super(SingleActionCardBody, self).__init__(single_title=single_title, single_url=single_url, **kwargs)


class BtnActionCardBody(BodyBase):
    btn_orientation = None  # 使用独立跳转ActionCard样式时的按钮排列方式，竖直排列(0)，横向排列(1)
    btn_json_list = None  # 使用独立跳转ActionCard样式时的按钮列表

    def __init__(self, btn_orientation, btn_json_list=list, **kwargs):
        btn_orientation = to_text(btn_orientation)
        assert btn_orientation in ('0', '1')
        super(BtnActionCardBody, self).__init__(btn_orientation=btn_orientation, btn_json_list=btn_json_list, **kwargs)

    def add_btn(self, title, action_url):
        assert isinstance(self.btn_json_list, list)
        self.btn_json_list.append({'title': title, 'action_url': action_url})
