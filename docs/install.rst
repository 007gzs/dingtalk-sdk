安装与升级
==========

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

如果需要安装 GitHub 上的最新代码::

    pip install https://github.com/007gzs/dingtalk-sdk/archive/master.zip

