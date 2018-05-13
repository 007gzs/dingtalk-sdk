# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

from dingtalk.core.utils import ObjectDict, DingTalkSigner


class UtilityTestCase(unittest.TestCase):

    def test_object_dict(self):
        obj = ObjectDict()
        self.assertTrue(obj.xxx is None)
        obj.xxx = 1
        self.assertEqual(1, obj.xxx)

    def test_wechat_card_signer(self):

        signer = DingTalkSigner()
        signer.add_data('789')
        signer.add_data('456')
        signer.add_data('123')
        signature = signer.signature

        self.assertEqual('f7c3bc1d808e04732adf679965ccc34ca7ae3441', signature)

