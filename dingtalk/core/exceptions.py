# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from dingtalk.core.utils import to_binary, to_text


class DingTalkException(Exception):

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        _repr = 'Error code: {code}, message: {msg}'.format(
            code=self.errcode,
            msg=self.errmsg
        )

        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def __repr__(self):
        _repr = '{klass}({code}, {msg})'.format(
            klass=self.__class__.__name__,
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


class DingTalkClientException(DingTalkException):
    """WeChat API client exception class"""
    def __init__(self, errcode, errmsg, client=None,
                 request=None, response=None):
        super(DingTalkClientException, self).__init__(errcode, errmsg)
        self.client = client
        self.request = request
        self.response = response


class InvalidSignatureException(DingTalkException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class InvalidCorpIdOrSuiteKeyException(DingTalkException):
    """Invalid app_id exception class"""

    def __init__(self, errcode=-40005, errmsg='Invalid CorpIdOrSuiteKey'):
        super(InvalidCorpIdOrSuiteKeyException, self).__init__(errcode, errmsg)
