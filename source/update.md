# Uliweb 更新日志

## 0.1.7

更新内容

* 増加 pretty_dict 函数，可以以缩近的形式打印dict数据结构，主要是为了输出。
* 向functions中添加 encrypt 和 decrypt 函数，需要安装 uliweb.contrib.secretkey APP。这个app是一个des算法的加解密功能模块。缺省使用pyDes模块（它是纯Python的DES算法模块），通过配置可以改为其它的DES算法模块。
* 在命令行find中添加 --tree 参数，可以以缩近形式显示模板的继承和include的调用。
* 优化了alembic的功能，増加了对索引变动的支持。同时向ORM中添加只用于映射的 __mapping_only__ 配置属性，它的作用是将不会和数据库进行同步，只是用来映射数据库中已经存在的表。因为这个特性，所以你可以定义少于数据库中字段的Model。一旦在Model中定义了 __mapping_only__=True，则对于reset, syncdb之类的操作都将无效，在命令行上会看到相应的提示。在alembic中会显示有变化，但是不会真正去处理。同时对于数据库中多，而Model中不存在的情况，缺省的比较会自动忽略，除非在执行alembic时指定了--remove参数，才会生成drop table的语句。它可以用来防止某个项目是对现有数据库的一个不完全映射时的数据库更新，以避免将还在使用的表删除。
* 增加 funtcions.request_url() 函数，可以用来替換request.url，主要是可以正确处理多级反向代理生成URL的处理。 
* 向ORM相关的命令行输出提示中添加Model的计数，可以让用户清楚了解执行的进度。
* 向 functions 中添加 authenticate 函数，方便用户实现自已的用户认证机制。
* uliweb shell 命令行可以传入文件名，则执行效果为启动uliweb项目环境后，执行这个文件，然后停在交互式环境中。
* 向ORM中添加 Lazy 和 Cache 的功能，这样可以实现在获得一个Model对象时，只装入指定的字段，其它的字段如果访问会自动再从数据库中获取。同时提供了 get_object Signal ，可以使用它实现ORM的cache功能。
* 向 uliweb.contrib 中添加redis_cli的APP，使用functions.get_redis()就可以方便获得redis的连接对象。
* 向ORM中添加post_do和rawsql, set_echo, SQLMonitor等功能。rawsql可以用于输出一条sqlalchemy风格的SQL的语句，并且是将相应的参数替換后的结果。set_echo是用于在线程环境下，打开sql输出，可以看到在执行过程中调用的sql语句。直到使用set_echo(False)来关闭这个功能，同时在输出时可以显示执行时间。SQLMonitor也是用来监控SQL执行的，但是它会将类似的SQL统一进行计数，最后显示一个统计结果，如每条SQL的执行次数，时间等。
* 在导出静态文件时，提供对静态文件的合并功能。前提是要在settings.ini中将要合并的css或js进行配置。这样会在导出静态文件时自动将一组的静态文件合并成一个文件。同时在使用use时，可以自动对这种合并后的文件进行处理。
* 在邮件处理中，増加了对sendmail后端的支持。
* 向session的key増加了独立于整个session的失效期的，以key为单位的失效期参数。
* 向ORM中的ManyToMany的ids()函数添加cache参数，用来指示是否将ids()得到的结果进行缓存。
* 升级werkzeug的版本到0.9.1
* 増加一个colorloged.py模块，可以用它来输出带颜然的日志信息。

## 0.1.6

更新内容

* 添加CSRF APP，可以支持CSRF的保护
* 増加在模板中可以使用块注释，可以忽略块内的模板代码
* 优化makeproject生成的项目文件，増加.gitignore和local_settings.ini
* 修复soap View模块中会两次调用__begin__和__end__的bug
* 将functions和decorators机制进行抽象，提供Finder类，可以用它实现functions的机制
* 使用inspect.isclass()来判断一个对象是否class，它可以兼容判断classic class和new style class
* 修复 --version 命令参数的bug
* 优化 import_mod_attr 函数，使其可以接受对象参数（原来只支持字符串路径形式）
* 向 Dispatcher 増加 handler() 方法，可以用它返回的对象来执行：get(), post(), delete()等模拟客户端的RESTFul请求，例如：
    
    ```
    from uliweb import application
 
    handler = application.handler()
    r = handler.get('/index')
    #r is response object
    ```
    
* 向 uliweb/utils/test.py 中添加 client_from_application() 方法
* 向 make_application 和 make_simple_application 函数添加 dispatcher_cls和dispatcher_kwargs参数，可以在创建application时使用不同的Dispatcher类
* 修复在extend同名模板时处理多次的bug
* 添加upload APP中的filename_convert 至FUNCTIONS配置中
* 向utils/common.py中添加 get_uuid() 函数
* 修复 orm 中 get_collection_name() bug
* 修复在进行json处理时，无法处理 0x00-0x1f 的bug
* 添加 generic APP，将常用的几个View类添加至FUNCTIONS中。同时向generic中添加generic命令，可以用它自动生成List, Add, Edit, View, Delete的代码框架。目前已经支持可以生成angularjs, html, easyui三种风格的代码框架。并且在处理Add, Edit, Delete时还可以选择是否采用ajax方式进行处理。其它在通常的开发时，可以先使用generic来生成一个初始的代码版本，然后基于这个版本再进行开发。
* 向BootstrapLayout中添加fieldset支持
* 向DetailView返回的view对象中添加.f属性，可以用它来引用DetailView中的字段
* 修改Form中的IntField生成HTML的Input控件时的类型为Number
* 修改DateTimeField在生成HTML代码时不使用UTC时区
* 修复使用 GET 或 POST在绑定同一个链接时，后者会替換前者的bug
* 修复在ini中使用 u""" 或 u''' 时解析错误的bug
* 在启动时，过滤无模板文件的目录，加快处理效率
* 优化template_plugins中的use模块的定义方式，简单的定义可以直接写在settings.ini中，同时可以支持版本的配置功能
* 修改模板中在处理Python代码缩近时，对return, continue, break的反缩近处理，全部采用判断pass
* 向html.py中添加一个Builder类，使用它可以直接生成包含不同部分的对象，可以对这些部分分别进行处理，最终合成统一的字符串，也可以根据需要分开使用。主要用在HTML代码的生成，允许用户根据需要结合使用或分拆使用
* 向ORM中的get(), filter()等处理添加额外的不定关键字参数，这些参数将在执行select时传递给select方法。目前可以使用它来实现for_update的处理，如：
    
    ```
    Model.get(Model.c.id==id, for_update=True)
    Model.filter(condition).for_update().filter(condition)
    ```
    
* 关于for_update可以参考sqlalchemy相关的文档
* 优化generic.py中的ListView和SimpleListView的处理，可以自动识别request中的page和rows值，当调用时没有传入pageno或rows_per_page参数时生效。
* 添加 secretkey APP，可以用它进行加解密的处理。加密类可以由用户进行配置。纯Python的DES算法实现，可以考虑使用pyDes库。同时提供 uliweb makekey命令，可以自动生成key文件。key文件的路径可以配置到settings.ini中。加解密示例如下：

    ```
    from uliweb import functions
    des = functions.get_cipher()
    d = des.encrypt('hello')
    des.descrypt(d)
    ```
    
* 删除pagecache APP
* 优化 safe_unicode 和 safe_str 函数，可以支持 i18n 的LazyString对象
* 向 commands.py 模块中添加 get_input() 方法 ，可以用来当参数值不存时从命令行获得一个值
* 删除0.1.4中提供的APPS_LAYOUT的机制，但是可以在模板中替換为:

    ```
    {{extend settings.APP_LAYOUTS.get('messages', 'layout.html')}}
    ```
    
    因此仍然可以把要替換的模板配置到settings.ini中。另一种办法是在新的app中直接定义一个要替換的同名模板，以实现新的要求。


## 0.1.5


更新内容


* 修改cache设置，移除file_dir和lock_dir
* 添加更多的dispatch调用异常输出信息
* 添加uliweb.contrib.form app，添加get_form函数
* 修改auth支持get_form功能
* 改进file_storage过程。
* 修正RedirectException显示bug。
* 添加TablenameConvert到uliweb.orm中，通过orm.set_tablename_converter(converter)传递函数，或者在settings.ini中定义，如：

    > [ORM]
    > TABLENAME_CONVERTER = 'uliweb.utils.common.camel_to_'
当Model名字是CamelCase时，将转化为camel_case
* 添加Reference，OneToOne，ManyToMany关系到Model层级
* 如果collection_name为None，并且tablename_set已存在，将自动创建新的collection_name,因此collection_name将会被会复制，如果传递了collection_name，并且tablename_set已经存在，将抛出异常，请注意其中的差别。
* 修改默认CHAR, str， unicode的max_length为255，之前默认为30.
* 在validator.py添加IS_LENGTH_LESSTHAN和IS_LENGTH_BETWEEN。
* 添加[GLOBAL_OBJECTS]机制，此处的对象配置将被注入到uliweb中。
* 在uliweb中添加validator，使用[VALIDATORS]机制
* 在generic.py中添加IS_LENGTH_LESSTHAN，如果max_length存在。


## 0.1.4


功能优化


* 向utils/date増加毫秒格式的支持
* 向SortedDict类添加sort()方法
* 向functions中添加get_var()和set_var()可以用来处理settings.ini，并且可以允许用户覆盖
* 优化soap app，添加多个SOAP服务的支持
* 重构form的生成处理
* 向 uliweb/utils/common.py get_choice() 中新増default参数
* 増强模板extend和include的处理，当某个模板在调用extend和include时，如果被调用的模板和当前模板文件为同一文件时，则会使用更前一个同名但不同目录的文件。可以把同名文件理解为一个栈，但是它们的目录不同。在这种情况下，是使用当前文件位置的前一个文件。这样就可以实现同名模板的继承机制，以前只是取栈底的文件，没有继承的机制。
* 添加APP_LAYOUTS的支持。如果在某个app的模板中使用了{{use template_layout}}，则此处template_layout为一个变量，并且，如果在settings.ini中定应义了对应的值时，如：

    > [APP_LAYOUTS]
    > appname = 'layout.html'
* 如果当前app的名字在APP_LAYOUTS中有定义，则使用配置的模板名。它的功能是可以将app级的layout模板进行配置化，不必hardcode。如果没定义，则缺省使用layout.html模板。
* 向common.py中添加QueryString(类)和query_string(函数)的支持，用来方便处理query_string
* 重构manage.py，添加call()方法 ，可以通过调用方式来执行uliweb的命令
* 向cache.get()中添加createor参数，它可以当key不存在时调用creator方法来生成value，并保存到cache中。同时value值可以为callable()对象。
* 添加cache和session对memcache的后端存储的支持，添加inc()和dec()方法。
* 调整了require_login的处理代码
* 修改Redirect由原来的异常类改为函数，原来的异常类改为RedirectException。与redirect()的区别是，Redirect()将直接抛出异常。而redirect()返回一个response对象。


问题修复


* 修复rules.py在处理定义在settings.ini中的class based view函数的bug, 并且修复app URL定义对相对url处理的bug
* 修复dispatch signal的bug
* 设置werkzeug的日志级为为info
* wsgi_staticfiles的静态文件的处理顺序进行了倒序处理
* 修复log格式串的bug

