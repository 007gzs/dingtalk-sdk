# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest


class MessagesTestCase(unittest.TestCase):

    def test_text_message(self):
        from dingtalk.model.message import TextBody

        msgbody = TextBody('test')
        msg = msgbody.get_dict()

        self.assertEqual('text', msg['msgtype'])
        self.assertEqual('test', msg['text']['content'])

    def test_file_message(self):
        from dingtalk.model.message import FileBody

        msgbody = FileBody('123456')
        msg = msgbody.get_dict()

        self.assertEqual('file', msg['msgtype'])
        self.assertEqual('123456', msg['file']['media_id'])

    def test_file_message(self):
        from dingtalk.model.message import ImageBody

        msgbody = ImageBody('123456')
        msg = msgbody.get_dict()

        self.assertEqual('image', msg['msgtype'])
        self.assertEqual('123456', msg['image']['media_id'])

    def test_voice_message(self):
        from dingtalk.model.message import VoiceBody

        msgbody = VoiceBody('123456')
        msg = msgbody.get_dict()

        self.assertEqual('123456', msgbody.media_id)
        self.assertEqual('voice', msg['msgtype'])
        self.assertEqual('123456', msg['voice']['media_id'])

    def test_link_message(self):
        from dingtalk.model.message import LinkBody

        msgbody = LinkBody('http://dingtalk.com', 'http://dingtalk.com/img.png', 'testtitle', 'testtext')
        msg = msgbody.get_dict()

        self.assertEqual('link', msg['msgtype'])
        self.assertEqual('http://dingtalk.com', msg['link']['messageUrl'])
        self.assertEqual('http://dingtalk.com/img.png', msg['link']['picUrl'])
        self.assertEqual('testtitle', msg['link']['title'])
        self.assertEqual('testtext', msg['link']['text'])

    def test_markdown_message(self):
        from dingtalk.model.message import MarkdownBody

        msgbody = MarkdownBody('title', 'markdowntext')
        msg = msgbody.get_dict()

        self.assertEqual('markdown', msg['msgtype'])
        self.assertEqual('title', msg['markdown']['title'])
        self.assertEqual('markdowntext', msg['markdown']['text'])

    def test_oa_message(self):
        from collections import OrderedDict
        from dingtalk.model.message import OaBodyContent, OaBody

        body_content = OaBodyContent('title', 'content', 'author', '123', '1', OrderedDict({'key1': 'value1', 'key2': 'value2'}), '1.12', 'unit')
        msgbody = OaBody('http://dingtalk.com', 'ffffff', 'head_text', body_content, 'http://dingtalk.com/index.html')
        msg = msgbody.get_dict()

        self.assertEqual('oa', msg['msgtype'])
        self.assertEqual('http://dingtalk.com', msg['oa']['message_url'])
        self.assertEqual('http://dingtalk.com/index.html', msg['oa']['pc_message_url'])
        self.assertEqual('ffffff', msg['oa']['head']['bgcolor'])
        self.assertEqual('head_text', msg['oa']['head']['text'])
        self.assertEqual('title', msg['oa']['body']['title'])
        self.assertEqual('content', msg['oa']['body']['content'])
        self.assertEqual('author', msg['oa']['body']['author'])
        self.assertEqual('123', msg['oa']['body']['image'])
        self.assertEqual('1', msg['oa']['body']['file_count'])
        self.assertEqual('1.12', msg['oa']['body']['rich']['num'])
        self.assertEqual('unit', msg['oa']['body']['rich']['unit'])
        self.assertEqual('key1', msg['oa']['body']['form'][0]['key'])
        self.assertEqual('value1', msg['oa']['body']['form'][0]['value'])
        self.assertEqual('key2', msg['oa']['body']['form'][1]['key'])
        self.assertEqual('value2', msg['oa']['body']['form'][1]['value'])

    def test_single_action_card_message(self):
        from dingtalk.model.message import SingleActionCardBody

        msgbody = SingleActionCardBody('title', 'markdown', 'single_title', 'http://dingtalk.com/index.html')
        msg = msgbody.get_dict()

        self.assertEqual('action_card', msg['msgtype'])
        self.assertEqual('title', msg['action_card']['title'])
        self.assertEqual('markdown', msg['action_card']['markdown'])
        self.assertEqual('single_title', msg['action_card']['single_title'])
        self.assertEqual('title', msg['action_card']['title'])
        self.assertEqual('http://dingtalk.com/index.html', msg['action_card']['single_url'])

    def test_button_action_card_message(self):
        from dingtalk.model.message import BtnActionCardBody

        msgbody = BtnActionCardBody('title', 'markdown', '0', [{'title': 'title1', 'action_url': 'action_url1'}, {'title': 'title2', 'action_url': 'action_url2'}])
        msgbody.add_btn('title3', 'action_url3')
        msg = msgbody.get_dict()

        self.assertEqual('action_card', msg['msgtype'])
        self.assertEqual('title', msg['action_card']['title'])
        self.assertEqual('markdown', msg['action_card']['markdown'])
        self.assertEqual('0', msg['action_card']['btn_orientation'])
        self.assertEqual('title1', msg['action_card']['btn_json_list'][0]['title'])
        self.assertEqual('action_url1', msg['action_card']['btn_json_list'][0]['action_url'])
        self.assertEqual('title2', msg['action_card']['btn_json_list'][1]['title'])
        self.assertEqual('action_url2', msg['action_card']['btn_json_list'][1]['action_url'])
        self.assertEqual('title3', msg['action_card']['btn_json_list'][2]['title'])
        self.assertEqual('action_url3', msg['action_card']['btn_json_list'][2]['action_url'])
