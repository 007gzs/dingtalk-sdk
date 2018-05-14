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
    content = None

    def __init__(self, content, **kwargs):
        """
        文本消息

        :param content: 消息内容
        :param kwargs:
        """
        super(TextBody, self).__init__(content=content, **kwargs)


class FileBody(BodyBase):
    _msgtype = 'file'
    media_id = None

    def __init__(self, media_id, **kwargs):
        """
        文件消息

        :param media_id: 媒体文件id，可以调用上传媒体文件接口获取。10MB
        :param kwargs:
        """
        super(FileBody, self).__init__(media_id=media_id, **kwargs)


class ImageBody(FileBody):
    _msgtype = 'image'

    def __init__(self, media_id, **kwargs):
        """
        图片消息

        :param media_id: 图片媒体文件id，可以调用上传媒体文件接口获取。建议宽600像素 x 400像素，宽高比3：2
        :param kwargs:
        """
        super(FileBody, self).__init__(media_id=media_id, **kwargs)


class VoiceBody(FileBody):
    _msgtype = 'voice'
    duration = None

    def __init__(self, media_id, duration=None, **kwargs):
        """
        语音消息

        :param media_id: 语音媒体文件id，可以调用上传媒体文件接口获取。2MB，播放长度不超过60s，AMR格式
        :param duration: 正整数，小于60，表示音频时长
        :param kwargs:
        """
        super(VoiceBody, self).__init__(media_id=media_id, duration=duration, **kwargs)


class LinkBody(BodyBase):
    _msgtype = 'link'
    messageUrl = None
    title = None
    text = None
    picUrl = None

    def __init__(self, message_url, pic_url, title, text, **kwargs):
        """
        超链接消息

        :param message_url: 消息点击链接地址
        :param pic_url: 图片媒体文件id，可以调用上传媒体文件接口获取
        :param title: 消息标题
        :param text: 消息描述
        """
        super(LinkBody, self).__init__(messageUrl=message_url, picUrl=pic_url,  title=title, text=text, **kwargs)


class MarkdownBody(BodyBase):
    _msgtype = "markdown"
    title = None
    text = None

    def __init__(self, title, text, **kwargs):
        """
        markdown消息

        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息
        :param kwargs:
        """
        super(MarkdownBody, self).__init__(title=title, text=text, **kwargs)


class OaBodyContent(BodyBase):
    title = None
    _forms = None
    rich = None
    content = None
    image = None
    file_count = None
    author = None

    def __init__(self, title=None, content=None, author=None, image=None, file_count=None, forms=dict,
                 rich_num=None, rish_unit=None, **kwargs):
        """
        OA消息 消息体

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
        if not self._forms:
            return None
        ret = []
        for k, v in self._forms.items():
            ret.append({"key": k, "value": v})
        return ret


class OaBody(BodyBase):
    _msgtype = 'oa'
    message_url = None
    pc_message_url = None
    head = None
    body = None

    def __init__(self, message_url, head_bgcolor, head_text, body, pc_message_url=None, **kwargs):
        """
        OA消息

        :param message_url: 客户端点击消息时跳转到的H5地址
        :param head_bgcolor: 消息头部的背景颜色。长度限制为8个英文字符，其中前2为表示透明度，后6位表示颜色值。不要添加0x
        :param head_text: 消息的头部标题（向普通会话发送时有效，向企业会话发送时会被替换为微应用的名字），长度限制为最多10个字符
        :param body: OaBodyContent OA消息 消息体
        :param pc_message_url: PC端点击消息时跳转到的H5地址
        :param kwargs:
        """
        super(OaBody, self).__init__(message_url=message_url, head={"bgcolor": head_bgcolor, "text": head_text},
                                     body=body, pc_message_url=pc_message_url, **kwargs)


class ActionCardBody(BodyBase):
    _msgtype = 'action_card'
    title = None
    markdown = None

    def __init__(self, title, markdown, **kwargs):
        super(ActionCardBody, self).__init__(title=title, markdown=markdown, **kwargs)


class SingleActionCardBody(ActionCardBody):
    single_title = None
    single_url = None

    def __init__(self, title, markdown, single_title, single_url, **kwargs):
        """
        整体跳转ActionCard消息

        :param title: 透出到会话列表和通知的文案
        :param markdown: 消息内容，支持markdown
        :param single_title: 标题
        :param single_url: 链接url
        :param kwargs:
        """
        super(SingleActionCardBody, self).__init__(title=title, markdown=markdown,
                                                   single_title=single_title, single_url=single_url, **kwargs)


class BtnActionCardBody(ActionCardBody):
    btn_orientation = None
    btn_json_list = None

    def __init__(self, title, markdown, btn_orientation, btn_list=(), **kwargs):
        """
        独立跳转ActionCard消息

        :param title: 透出到会话列表和通知的文案
        :param markdown: 消息内容，支持markdown
        :param btn_orientation: 按钮排列方式，竖直排列(0)，横向排列(1)
        :param btn_json_list: 按钮列表
        :param kwargs:
        """
        btn_orientation = to_text(btn_orientation)
        assert btn_orientation in ('0', '1')
        super(BtnActionCardBody, self).__init__(title=title, markdown=markdown,
                                                btn_orientation=btn_orientation, btn_json_list=list(btn_list), **kwargs)

    def add_btn(self, title, action_url):
        """
        添加按钮

        :param title: 标题
        :param action_url: 链接url
        :return:
        """
        assert isinstance(self.btn_json_list, list)
        self.btn_json_list.append({'title': title, 'action_url': action_url})
