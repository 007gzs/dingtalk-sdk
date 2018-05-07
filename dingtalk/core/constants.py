# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from enum import Enum


class SuitePushType(Enum):
    """套件相关回调枚举"""
    CHECK_URL = "check_url"  # 校验url
    CHANGE_AUTH = "change_auth"  # 授权变更
    SUITE_TICKET = "suite_ticket"  # 套件ticket
    TMP_AUTH_CODE = "tmp_auth_code"  # 临时授权码
    SUITE_RELIEVE = "suite_relieve"  # 解除授权
    CHECK_CREATE_SUITE_URL = "check_create_suite_url"  # 校验创建套件时候的url
    CHECK_UPDATE_SUITE_URL = "check_update_suite_url"  # 校验更改套件时候的url
    CHECK_SUITE_LICENSE_CODE = "check_suite_license_code"  # 校验序列号
    MARKET_BUY = "market_buy"  # 用户购买下单
    ORG_MICRO_APP_STOP = "org_micro_app_stop"  # 企业逻辑停用微应用
    ORG_MICRO_APP_REMOVE = "org_micro_app_remove"  # 企业物理删除微应用
    ORG_MICRO_APP_RESTORE = "org_micro_app_restore"  # 企业逻辑启用微应用
