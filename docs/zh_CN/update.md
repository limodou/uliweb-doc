# Uliweb 更新日志

## 0.2.3

* 更新nginx配置文件的输出模板，添加 proxy_set_header 指令
* 向 ORM 添加 save_file() 方法，你可以用它保存select之后的结果集到一个csv文件中
* 修复 SortedDict 类中丢失的 clear() 方法
* 修改i18n处理，对于项目和apps方式的抽取，它将首先启动应用，这样是为了让自定义tag可以起作用。但是建议用户尽量不用自定义tag，因为模板中可以直接写python代码。
* 向utils/common.py中添加walk_dirs()方法，这个函数可以用来遍历目录，同时可以支持对文件名和后缀的过滤功能。

## 0.2.2

* 向 `SortedDict` 添加 `clear()` 函数
* 向 AddView, EditView 添加提交保护，缺省为不启动。它可以用来防止多次提交。但对于
  前端建议再増加相关的措施，比如在提交时将按钮禁掉。如果想要其生效，需要传入 `protect=True` 参数。
* 向 uliweb find -t 命令添加 `--blocks` 和 `--with-filename` 参数，前者用来显示在
  模板中定义的块信息，后者用来列出定义相应块所在的模板文件名。同时向settings.ini
  中添加 GLOBAL/DEBUG_TEMPLATE 配置项，用来控制模板是否显示调试用的注释，用来区分
  不同的块的开始和结束。但是这种输出具有一定的破坏性，比如非HTML的结果等。所以只
  能用于调试，正式使用一定要关闭。比如，打开之后，在输出的模板中可能有：

    ```
    <!-- BLOCK title (apps/theme/templates/theme/skeleton.html) -->
    <!-- END title -->
    ```
    
* 増加filedown.py在下载时对 `content-range` 的处理，感谢 zhangchunlin 提供代码。
* 改进 `import_attr()` 的处理，増加对 pkg_resource 入口字符串格式的支持，比如： 
  `x.y.z` 原来是根据从左向右逐层导入时，动态来判断后面的是模块还是属性，如果是
  模块，则继续导入，如果是属性则使用 `getattr()` 来处理。现在则可以定义为： `x.y:z.c`,
  这样可以更清晰表示 `:` 号前是模块，后面是属性。
* 向 `uliweb.contrib.orm` 上添加 requirements.txt，可以直接用 uliweb install
  来安装: SQLAlchemy, MySQL-python, alembic(这个是我修改的版本)。注意，要在你的应
  中用先配置 `uliweb.contrib.orm` 才可以。因为这个requirements.txt是在app上定义的。
* 添加　LOGO 文件，可以用这里面的图片来展示 uliweb。
* 向 runserver 命令増加 `--color` 参数，可以输出彩色日志。输省是不输出。同时，你
  可以根据需要，在settings.ini中对颜色进行配置，如缺省的为：

    ```
    [LOG.COLORS]
    DEBUG = 'white'
    INFO = 'green'
    WARNING = 'yellow'
    ERROR = 'red'
    CRITICAL = 'red'
    ```
    
    支持的颜色为: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE.
    
* 増加 `config` 命令。它可以用来向控制台输出配置文件的模板。目前可以生成 nginx, supervisor
  相关的配置。你也可以在自已的app中定义这样的输出。只要在app下创建 `template_files/config`
  的目录结构，然后创建 `xxxx.conf` 和 `xxxx.ini` 文件。在 `xxxx.ini` 中用来定义一些
  变量，这些变量将用于 `xxxx.conf` 中。

    ini格式定义示例为：
    
    ```
    [INPUT]
    port = '', 80
    path =
    ```
    
    port为变量名，值为一个tuple或者不定义，第一个值为提示用的文本，如果为空则表示没有额外
    说明。第二个表示缺省值。
    
    xxxx.conf 为uliweb格式的模板，如果存在模板变量，则需要与ini中的一致。同时
    有一些预定义的变量，如: project 表示项目目录名称，project_dir 表示项目目录。
    
    执行时可以： `uliweb config xxxx`

* 优化 `support` 命令，可以象config命令一样，在你的app下创建 `template_files/support/xxxx`
  这样的目录结构，下面放执行 `uliweb support xxxx` 时将要拷贝的文件及目录即可。
* 修复 tmplate 中normcase的bug，改为 normpath 。
* 重构ORM的关系字段的处理，让关系的处理为延迟执行（待get_model时才执行）。这样
  是为了解决存在循环引用的问题，但是带来可能的不兼容问题，就是反向关系的获取。
  如果A和B都是在一个文件中定义，那么在导入A时，B自然也被引入，如果B上有对A的关
  系定义，则A自动被注入一个反向关系。但是现在则要显示执行 get_model('B')才可以
  创建反向关系。
* `get_model()` 和 `set_model()` 中的Model名不再区分大小写。
* 修复当重名的URL定义存在时，后定义的没有替換前面定义的URL的bug。
* 修复 rbac 中没有使用 `functions.has_role()` 和 `functions.has_permission()` 的bug。
* 修复rules.py在处理View类继承时的bug。添加 `expose(replace=True)` 的支持，用来实
  现View类的替換方式，即不会増加新的一套URL，而是为了修改原来的View方法处理。
  如果replace=False,或不写，则为普通的派生方式.
* 向expose()増加template参数，这样除了可以在view函数中指定 `response.tmplate = 'xxxx.html` 外
  还可以直接在expose上指定。执行优先级，以response.template最高。
* 恢复 ORM 配置中关于 `NULLABLE = False` 的配置。这样字段缺省允许为 null。

## 0.2.1

* 添加 `uliweb.utils.timeit` 模块，用户可以使用 `with timeit(prompt):` 来计算下面
  代码的执行时间
* 修改 `file_serving()` 处理的 `action` 缺省值为 `None`. 这样缺省的 `/uploads` 文件
  服务不再是默认为下载。
* 修复ORM的Reference的validate问题。它影响Reference的默认缺省值。

## 0.2

更新内容

* 修复 auth.models `get_href` 错误
* 修改 ORM `save()` 处理，它将保存manytomany数据
* 向 `save()` 中添加 `changed`, `saved` 和 `send_dispatch` 参数。其中 `changed`
  是一个回调函数，当有更新时（不是新増)时被调用。 `saved` 也是一个回调，当保存
  了数据时被回调，它包括更新和新増两种情况。 `send_dispatch` 表示是否发送pre_save和
  post_save信号。
* 改进 `set_echo()`, 添加 `time`, `explain`, `caller` 等参数。
* 向 utils.common 模块添加 `get_caller()` 函数。
* 向 form 模块添加 `CheckboxSelectField` 字段类。
* 添加 `jsonp` 函数，使用方式如json。
* 修复rule合并错误。
* 优化 `get_redis(**options)` 允许传入参数。
* 优化 `jsonp()` 限制 `callback` 参数只能传入字母和数字。
* 优化 pyini, 支持跨section变量引用和延迟处理。
* 优化 `load` 命令，添加总条数和花费时间显示，同时在插入时采用批量插入。
* 向 uliweb/utils/image.py 添加 `test_image` 函数。
* 添加 `xhr_redirect_json` 支持. 在启动uliewb应用时，可以传入 `xhr_redirect_json` (布尔值) 参数，
  缺省值是 `True` 。它的作用是，如果请求是ajax，重定向将返回为一个json结果，错
  误码是 500。所以前端可以使用它来根据需要进行重定向。
* ORM `remove/clear` 函数在传入空条件时将删除全部记录。
* 向 uliweb.utils.common 中添加 `classonlymethod()` 方法, 它和classmethod类似，
  但是它可以限制类属性只能通过类来调用，而不是实例。主要用来控制ORM的Model delete 方法 。
* 重构上传App，添加 `download` 到 functions 配置。
* 优化 secretkey app, 添加 `-o` 来指定输出文件名。向大部分加解密函数添加 `keyfile` 参数。
* 向upload App添加 `MIME_TYPES` section，但是它只会对uliweb应用有效，而不是对web server。
* 优化 `call` 命令，允许调用在apps目录之外的模块，添加project目录到 `sys.path` 中。
* 修复 ORM PICKLE 更新错误, 使用 `deepcopy` 来保存 old_value。
* 添加 tornado 服务器支持。
* 添加 gevent 和 gevent-socketio 服务器支持。
* 添加 `install` 命令支持，你可以在项目目录或app目录下写 `requirements.txt`。
* 在执行 `makeproject` 时添加 `setup.py` 文件。
* `make_application()` 可以重入。
* 添加 `ORM/MODELS_CONFIG` 配置支持。

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
* 増加一个colorloged.py模块，可以用它来输出带颜色的日志信息。

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

