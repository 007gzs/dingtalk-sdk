# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

import json

from dingtalk import crypto as _crypto
from dingtalk.crypto import DingTalkCrypto


class PrpCryptoMock(_crypto.PrpCrypto):

    def get_random_string(self):
        return '1234567890123456'


class CryptoTestCase(unittest.TestCase):

    token = '123456'
    encoding_aes_key = '4g5j64qlyl3zvetqxz5jiocdr586fn2zvjpa8zls3ij'
    suite_key = 'suite4xxxxxxxxxxxxxxx'

    def test_encrypt_message(self):
        origin_crypto = _crypto.PrpCrypto
        _crypto.PrpCrypto = PrpCryptoMock

        nonce = 'nEXhMP4r'
        timestamp = '1445827045067'
        msg = """{"EventType":"check_create_suite_url","Random":"LPIdSnlF","TestSuiteKey":"suite4xxxxxxxxxxxxxxx"}"""

        expected = {
            'msg_signature':'bcf6dcefa4ce2dbaf7b0666c7264d46fd9aad4bd',
            'encrypt': '5DJFWzjRNOQk+5GSZxW+VrFMDWCIidPjEjg3//gm5x556BedVi62rDj1F9uXU97a4jw1R4FACUv9RCpoDobNqxhxRB2YtW901k4KHbP1/wpFJ3xdLG0n0A8U1VhENg80zKJd+YROR0YMGum4WYuoXJ6J98vt0ihYeIFoapNddLML5MyNAGM9saSpkouDMSvD+iU14i7V8ix1ia1Tb9ogog==',
            'timeStamp': '1445827045067',
            'nonce': 'nEXhMP4r'
        }
        crypto = DingTalkCrypto(self.token, self.encoding_aes_key, self.suite_key)
        encrypted = crypto.encrypt_message(msg, nonce, timestamp)

        _crypto.PrpCrypto = origin_crypto

        self.assertEqual(expected.keys(), encrypted.keys())
        for key in expected.keys():
            self.assertEqual(expected[key], encrypted[key])

    def test_decrypt_message(self):
        from dingtalk.core.utils import to_text
        jsonstr = """{"encrypt":"1a3NBxmCFwkCJvfoQ7WhJHB+iX3qHPsc9JbaDznE1i03peOk1LaOQoRz3+nlyGNhwmwJ3vDMG+OzrHMeiZI7gTRWVdUBmfxjZ8Ej23JVYa9VrYeJ5as7XM/ZpulX8NEQis44w53h1qAgnC3PRzM7Zc/D6Ibr0rgUathB6zRHP8PYrfgnNOS9PhSBdHlegK+AGGanfwjXuQ9+0pZcy0w9lQ=="}"""

        signature = '5a65ceeef9aab2d149439f82dc191dd6c5cbe2c0'
        timestamp = '1445827045067'
        nonce = 'nEXhMP4r'

        crypto = DingTalkCrypto(self.token, self.encoding_aes_key, self.suite_key)
        msg = crypto.decrypt_message(jsonstr, signature, timestamp, nonce)
        msg_dict = json.loads(to_text(msg))
        self.assertEqual('check_create_suite_url', msg_dict['EventType'])
        self.assertEqual('LPIdSnlF', msg_dict['Random'])
        self.assertEqual(self.suite_key, msg_dict['TestSuiteKey'])

    def test_decrypt_binary_message(self):
        from dingtalk.core.utils import to_text
        jsonbinary = b"""{"encrypt":"1a3NBxmCFwkCJvfoQ7WhJHB+iX3qHPsc9JbaDznE1i03peOk1LaOQoRz3+nlyGNhwmwJ3vDMG+OzrHMeiZI7gTRWVdUBmfxjZ8Ej23JVYa9VrYeJ5as7XM/ZpulX8NEQis44w53h1qAgnC3PRzM7Zc/D6Ibr0rgUathB6zRHP8PYrfgnNOS9PhSBdHlegK+AGGanfwjXuQ9+0pZcy0w9lQ=="}"""

        signature = '5a65ceeef9aab2d149439f82dc191dd6c5cbe2c0'
        timestamp = '1445827045067'
        nonce = 'nEXhMP4r'

        crypto = DingTalkCrypto(self.token, self.encoding_aes_key, self.suite_key)
        msg = crypto.decrypt_message(jsonbinary, signature, timestamp, nonce)
        msg_dict = json.loads(to_text(msg))
        self.assertEqual('check_create_suite_url', msg_dict['EventType'])
        self.assertEqual('LPIdSnlF', msg_dict['Random'])
        self.assertEqual(self.suite_key, msg_dict['TestSuiteKey'])

    def test_decrypt_encrypt_str(self):
        from dingtalk.core.utils import to_text
        signature = '5a65ceeef9aab2d149439f82dc191dd6c5cbe2c0'
        timestamp = '1445827045067'
        nonce = 'nEXhMP4r'
        encrypt_str = '1a3NBxmCFwkCJvfoQ7WhJHB+iX3qHPsc9JbaDznE1i03peOk1LaOQoRz3+nlyGNhwmwJ3vDMG+OzrHMeiZI7gTRWVdUBmfxjZ8Ej23JVYa9VrYeJ5as7XM/ZpulX8NEQis44w53h1qAgnC3PRzM7Zc/D6Ibr0rgUathB6zRHP8PYrfgnNOS9PhSBdHlegK+AGGanfwjXuQ9+0pZcy0w9lQ=='

        crypto = DingTalkCrypto(self.token, self.encoding_aes_key, self.suite_key)
        msg = crypto.decrypt_encrypt_str(
            signature,
            timestamp,
            nonce,
            encrypt_str
        )
        msg_dict = json.loads(to_text(msg))
        self.assertEqual('check_create_suite_url', msg_dict['EventType'])
        self.assertEqual('LPIdSnlF', msg_dict['Random'])
        self.assertEqual(self.suite_key, msg_dict['TestSuiteKey'])

    def test_decrypt_encrypt_binary(self):
        from dingtalk.core.utils import to_text
        signature = '5a65ceeef9aab2d149439f82dc191dd6c5cbe2c0'
        timestamp = '1445827045067'
        nonce = 'nEXhMP4r'
        encrypt_str = b'1a3NBxmCFwkCJvfoQ7WhJHB+iX3qHPsc9JbaDznE1i03peOk1LaOQoRz3+nlyGNhwmwJ3vDMG+OzrHMeiZI7gTRWVdUBmfxjZ8Ej23JVYa9VrYeJ5as7XM/ZpulX8NEQis44w53h1qAgnC3PRzM7Zc/D6Ibr0rgUathB6zRHP8PYrfgnNOS9PhSBdHlegK+AGGanfwjXuQ9+0pZcy0w9lQ=='

        crypto = DingTalkCrypto(self.token, self.encoding_aes_key, self.suite_key)
        msg = crypto.decrypt_encrypt_str(
            signature,
            timestamp,
            nonce,
            encrypt_str
        )
        msg_dict = json.loads(to_text(msg))
        self.assertEqual('check_create_suite_url', msg_dict['EventType'])
        self.assertEqual('LPIdSnlF', msg_dict['Random'])
        self.assertEqual(self.suite_key, msg_dict['TestSuiteKey'])

    def test_decrypt_encrypt_str_should_fail(self):
        from dingtalk.core.exceptions import InvalidSignatureException
        signature = '5a65ceeef9aab2d149439f82dc191dd6c5cbe2c0'
        timestamp = '1445827045067'
        nonce = 'xxxxx'
        encrypt_str = b'1a3NBxmCFwkCJvfoQ7WhJHB+iX3qHPsc9JbaDznE1i03peOk1LaOQoRz3+nlyGNhwmwJ3vDMG+OzrHMeiZI7gTRWVdUBmfxjZ8Ej23JVYa9VrYeJ5as7XM/ZpulX8NEQis44w53h1qAgnC3PRzM7Zc/D6Ibr0rgUathB6zRHP8PYrfgnNOS9PhSBdHlegK+AGGanfwjXuQ9+0pZcy0w9lQ=='

        crypto = DingTalkCrypto(self.token, self.encoding_aes_key, self.suite_key)

        self.assertRaises(
            InvalidSignatureException,
            crypto.decrypt_encrypt_str,
            signature, timestamp, nonce, encrypt_str
        )
