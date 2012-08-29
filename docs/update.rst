=================
更新日志
=================

0.1.5
===========

更改内容：
-------------
    
    * 修改cache设置，移除file_dir和lock_dir
    * 添加更多的dispatch调用异常输出信息
    * 添加uliweb.contrib.form app，添加get_form函数
    * 修改auth支持get_form功能
    * 改进file_storage过程。
    * 修正RedirectException显示bug。
    * 添加TablenameConvert到uliweb.orm中，通过orm.set_tablename_converter(converter)传递函数，或者在settings.ini中定义，如：
    
    .. code-block:: python
           :linenos:
           :emphasize-lines: 3,5

            [ORM]
            TABLENAME_CONVERTER = 'uliweb.utils.common.camel_to_'
    
当Model名字是CamelCase时，将转化为camel_case
    
    * 添加Reference，OneToOne，ManyToMany关系到Model层级
    * 如果collection_name为None，并且tablename_set已存在，将自动创建新的collection_name,因此collection_name将会被会复制，如果传递了collection_name，并且tablename_set已经存在，将抛出异常，请注意其中的差别。
    * 修改默认CHAR, str， unicode的max_length为255，之前默认为30.
    * 在validator.py添加IS_LENGTH_LESSTHAN和IS_LENGTH_BETWEEN。
    * 添加[GLOBAL_OBJECTS]机制，此处的对象配置将被注入到uliweb中。
    * 在uliweb中添加validator，使用[VALIDATORS]机制
    * 在generic.py中添加IS_LENGTH_LESSTHAN，如果max_length存在。
    

0.1.4
===========

功能优化：
-------------

    * 向utils/date増加毫秒格式的支持
    * 向SortedDict类添加sort()方法
    * 向functions中添加get_var()和set_var()可以用来处理settings.ini，并且可以允许用户覆盖
    * 优化soap app，添加多个SOAP服务的支持
    * 重构form的生成处理
    * 向 uliweb/utils/common.py get_choice() 中新増default参数
    * 増强模板extend和include的处理，当某个模板在调用extend和include时，如果被调用的模板和当前模板文件为同一文件时，则会使用更前一个同名但不同目录的文件。可以把同名文件理解为一个栈，但是它们的目录不同。在这种情况下，是使用当前文件位置的前一个文件。这样就可以实现同名模板的继承机制，以前只是取栈底的文件，没有继承的机制。
    * 添加APP_LAYOUTS的支持。如果在某个app的模板中使用了{{use template_layout}}，则此处template_layout为一个变量，并且，如果在settings.ini中定应义了对应的值时，如：

    .. code-block:: python
       :linenos:
       :emphasize-lines: 3,5

        [APP_LAYOUTS]
        appname = 'layout.html'
    

    * 如果当前app的名字在APP_LAYOUTS中有定义，则使用配置的模板名。它的功能是可以将app级的layout模板进行配置化，不必hardcode。如果没定义，则缺省使用layout.html模板。
    * 向common.py中添加QueryString(类)和query_string(函数)的支持，用来方便处理query_string
    * 重构manage.py，添加call()方法 ，可以通过调用方式来执行uliweb的命令
    * 向cache.get()中添加createor参数，它可以当key不存在时调用creator方法来生成value，并保存到cache中。同时value值可以为callable()对象。
    * 添加cache和session对memcache的后端存储的支持，添加inc()和dec()方法。
    * 调整了require_login的处理代码
    * 修改Redirect由原来的异常类改为函数，原来的异常类改为RedirectException。与redirect()的区别是，Redirect()将直接抛出异常。而redirect()返回一个response对象。

问题修复：
----------------

    * 修复rules.py在处理定义在settings.ini中的class based view函数的bug, 并且修复app URL定义对相对url处理的bug
    * 修复dispatch signal的bug
    * 设置werkzeug的日志级为为info
    * wsgi_staticfiles的静态文件的处理顺序进行了倒序处理
    * 修复log格式串的bug



