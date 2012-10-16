=============================
Uliweb App 清单
=============================

uliweb.contrib.auth
---------------------

* 用户认证处理App，提供User Model，及相应的用户认证的处理。

uliweb.contrib.bae
---------------------

* BAE(百度云)支持App。提供对数据连接的配置功能。

uliweb.contrib.cache
---------------------

* 提供cache支持能力。通过::

    functions.get_cache()
    
  来获得cache对象。

详细信息参见 `cache <cache.html>`_

uliweb.contrib.csrf
-----------------------

* 提供CSRF保护机制。

详细信息参见 `csrf <app_csrf.html>`_

uliweb.contrib.dbupload
-------------------------

* 采用数据库来保存上传文件机制

uliweb.contrib.flashmessage
-----------------------------

* 提供静态的flash信息展示功能，它需要使用session来传递信息。

uliweb.contrib.form
------------------------

* 提供form相关的配置信息：

    * ``function.get_form('formname')`` 可以将Form信息配置在settings中，这样可以通过 ``get_form``
      来动态获取
    * 向全局环境中注入 ``validators`` 对象，这样可以直接通过 ``from uliweb import validators``
      来导入。

uliweb.contrib.generic
-------------------------

* 提供generic相关的view类的配置，可以通过 functions 来获取:

    * ListView
    * AddView
    * EditView
    * DeleteView
    * DetailView
    
详情参见 `generic <generic.html>`_

uliweb.contrib.heroku
-------------------------

* 提供heroku部署的支持功能。主要提供数据库配置信息。

详情参见 `Heroku <heroku.html>`_

uliweb.contrib.i18n
-------------------------

* 提供i18n处理相关的配置。

详情参见 `i18n <i18n.html>`_

uliweb.contrib.mail
-------------------------

* 邮件发送配置设置

详情参见 `mail <mail.html>`_

uliweb.contrib.objcache
-------------------------

* 提供对Uliorm中单条对象的缓存处理。

uliweb.contrib.orm
-------------------------

* 提供数据库ORM的配置机制
* 提供ORM相关的命令
* 提供Alembic的支持
* 提供functions.get_model
* 自动提供transcation的Middleware

详情参见 `ORM <orm.html>`_

uliweb.contrib.rbac
-----------------------

* 提供基本的基于角色的用户管理机制

详情参见 `RBAC <app_rbac.html>`_

uliweb.contrib.sae
-----------------------

* 提供SAE支持功能

详情参见 `SAE <sae.html>`_

uliweb.contrib.secretkey(0.1.6)
-----------------------------------

* 提供加，解密功能

uliweb.contrib.session
--------------------------

* 提供session处理功能

详情参见 `session <session.html>`_

uliweb.contrib.soap
-------------------------

* 提供SOAP协议的WEB Service服务

详情参见 `SOAP <app_soap.html>`_

uliweb.contrib.staticfiles
------------------------------

* 提供静态文件支持

详情参见 `staticfiles <app_staticfiles.html>`_

uliweb.contrib.tables
------------------------------

* 为每个Model提供一个ID，根据tablename进行唯一判断，可用在GenericRelation关系处理中。

uliweb.contrib.template
------------------------------

* 提供use, link标签

详情参见 `template <template.html>`_

uliweb.contrib.timezone
------------------------------

* 提供时区初始化处理

uliweb.contrib.upload
-------------------------------

* 提供文件上传处理
* 提供文件上传后文件名转換配置
* 提供文件上传后相关的API

详情参见 `upload <app_upload.html>`_

uliweb.contrib.xmlrpc
-----------------------------

* 提供XMLRPC接入机制

详情参见 `xmlrpc <xmlrpc.html>`_