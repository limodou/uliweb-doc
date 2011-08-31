=====================
命令行工具使用指南
=====================

uliweb
---------

当运行不带参数的uliweb命令时，会显示一个帮助信息，但是因为命令很多，所以这个帮
助只是列出可用命令的清单，如::

    Usage: uliweb [global_options] [subcommand [options] [args]]
    
    Global Options:
      --help                show this help message and exit.
      -v, --verbose         Output the result in verbose mode.
      -s SETTINGS, --settings=SETTINGS
                            Settings file name. Default is "settings.ini".
      -L LOCAL_SETTINGS, --local_settings=LOCAL_SETTINGS
                            Local settings file name. Default is
                            "local_settings.ini".
      --project=PROJECT     Project "apps" directory.
      --pythonpath=PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/myproject".
      --version             show program's version number and exit
    
    Type 'uliweb help <subcommand>' for help on a specific subcommand.
    
    Available subcommands:
      call
      develop
      exportstatic
      i18n
      makeapp
      makepkg
      makeproject
      runserver
      shell
      support

在uliweb中，有一些是全局性的命令，有一些是由某个app提供的命令。因此当你在一个
project目录下运行uliweb命令时，它会根据当前project所安装的app来显示一个完整的
命令清单。上面的示例只显示了在没有任何项目时的全局命令。比如你安装了orm app，则
可能显示的清单为::

    Available subcommands:
      call
      createsuperuser
      dbinit
      develop
      droptable
      dump
      dumptable
      dumptablefile
      exportstatic
      i18n
      load
      loadtable
      loadtablefile
      makeapp
      makepkg
      makeproject
      reset
      resettable
      runserver
      shell
      sql
      sqldot
      support
      syncdb

其中象 dump\*, load\*, sql\*, syncdb, reset\* 等命令都是由orm app提供的。

如果想看单个命令的帮助信息，可以执行::

    #> uliweb help sql
    Usage: uliweb sql <appname, appname, ...>
    
    Display the table creation sql statement. If no apps, then process the whole dat
    abase.

常用全局选项说明
~~~~~~~~~~~~~~~~~~~

除了命令，uliweb还提供了全局可用的参数，它与单个命令自已的参数不同，它是对
所有命令都可以使用的参数。
    
--help
    和不带任何参数一样，显示帮助信息。
    
-v, --verbose
    是否冗余方式输出。缺省情况下，许多命令在成功时不会有输出结果，只在出错时
    显示出错信息。使用-v模式，可以在执行时显示一些执行信息。
    
-s SETTINGS, --settings=SETTINGS
    uliweb的全局配置文件缺省为project/apps目录下的settings.ini文件，你也可以通过
    本参数将其改为其它的文件名。
    
-L LOCAL_SETTINGS, --local_settings=LOCAL_SETTINGS 
    除全局配置文件外，还有一个本地配置文件，缺省文件名为local_settings.ini。也
    同样放在project/apps目录下。它会在settings.ini被处理完之后被处理。
    因此，你可以在其中加入只在当前环境有效的参数，并且不将其放入版本库中，以实
    现，不同的环境有不同的配置信息。简单讲，可以在settings.ini中放在公共的配置
    信息，在local_settings.ini中放入与环境相关的配置信息。
    
--pythonpath=PYTHONPATH
    设置python路径，将会被添加到sys.path。
    
--version
    显示当前的版本
    
runserver
~~~~~~~~~~~~~~~~~~

启动开发服务器::

    Usage: uliweb runserver [options] 
    
参数说明:
    
-h HOSTNAME

    开发服务器的地址，缺省为localhost
    
-p PORT

    开发服务器端口，缺省为8000
    
--no-reload

    是否当修改代码后自动重新装载代码，缺省为True。
    
--no-debug

    是否当出现错误时可以显示Debug页面，缺省为True。
    
--thread

    是否使用线程模式。缺省为False。
    
--processes=PROCESSES

    启动时创建进程的个数。此命令在windows下不可用。因为它要使用os.fork来创
    建进程。
        
示例：

::

    uliweb runserver #启动缺省服务器
    
develop
~~~~~~~~~~~~~~~~~~

功能同runserver，但是会自动包含develop这个App。

makeproject
~~~~~~~~~~~~~~~~~~

生成一个project框架，它将自动按给定的名字生成一个project目录，同时包含有初始子目录和文件。

::

    Usage: uliweb makeproject projectname
  
示例：

::

    uliweb makeproject project 
    
创建project项目目录。

makeapp
~~~~~~~~~~~~~~~~~~

生成一个app框架，它将自动按给定的名字生成一个app目录，同时包含有初始子目录和文件。

::

    Usage: uliweb makeapp appname
  
示例：

::

    uliweb makeapp Hello 
    
创建Hello应用。如果当前目前下有apps目录，则将在apps目录下创建一个Hello的目录，
并带有初始的文件和结构。如果当前目前下没有apps目录，则直接创建Hello的目录。

makepkg
~~~~~~~~~~~~~~~~~~

生成一个Python包结构目录，即带有__init__.py文件。

::

    Usage: uliweb makepkg pkgname

exportstatic
~~~~~~~~~~~~~~~~~~

将所有已安装的app下的static文件和子目录复制到一个统一的目录下。注意，如果你在apps的
settings.py中设定了INSTALLED_APPS参数，则所有设定的app将被处理，如果没有设置，则
按缺省方式，将apps目录下的所有app都进行处理。对于存在同名的文件，此命令缺省将进行检
查，如果发现文件名相同，但内容不同的文件将会给出指示，并且放弃对此文件的拷贝。可以
在命令行使用-no-check来关闭检查。

::

    Usage: uliweb exportstatic [options] outputdir
    
参数说明:
    
-c, --check
    是否在拷贝时进行检查，一旦发现不符会在命令行进行指示。如果设定为
    不检查，则直接进行覆盖。缺省为不检查。
    
--js
    和下面的-J连用，用于将js文件进行压缩处理。

-J JS_COMPRESSOR
    JS压缩程序(Jar包)路径。缺省使用Google Clource Compiler(compiler.jar)来
    进行处理。默认是从命令执行目录下查找compiler.jar包。
    
--css
    和下面的-C连用，用于将css文件进行压缩处理。

-C CSS_COMPRESSOR
    CSS压缩程序(Jar包)路径。缺省使用Yahoo的Yui CSS Compressor(yuicompressor.jar)
    来进行处理。默认是从命令执行目录下查找yuicompressor.jar包。
        
示例：

::

    uliweb exportstatic static
    #将所有已安装的app下的static文件拷贝到static目录下。
        
i18n
~~~~~~~~~~~~~~~~~~

i18n处理工具，用来从项目中提取_()形式的信息，并生成.pot文件。可以按app或全部app或整个
项目为单位进行处理。对于app或全部app方式，将在每个app下创建： ``app/locale/[zh]/LC_MESSAGES/uliweb.pot`` 
这样的文件。其中[zh]根据语言的不同而不同。并且它还会把.pot文件自动合并到uliweb.po文件上。

::

    Usage: uliweb i18n [options] <appname, appname, ...>
    
参数说明:
    
--apps

    对所有app进行处理。
    
-p

    处理整个项目。
    
-d DIRECTORY

    处理指定目录。
    
--uliweb

    只处理uliweb本身。

-l LOCALE

    如果没有指定则为en。否则按指定名字生成相应的目录。
        
如果最后给出app的列表，则会按指定的app进行处理。但一旦给出了--apps参数，
则app列表将无效。
        
        
示例：

::

    uliweb i18n -d plugs -l zh_CN #处理plugs目录
    uliweb i18n --apps -l zh_CN   #全部全部app的处理
    uliweb i18n -l zh_CN Test     #只处理 Test app
    uliweb i18n -p                #整个项目，使用en
    
call
~~~~~~~~~~~~~~~~~~

::

    Usage: uliweb call name
    
执行所有安装的App下的名为<name>.py程序。

support
~~~~~~~~~~~~~~~~~~

::

    Usage: uliweb support supported_type
    
向当前的项目添加某种平台的支持文件。目前支持gae和doccloud。

gae平台
    将额外拷贝app.yaml和gae_handler.py。

dotcloud平台
    将额外拷贝requirements.txt和wsgi.py。不过一般情况下你有可能要修改requirements.txt
    以满足你的要求。
    
shell
~~~~~~~~~~~~~~~~~~~~

在当前项目目录下，进入shell环境。可以直接使用如application, settings.ini等全局
变量。
    
其它App包含的命令
---------------------

orm app
~~~~~~~~~~~~~~

orm app带有一系列针对数据库操作的命令，列举如下：

syncdb
^^^^^^^^^^^^^^

自动根据已安装的app中settings.ini中所配置的MODELS信息，在数据库中创建不存在的表。
如果只是写在models.py中，但是未在settings.ini中进行配置，则不能自动创建。

settings.ini中的写法如::

    [MODELS]
    question = 'ticket.models.Question'
    
其中key是与Model对应的真正的表名，不能随便起。

sql
^^^^^^^^^^^^^^

::

    Usage: uliweb sql <appname, appname, ...>
    
用于显示对应app的Create语句。但是目前还无法显示创建Index的信息。

命令后面可以跟若干app名字，如果没有给出，则表示整个项目。
    
sqldot
^^^^^^^^^^^^^^^^

::

    Usage: uliweb sqldot <appname, appname, ...>
    
类似sql命令，但是它会将表及表的关系生成.dot文件，可以使用graphviz将dot文件转
为图形文件。

droptable
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb droptable <tablename, tablename, ...>
    
从数据库中删除某些表。

dump
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb dump [options] <appname, appname, ...>
    
将数据从数据库中卸载下来。

::

参数说明:
    
-o OUTPUT_DIR
    数据文件输出路径。缺省在项目目录的./data目录下。
    
-t, --text
    将数据以纯文本格式卸载下来。
    
--delimiter=DELIMITER
    文本文件字段的分隔符。缺省为','。需要与-t连用。
                      
--encoding=ENCODING
    文本文件字符字段所使用的编码。缺省为'utf-8'。需要与-t连用。

dumptable
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb dumptable [options] <tablename, tablename, ...>
    
将指定的表中的数据卸载下来。参数说明同dump。

dumptablefile
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb dumptablefile [options] tablename text_filename
    
将指定的表数据卸载到指定的文件中。此命令与dump和dumptable不同的地方是：这个命令
只处理一个表，并且可以指定输出文件名。而后两个命令不能指定文件名，它将按表名生
成文件名，并且放到指定的目录下。

::

参数说明:
    
-t, --text
    将数据以纯文本格式卸载下来。
    
--delimiter=DELIMITER
    文本文件字段的分隔符。缺省为','。需要与-t连用。
    
--encoding=ENCODING
    文本文件字符字段所使用的编码。缺省为'utf-8'。需要与-t连用。

load
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb load [options] <appname, appname, ...>
    
将数据装入到数据库中。

::

参数说明:
    
-d DIR
    数据文件所存放的目录。
    
-t, --text
    将数据以纯文本格式进行处理。
    
--delimiter=DELIMITER
    文本文件字段的分隔符。缺省为','。需要与-t连用。
    
--encoding=ENCODING
    文本文件字符字段所使用的编码。缺省为'utf-8'。需要与-t连用。
    
loadtable
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb loadtable [options] <tablename, tablename, ...>
    
只装入指定的表名数据到数据库中。参数同load。


loadtablefile
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb loadtablefile [options] tablename text_filename
    
将指定的文件装入到对应的表中。

::

参数说明:
    
-t, --text
    将数据以纯文本格式进行处理。
    
--delimiter=DELIMITER
    文本文件字段的分隔符。缺省为','。需要与-t连用。
    
--encoding=ENCODING
    文本文件字符字段所使用的编码。缺省为'utf-8'。需要与-t连用。

reset
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb reset <appname, appname, ...>
    
重置整个数据库或指定的app。

resettable
^^^^^^^^^^^^^^^^^^

::

    Usage: uliweb resettable <tablename, tablename, ...>
    
重置指定的表。

auth app
~~~~~~~~~~~~~~

createsuperuser
^^^^^^^^^^^^^^^^^^^^^

创建超级用户。