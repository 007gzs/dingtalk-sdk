钉钉应用服务商（ISV）接口
===========================================

.. module:: dingtalk.client.isv

.. autoclass:: ISVClient
   :members:
   :inherited-members:

`ISVClient` 基本使用方法::

   from dingtalk import ISVClient

   client = ISVClient('corp_id', 'secret', 'token', 'aes_key')
   corp_info = client.get_auth_info('corpid')

   corp_client = client.get_dingtalk_client('corpid')
   user = corp_client.user.get('userid')
   departments = corp_client.department.list()
   # 以此类推，corp_client可针对企业执行api

.. toctree::
   :maxdepth: 1
   :glob:

   index


如果不提供 ``storage`` 参数，默认使用 ``dingtalk.storage.memorystorage.MemoryStorage`` 类型，
注意该类型不是线程安全的，而且非持久化保存，不推荐生产环境使用。

