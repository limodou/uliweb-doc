# 0.5 2016-1-21

## 问题修复

* 修复 flashmessage 的配置 BUG
* 修复 gitignore 模板
* 修复 setup.py 模板

## 功能优化

* `json` 函数增加对content_type的默认处理.当请求头中的 `Accept` 为 `'*/*'` 时, content_type
  值为 `application/json`,当 `Accept` 的值中不含有 `application/json` 时, 则值为 `text/plain`,
  否则为 `application/json`
* 向 `Dispatcher` 中添加 `parse_tag_xml` 及 `parse_tag` 方法,用于方便处理taglib.前者用于解析
  tag为数据结构,后者则将tag处理为HTML代码.
* `support` 命令中删除掉不再支持的配置,如: bae, dotcloud, gae, fcgi等.
* 添加 `exportconfigjs` 命令. 用于配合 `uliweb-ui` 项目,可以根据 `ui_modules.js` 生成需要的 config.js
  用在 requirejs 中.
* 增加 `reflect_table()`, `reflect_table_data()`, `reflect_table_model` 函数用于将数据库
  反射为Model或数据结构.


# 0.5b 2015-12-27

## 问题修复

* 修复pyini重入的BUG
* 修复在执行 `set_password` 时自动执行 `save` 的BUG,改为不执行
* 修复 `Content-Range` 头处理不正确的BUG, 感谢 zhangchunlin 的支持
* 修复 `StaticFilesMiddleware` 中的URL没有使用 `settings.DOMAINS` 的配置的BUG, 感谢 zhangchunlin 的贡献
* 修复 form 中传入 `BooleanField` 值为 `None` 时未转为 `False` 的BUG, 感谢 zhangchunlin 的贡献
* 修复 pretty_dict 在处理unicode出错的BUG


## 普通功能优化

* `SortedDict` 重构,以dict作为父类,并且支持传入初始化值.
* 增加 `Dispatcher` 和 `make_application` `reset` 参数,可以用来决定是每次执行创建新的application
  对象还是可以重用上次的对象.主要用在测试中,以便可以重用.
* 增加按某个前缀对 redis 中的keys进行统计的函数 `count_prefix(prefix)`
* 在 `uliweb.utils.common` 中添加获得临时文件的函数 `get_tempfilename(prefix, dir='')`
* 修改 APP_URL 的定义形式为 `{'prefix':''}` ,只能是字典形式.增加 `URL_ROUTE` 的映射支持:

    ```
    [URL_ROUTE]
    any_key_1 = ('mapping_str', 'replacement')
    any_key_2 = ('mapping_str', 'replacement')
    ```

    可以把某个 URL 替换为指定值.如: `('/admin', '/demo')`

* 增加 pyini 在处理时,可以传入字典形式的初始化数据,如 `x = Ini({'DEFAULT':{'x':1}})`
* 增加对带路径的对象的配置项的导入处理,通过 `uliweb.utils.common` 中新增 `get_configrable_object(key, section, cls=None)`
  函数.对于象 `key=path.to.model.function` ,可以自动根据路径导入后面的对象.
* 重构Form的校验功能,增加Form中的 `rules` 配置,方便前面实现前端校验处理
* mail 支持 cc 转发参数, 感谢 zhangchunlin 的贡献
* `uliweb runserver` 增加对运行单个 app 的支持.
* 当返回一个generator时,可以通过 `response.content_type` 来设定上下文类型.
* 在utils目录下增加 `workers.py` 用于方便生成带管理的父子进程调度处理. [查看](../utils/workers.html)
* 向 `utils/date.py` 中添加 `parse_time` 函数,可以解析 `1h, 5s` 之类的时间格式
* `ListView` 中增加 `group_by` 和 `having` 的参数支持
* 在 `uliweb.contrib.generic` 中添加 `MultiView` 的支持,它提供了对 `ListView`, `AddView`, `EditView`
  等的集成.
* `url_for` 增加 `_format=True` 参数,可以将URL生成为参数形式,如对于 `expose('/view/<name>/<int:value>')`
  的URL的定义,使用 `url_for(endpoint, _format=True)` 生成结果为 `'/view/{name}/{value}'`
* 增加 `format_size()` 函数,用于将数值转为大小描述,如 `format_size(1026)` 结果为 `2KB`
* 集成 `xltools.py` 模块,用于对Excel的处理.需要安装 `openpyxl` 模块. [查看](http://github.com/limodou/xltools)
* 增加模板中对tag库的支持. [查看](../taglibs.html)
* 去除对 `head.js` 的支持
* 向 application 添加 `get_config()` 用来读取其它的 ini 配置文件.和settings.ini类似,会自动
  对所有生效的app下的配置文件进行合并处理.
* 向 `uliweb.contrib.auth` 中 `User` 表中添加 `auth_type` 字段,将用于区分用户登录使用的方法.感谢 zhangchunlin 的贡献


## 命令行变化
* 增加 uliweb 命令中传入环境变量的参数支持,通过 `-Ea=b` 的形式,可以传多个.
* `uliweb find -u url` 增加显示view函数的docstring的功能.
* 增加 `uliweb find -U url_pattern` 命令,可以显示带通配符的URL,如: `uliweb find -U "blog*"`.
  注意,模式对于 `*` 要添加双引号.
* 增加ipython的支持,可以在启动 `uliweb shell` 时自动检测是否安装了ipython.如果使用 `uliweb shell -n`
  可以启动 jupyter notebook.提供对uliweb的扩展,执行 `%load_ext uliweb` 就会自动将 `application`,
  `functions`, `settings` 注入到环境中.并且,可以对Model的类和实例查看相应的内容.类则可以看到建表语句及
  表之间的关系图(需要安装graphviz).实例可以看到表结构对应的值.
* 重构recorder命令
* 增加 `relectdb` 命令,用于反向从数据库生成 `models.py` 文件
* 增加 `uliweb makemodule` 命令,可以快速生成uliweb第三方模块的目录结构,要求以 `uliweb-` 开头,
  但生成的模块名是 `uliweb_`

## ORM 变化
* 重构rawsql对postgresql的支持
* 增强 `OneToOne` 的处理.修复结果不被缓存的bug.并且当访问 `OneToOne` 对象时,如果不存在,则会自动创建空对
  象.并且当记录删除时,会自动将联带的 `OneToOne` 对象删除.
* 增加动态创建Model的支持.可以根据配置信息自动生成新的Model.提供 `create_model` 方法.
* 增加Model的移迁的支持.提供migrate方法,可以在运行时升级数据库.
* 向 `Property` 中添加 `to_column_info()` 函数和向 `Model` 添加 `get_columns_info()` 函数可以方便
  获得Property或Model的字段详细信息.
* 添加:UUID, UUID_B, SMALLINT, BINARY, VARBINARY, JSON字段类型
* 增加 `ORMResetMiddle` 中间件,可以对某些全局变量进行重置,如:set_echo的状态, signal发布状态
* 向session中增加post_commit和post_commit_once回调,可以在提交事务后执行.
* 增加 `relectdb` 命令,用于反向从数据库生成 `models.py` 文件
* 增加除ID外,可以自定义主键的功能.


## APP变化

* 增加 `model_config` APP.用来实现Model动态迁移的支持
* 增加 `celery` 的支持
* 增加 `datadict` 功能,用来处理数据字典
* 删除不用的APP:
    * bae 百度app engine的支持
    * dbupload 使用数据库来保存上传文件
    * heroku heroku的支持
    * sae 新浪app engine的支持
    * xmlrpc

## 不再内置的模块

* pysimplesoap



