# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
import base64
import json

from dingtalk.core.exceptions import InvalidSignatureException, InvalidCorpIdOrSuiteKeyException
from dingtalk.core.utils import to_text, to_binary, DingTalkSigner, random_string

from dingtalk.crypto.base import BasePrpCrypto


def _get_signature(token, timestamp, nonce, encrypt):
    signer = DingTalkSigner()
    signer.add_data(token, timestamp, nonce, encrypt)
    return signer.signature


class PrpCrypto(BasePrpCrypto):

    def encrypt(self, text, _id):
        return self._encrypt(text, _id)

    def decrypt(self, text, _id):
        return self._decrypt(text, _id, InvalidCorpIdOrSuiteKeyException)


class BaseDingTalkCrypto(object):

    def __init__(self, token, encoding_aes_key, _id):
        if encoding_aes_key:
            encoding_aes_key = to_binary(encoding_aes_key + '=')
            self.key = base64.b64decode(encoding_aes_key)
            assert len(self.key) == 32
        else:
            self.key = None
        self.token = token
        self._id = _id

    def _decrypt_encrypt_str(self,
                             signature,
                             timestamp,
                             nonce,
                             encrypt_str,
                             crypto_class=None):

        _signature = _get_signature(self.token, timestamp, nonce, encrypt_str)
        if _signature != signature:
            raise InvalidSignatureException()
        assert self.key is not None
        pc = crypto_class(self.key)
        return pc.decrypt(encrypt_str, self._id)

    def _encrypt_message(self,
                         msg,
                         nonce=None,
                         timestamp=None,
                         crypto_class=None):

        timestamp = timestamp or int(time.time() * 1000)
        timestamp = to_text(timestamp)
        if nonce is None:
            nonce = random_string()
        assert self.key is not None
        pc = crypto_class(self.key)
        encrypt = to_text(pc.encrypt(msg, self._id))
        signature = _get_signature(self.token, timestamp, nonce, encrypt)
        result = dict()
        result['msg_signature'] = signature
        result['encrypt'] = encrypt
        result['timeStamp'] = timestamp
        result['nonce'] = nonce
        return result

    def _decrypt_message(self,
                         msg,
                         signature,
                         timestamp,
                         nonce,
                         crypto_class=None):
        if not isinstance(msg, dict):
            msg = json.loads(to_text(msg))
        encrypt = msg['encrypt']
        return self._decrypt_encrypt_str(signature, timestamp, nonce, encrypt, crypto_class)


class DingTalkCrypto(BaseDingTalkCrypto):

    def __init__(self, token, encoding_aes_key, corpid_or_suitekey):
        super(DingTalkCrypto, self).__init__(token, encoding_aes_key, corpid_or_suitekey)

    def decrypt_encrypt_str(self, signature, timestamp, nonce, encrypt_str):
        return self._decrypt_encrypt_str(signature, timestamp, nonce, encrypt_str, PrpCrypto)

    def encrypt_message(self, msg, nonce=None, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp, PrpCrypto)

    def decrypt_message(self, msg, signature, timestamp, nonce):
        return self._decrypt_message(
            msg,
            signature,
            timestamp,
            nonce,
            PrpCrypto
        )
