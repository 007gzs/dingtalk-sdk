# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from Crypto.Cipher import AES


class DingTalkCipher(object):

    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_CBC, key[:16])

    def encrypt(self, plaintext):
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext)
