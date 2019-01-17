# Uliweb App 清单


## uliweb.contrib.auth


* 用户认证处理App，提供User Model，及相应的用户认证的处理。


## uliweb.contrib.cache


* 提供cache支持能力。通过:

    ```
    functions.get_cache()
    ```

来获得cache对象。

详细信息参见 [cache](cache.html)


## uliweb.contrib.csrf


* 提供CSRF保护机制。

详细信息参见 [csrf](app_csrf.html)


## uliweb.contrib.flashmessage


* 提供静态的flash信息展示功能，它需要使用session来传递信息。


## uliweb.contrib.form


* 提供form相关的配置信息：

    * `function.get_form('formname')` 可以将Form信息配置在settings中，这样可以通过 `get_form`
        来动态获取
    * 向全局环境中注入 `validators` 对象，这样可以直接通过 `from uliweb import validators`
        来导入。



## uliweb.contrib.generic


* 提供generic相关的view类的配置，可以通过 functions 来获取:

    * ListView
    * AddView
    * EditView
    * DeleteView
    * DetailView


详情参见 [generic](generic.html)


## uliweb.contrib.i18n


* 提供i18n处理相关的配置。

详情参见 [i18n](i18n.html)


## uliweb.contrib.mail


* 邮件发送配置设置

详情参见 [mail](mail.html)


## uliweb.contrib.orm


* 提供数据库ORM的配置机制
* 提供ORM相关的命令
* 提供Alembic的支持
* 提供functions.get_model
* 自动提供transcation的Middleware

详情参见 [ORM](orm.html)


## uliweb.contrib.rbac


* 提供基本的基于角色的用户管理机制

详情参见 [RBAC](app_rbac.html)


## uliweb.contrib.secretkey(0.1.6)


* 提供加，解密功能


## uliweb.contrib.session


* 提供session处理功能

详情参见 [session](session.html)


## uliweb.contrib.staticfiles


* 提供静态文件支持

详情参见 [staticfiles](app_staticfiles.html)


## uliweb.contrib.tables


* 为每个Model提供一个ID，根据tablename进行唯一判断，可用在GenericRelation关系处理中。


## uliweb.contrib.template


* 提供use, link标签

详情参见 [template](template.html)


## uliweb.contrib.timezone


* 提供时区初始化处理


## uliweb.contrib.upload


* 提供文件上传处理
* 提供文件上传后文件名转換配置
* 提供文件上传后相关的API

详情参见 [upload](app_upload.html)

