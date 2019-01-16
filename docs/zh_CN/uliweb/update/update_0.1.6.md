# 0.1.6

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