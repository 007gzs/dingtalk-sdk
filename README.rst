#######################
DingTalk Sdk for Python
#######################
.. image:: https://travis-ci.org/007gzs/dingtalk-sdk.svg?branch=master
       :target: https://travis-ci.org/007gzs/dingtalk-sdk
.. image:: https://img.shields.io/pypi/v/dingtalk-sdk.svg
       :target: https://pypi.org/project/dingtalk-sdk

钉钉开放平台第三方 Python SDK。
`【阅读文档】 <http://dingtalk-sdk.readthedocs.io/zh_CN/latest/>`_。

********
功能特性
********
+ 企业内部开发接入api
+ 应用服务商（ISV）接入api

********
安装
********

目前 dingtalk-sdk 支持的 Python 环境有 2.7, 3.4, 3.5, 3.6 和 pypy。

dingtalk-sdk 消息加解密同时兼容 cryptography 和 PyCrypto, 优先使用 cryptography 库。
可先自行安装 cryptography 或者 PyCrypto 库::

    # 安装 cryptography
    pip install cryptography>=0.8.2
    # 或者安装 PyCrypto
    pip install pycrypto>=2.6.1

为了简化安装过程，推荐使用 pip 进行安装

.. code-block:: bash

    pip install dingtalk-sdk
    # with cryptography
    pip install dingtalk-sdk[cryptography]
    # with pycrypto
    pip install dingtalk-sdk[pycrypto]

升级 dingtalk-sdk 到新版本::

    pip install -U dingtalk-sdk

****************
使用示例
****************

django 示例 https://github.com/007gzs/dingtalk-django-example
