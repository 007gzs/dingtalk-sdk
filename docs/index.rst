.. dingtalk-sdk documentation master file, created by
   sphinx-quickstart on Fri May  4 11:18:22 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dingtalk-sdk 使用文档
========================================

dingtalk-sdk 是一个钉钉开放平台的第三方 Python SDK, 实现了 企业内部开发 和 应用服务商（ISV）的 API。

快速入门
-------------

.. toctree::
   :maxdepth: 2

   install


企业内部开发
--------------------
建议在使用前先阅读 `钉钉开放平台文档 <https://open-doc.dingtalk.com>`_ 

.. toctree::
   :glob:
   :maxdepth: 2

   model/message
   model/field
   client/index

应用服务商（ISV）
----------------------------
.. toctree::
   :glob:
   :maxdepth: 2

   client/isv

未实现接口
--------------------
由于钉钉接口过多，文档较分散，有未实现的接口可以提交 Issues, sdk未更新时候可根据下面代码临时使用
post/get接口中的access_token,top接口中的session会在请求时自动设置，无需手动添加

.. module:: dingtalk.client.base

.. autoclass:: BaseClient

   .. automethod:: get
   .. automethod:: post
   .. automethod:: top_request

调用示例::

   client = SecretClient('CORP_ID', 'CORP_SECRET')

   # top 接口： 获取考勤组列表详情
   ret = client._top_request(
      'dingtalk.smartwork.attends.getsimplegroups',
      {
          "offset": 0,
          "size": 10
      }
   )
   has_more = ret.result.has_more
   groups = ret.result.groups


   # get 接口：获取子部门ID列表
   ret = client.get(
      '/department/list_ids',
      {'id': 0}
   )
   sub_dept_id_list = ret.sub_dept_id_list


   # post 接口：创建会话
   return self._post(
      '/chat/create',
      {
          'name': "群名称",
          'owner': "zhangsan",
          'useridlist': ["zhangsan", "lisi"]
      }
   )
   chatid = ret.chatid


示例项目
---------------------

`django demo <https://github.com/007gzs/dingtalk-django-example/>`_


Changelogs
---------------

.. toctree::
   :maxdepth: 1

   changelog

