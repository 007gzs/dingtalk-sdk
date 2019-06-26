钉钉企业内部开发接口
===========================================

.. module:: dingtalk.client

.. autoclass:: DingTalkClient
   :members:
   :inherited-members:

`DingTalkClient` 基本使用方法::

   from dingtalk import SecretClient, AppKeyClient

   client = SecretClient('corp_id', 'secret')  # 旧 access_token 获取方式
   client = AppKeyClient('corp_id', 'app_key', 'app_secret')  # 新 access_token 获取方式

   user = client.user.get('userid')
   departments = client.department.list()
   # 以此类推，参见下面的 API 说明
   # client.chat.xxx()
   # client.role.xxx()

如果不提供 ``storage`` 参数，默认使用 ``dingtalk.storage.memorystorage.MemoryStorage`` 类型，
注意该类型不是线程安全的，而且非持久化保存，不推荐生产环境使用。

.. toctree::
   :maxdepth: 2
   :glob:

   api/*

