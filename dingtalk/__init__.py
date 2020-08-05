from __future__ import absolute_import, unicode_literals

import logging

from dingtalk.client import SecretClient, AppKeyClient  # NOQA
from dingtalk.client.isv import ISVClient  # NOQA
from dingtalk.core.exceptions import DingTalkClientException, DingTalkException  # NOQA

__version__ = '1.3.8'
__author__ = '007gzs'

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
