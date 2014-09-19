# 命令行工具使用指南


## uliweb

当运行不带参数的uliweb命令时，会显示一个帮助信息，但是因为命令很多，所以这个帮
助只是列出可用命令的清单，如:


```
Usage: uliweb [global_options] [subcommand [options] [args]]

Global Options:
  --help                show this help message and exit.
  -v, --verbose         Output the result in verbose mode.
  -s SETTINGS, --settings=SETTINGS
                        Settings file name. Default is "settings.ini".
  -L LOCAL_SETTINGS, --local_settings LOCAL_SETTINGS
                        Local settings file name. Default is
                        "local_settings.ini".
  --project PROJECT     Project "apps" directory.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/myproject".
  --version             show program's version number and exit

Type 'uliweb help <subcommand>' for help on a specific subcommand.

Available subcommands:
  call
  develop
  export
  exportstatic
  find
  i18n
  makeapp
  makecmd
  makepkg
  makeproject
  runserver
  shell
  support
```

在uliweb中，有一些是全局性的命令，有一些是由某个app提供的命令。因此当你在一个
project目录下运行uliweb命令时，它会根据当前project所安装的app来显示一个完整的
命令清单。上面的示例只显示了在没有任何项目时的全局命令。比如你安装了orm app，则
可能显示的清单为:


```
Available subcommands:
  call
  createsuperuser
  dbinit
  develop
  droptable
  dump
  dumptable
  dumptablefile
  export
  exportstatic
  find
  i18n
  load
  loadtable
  loadtablefile
  makeapp
  makecmd
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
```

其中象 dump*, load*, sql*, syncdb, reset* 等命令都是由orm app提供的。

如果想看单个命令的帮助信息，可以执行:


```
#> uliweb help sql
Usage: uliweb sql <appname, appname, ...>

Display the table creation sql statement. If no apps, then process the whole dat
abase.
```


### 常用全局选项说明

除了命令，uliweb还提供了全局可用的参数，它与单个命令自已的参数不同，它是对
所有命令都可以使用的参数。


### runserver

启动开发服务器:


```
Usage: uliweb runserver [options]

Start a new development server.

Options:
  -h HOSTNAME           绑定IP，缺省为localhost，如果希望让别人访问，可以绑定 0.0.0.0
  -p PORT               绑定的端口号，缺省为8000
  --no-reload           禁止服务器自动重启。缺省是自动重启
  --no-debug            禁止服务器进入调试模式。缺省是进入
  --color               输出彩色日志，缺省为不输出
  --thread              如果设置，则进入多线程工作模式。缺省是单线程
  --processes=PROCESSES
                        进程方式启动的个数。缺省是1个。在windows下无法使用
  --ssl                 以https方式启动服务。此方式将自动使用pyOpenSSH来创建证书
  --ssl-key=SSL_KEY     如果不想自动创建证书，则可以指定ssl-key和ssl-cert来使用已经
  --ssl-cert=SSL_CERT   生成好的证书。ssl-key和ssl-cert可以同时使用。ssl为单独使用。
  --tornado             使用tornado来提供服务
  --gevent              使用gevent来提供服务
  --gevent-socketio     使用gevent-socketio来提供服务
  
```

参数说明:


{% alert class=info %}
在werkzeug的文档中有如何生成key和cert文件的方法，示例如下:

```
$ openssl genrsa 1024 > ssl.key
$ openssl req -new -x509 -nodes -sha1 -days 365 -key ssl.key > ssl.cert
```

其中在生成cert文件时，会提许多的问题，按要求回答一下就好了。在windows下我是装了git环境，它带了一个openssl的工具，用起来很方便。
{% endalert %}

示例：


```
uliweb runserver #启动缺省服务器
```

如果你想修改日志颜色，可以在settings.ini设置：

```
[LOG.COLORS]
DEBUG = 'white'
INFO = 'green'
WARNING = 'yellow'
ERROR = 'red'
CRITICAL = 'red'
```

可用颜色为：BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE. 颜色值不区分大小写。

### develop

功能同runserver，但是会自动包含develop这个App。


{% alert class=info %}
使用这个命令，需要安装plugs。

{% endalert %}

### export

将已安装的app目录下的文件导出到指定目录。它的作用是当部署到某些受限环境时，需要
将用到的模块源码打包上传，通过这个命令可以导出uliweb项目中已经安装的模块的源码，
未安装的app源码将不会导出。同时也可以导出指定模块的源码，如导出uliweb的源码。


```
Usage: uliweb export [options] [module1 module2]
```

参数说明:

示例：


```
uliweb export -d ../lib
#将所有已安装的app导出到 ``../lib`` 目录下，不包含 static 目录。

uliweb export -d ../lib uliweb
#uliweb包导出到 ``../lib`` 目录下。
```


### exportstatic

将所有已安装的app下的static文件和子目录复制到一个统一的目录下。注意，如果你在apps的
settings.py中设定了INSTALLED_APPS参数，则所有设定的app将被处理，如果没有设置，则
按缺省方式，将apps目录下的所有app都进行处理。对于存在同名的文件，此命令缺省将进行检
查，如果发现文件名相同，但内容不同的文件将会给出指示，并且放弃对此文件的拷贝。可以
在命令行使用-no-check来关闭检查。

```
Usage: uliweb exportstatic [options] output_directory [app1, app2, ...]

Export all installed apps static directory to output directory.

Options:
  -c, --check  检查输出文件或目录是否有冲突，即同名但是内容不同的文件,或相同的子目录名
  --js         允许javascript压缩处理（缺省使用rminjs）
  --css        允许css压缩处理（缺省使用rmincss）
  --auto       允许js和css同时压缩处理
```

参数说明:

可以在输出路径后面再指定若干个app的名字，这样只会导出指定app的静态文件。

示例：

```
uliweb exportstatic static
#将所有已安装的app下的static文件拷贝到static目录下。
```

目前exportstatic支持将css和js进行打包，合并，压缩的功能，具体描述详见 [CSS, JS合并与压缩](css_js_combine.html)

### find {#find}

查找对象，包括：模板、URL对应的view、静态文件、Model定义及配置项的定义位置的模块


```
Usage: uliweb find -u url
or
Usage: uliweb find -t template --tree --blocks --with-filename --source --comment
or
Usage: uliweb find -c static
or
Usage: uliweb find -m model_name
or
Usage: uliweb find -o option
```

关于模板查找

uliweb find -t template --
    查找某个模板的实际路径，如果存在多个同名的模板，则按照查找顺序依次列出。但是系统真正使用的只是第一个。

uliweb find -t template --tree --
    查找某个模板的实际路径，同时列出这个模板继承或包含其它模板的信息，如：

    ```
    apps/project/templates/layout.html

    -------------- Tree --------------
         /Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html
             (extend)/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_fluid_layout.html
                 (extend)/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html
    ---------------> (extend)apps/project/templates/layout.html
                         (include)/Users/limodou/mywork/uliweb/uliweb/contrib/csrf/templates/inc_jquery_csrf.html
                     (include)/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/menu.html
                     (include)/Users/limodou/mywork/plugs/plugs/ui/jquery/pnotify/templates/inc_show_flashes.html
    ```

    其中箭头表示当前模板的位置。

uliweb find -t template --blocks --with-filename --
    查找某个模板的实际路径，同时列出这个模板中所有block定义及继承的情况。如果同时给出 `--with-filename`
    参数，则同时显示此block定义所在的文件名，如：

    ```
    apps/project/templates/layout.html
    /Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html
    /Users/limodou/mywork/plugs/plugs/layout/default/templates/layout.html

    -------------- Blocks --------------
        html_tag   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html)
        meta   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html)
        title   (/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html)
        _css   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html)
        body_tag   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html)
        before_header   (/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html)
        header   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html)
            project   (/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html)
            nav   (/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html)
                menu   (/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html)
            user_info   (apps/project/templates/layout.html)
                message_number_show   (apps/project/templates/layout.html)
        content   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_fluid_layout.html)
            content_sidebar   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_fluid_layout.html)
            content_tool_container   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_fluid_layout.html)
                content_tool   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_fluid_layout.html)
            content_main   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_fluid_layout.html)
        footer_container   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html)
            footer   (/Users/limodou/mywork/plugs/plugs/layout/bootstrap/templates/layout.html)
        after_footer   (/Users/limodou/mywork/plugs/plugs/ui/bootstrap/templates/bootstrap/bootstrap_layout.html)
    ```

    从上面的结果可以看出block之间的包含关系，并且每个block最终生效的是定义在哪个文件中。

uliweb find -t template --source --
    打印当前模板转换为python后的源代码，不包含相关的生成注释

uliweb find -t template --source --comment --
    打印当前模板转换为python后的源代码，包含相关的生成行号及注释


### validatetemplate {#validatetemplate}

校验模板正确性，可以用于升级到0.4的模板语法检查


```
Usage: uliweb validatetemplate #整个项目检查
or
Usage: uliweb validatetemplate appname #只对appname进行检查
or
Usage: uliweb validatetemplate -f template #只对template进行检查
```

其中第三种用法，template是可以是相对路径，即从 `templates` 目录开始的相对路径, 或者是绝对路径。

### makeproject

生成一个project框架，它将自动按给定的名字生成一个project目录，同时包含有初始子目录和文件。


```
Usage: uliweb makeproject [-f] projectname
```

参数说明:

示例：


```
uliweb makeproject project
```

创建project项目目录。


### makeapp

生成一个app框架，它将自动按给定的名字生成一个app目录，同时包含有初始子目录和文件。


```
Usage: uliweb makeapp [-f] appname
```

参数说明:

示例：


```
uliweb makeapp Hello
```

创建Hello应用。如果当前目前下有apps目录，则将在apps目录下创建一个Hello的目录，
并带有初始的文件和结构。如果当前目前下没有apps目录，则直接创建Hello的目录。


### makecmd

向指定的app或当前目录下生成一个commands.py模板。


```
Usage: uliweb makecmd [appname, ...]
```

示例：


```
uliweb makecmd Hello
```


### makepkg

生成一个Python包结构目录，即带有__init__.py文件。


```
Usage: uliweb makepkg pkgname
```


### i18n

i18n处理工具，用来从项目中提取_()形式的信息，并生成.pot文件。可以按app或全部app或整个
项目为单位进行处理。对于app或全部app方式，将在每个app下创建： `app/locale/[zh]/LC_MESSAGES/uliweb.pot`
这样的文件。其中[zh]根据语言的不同而不同。并且它还会把.pot文件自动合并到uliweb.po文件上。


```
Usage: uliweb i18n [options] <appname, appname, ...>
```

参数说明:

如果最后给出app的列表，则会按指定的app进行处理。但一旦给出了--apps参数，
则app列表将无效。

示例：


```
uliweb i18n -d plugs -l zh_CN #处理plugs目录
uliweb i18n --apps -l zh_CN   #全部全部app的处理
uliweb i18n -l zh_CN Test     #只处理 Test app
uliweb i18n -p                #整个项目，使用en
```


### call


```
Usage: uliweb call name
```

执行所有安装的App下的名为<name>.py程序。如果是 'moduleA.moduleB' 则导入指定的模块
执行其中的call()或main()方法。

### config(0.2.2)

```
Usage: uliweb config supported_type
```

输出支持的配置信息。缺省支持nginx和supervisor配置模板，你可以基于它们进行修改。

你也可以自定义config输出，只要在app下创建 `template_files/config`
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

### install(0.2)

```
Usage: uliweb install [appname,...]
```

执行在项目目录下或app目录下的requirements.txt。如果不指定appname，则是扫描整个项
目，如果指定app，则只扫描指定app下的requirements.txt。

### support


```
Usage: uliweb support supported_type
```

向当前的项目添加某种平台的支持文件。目前支持gae, doccloud, fcgi, bae, heroku, sae, tornado, gevent, gevent-socketio。


gae --
    将额外拷贝app.yaml和gae_handler.py。

dotcloud --
    将额外拷贝requirements.txt和wsgi.py。不过一般情况下你有可能要修改requirements.txt
    以满足你的要求。

bae --
    将额外拷贝app.conf和index.py。
    
heroku --
    将额外拷贝app.py, lib, Procfile和 requirements.txt.
    
sae --
    将额外拷贝index.wsgi和lib.
    
fcgi --
    将额外拷贝 fcgi_handler.py.

tornado --
    将额外拷贝 tornado_handler.py.
    
gevent --
    将额外拷贝 gevent_handler.py
    
gevent-socketio --
    将额外拷贝 gevent_socketio_handler.py

在0.2.2中，可以象config命令一样，在你的app下创建 `template_files/support/xxxx`
这样的目录结构，下面放执行 `uliweb support xxxx` 时将要拷贝的文件及目录即可。


### shell

在当前项目目录下，进入shell环境。可以直接使用如application, settings.ini等全局
变量。

可以带一个文件名参数，这样在进入shell交互环境之前可以先运行指定的文件。


## 其它App包含的命令


### orm app

orm app带有一系列针对数据库操作的命令，从0.1版本开始，uliorm开始支持多数据连接的
设置，具体的使用参见 ORM 的文档。同时在命令行工具上也支持对不同数据连接，它们共
同使用 `--engine` 参数。缺省为 `default` 。其它的数据库连接要在 `settings.ini`
中进行设置。

可用命令列举如下：


#### alembic

[alembic](http://readthedocs.org/docs/alembic/en/latest/index.html) 是用于
sqlalchemy的数据库迁移工具。目前Uliweb已经集成了alembic的部分命令，分别为:


```
init                        初始化alembic环境
revision                    生成一个版本
    -m --message Message    可选的消息
    --autogenerate          自动生成版本
diff                        相当于使用revision时自动带autogenerate
    -m --message Message    可选的消息
    -f --force              强制比较。如果不设，则当上一个版本没有更新
                            时，则不能进行新的比较
upgrade revision            升级指定的版本，当前版本为head
    --sql                   不真正执行升级，而是生成sql
    --tag TAG               指定一个tag（不是太明白作用）
help <subcommand>           查看某个子命令的帮助
```

全部选项：

和数据库的命令一样，alembic也支持加入 `--engine` 选项，用来选择数据库的连接。
上面所有的alembic的子命令都支持 `--engine` 选项。如果没有设置，缺省为 `default`.

在使用时，一般先执行 `init` 进行初始化，如:


```
uliweb alembic init [--engine other]
```

如果是使用缺省数据库连接，则不用带其它的参数。如果要指定其它的数据库连接，则要
使用 `--engine` 来指定。执行后，uliweb会在当前的目录下创建形为:


```
project/
    alembic/
        <engine>/
            alembic.ini
            versions/
            env.py
            script.py.mako
```

`alembic.ini` 为alembic使用的配置文件。 `env.py` 为自动处理时要调用的脚本。
uliweb主要是针对这两个文件进行了定制性的处理。上面的目录结构将会为每个数据库连接
创建一个目录。这样不同的数据库的脚本将分别存放。

在使用alembic命令前，首先要安装它，简单的命令为:


```
pip install alembic
```

{% alert class=info %}
为了更好的支持uliweb和mysql，我在原生的alembic上进行了修改，因此建议下载这个
版本 https://github.com/limodou/alembic
{% endalert %}

#### syncdb

自动根据已安装的app中settings.ini中所配置的MODELS信息，在数据库中创建不存在的表。
如果只是写在models.py中，但是未在settings.ini中进行配置，则不能自动创建。

settings.ini中的写法如:


```
[MODELS]
question = 'ticket.models.Question'
```

其中key是与Model对应的真正的表名，不能随便起。


#### sql


```
Usage: uliweb sql <appname, appname, ...>
```

用于显示对应app的Create语句。但是目前还无法显示创建Index的信息。

命令后面可以跟若干app名字，如果没有给出，则表示整个项目。


#### sqldot


```
Usage: uliweb sqldot <appname, appname, ...>
```

类似sql命令，但是它会将表及表的关系生成.dot文件，可以使用graphviz将dot文件转
为图形文件。


#### droptable


```
Usage: uliweb droptable <tablename, tablename, ...>
```

从数据库中删除某些表。


#### dump


```
Usage: uliweb dump [options] <appname, appname, ...>
```

将数据从数据库中卸载下来。

参数说明:


{% alert class=info %}
dump系列函数在0.1版本后有所变化。因为支持了多数据库，所以缺省情况下，dump
出来的文件将存放到 `data/default` 目录下。如果指定了 `--engine other` 参数，则
文件将存放到 `data/other` 目录下。同时load系列函数也会作相同的处理。

{% endalert %}

#### dumptable


```
Usage: uliweb dumptable [options] <tablename, tablename, ...>
```

将指定的表中的数据卸载下来。参数说明同dump。


#### dumptablefile


```
Usage: uliweb dumptablefile [options] tablename text_filename
```

将指定的表数据卸载到指定的文件中。此命令与dump和dumptable不同的地方是：这个命令
只处理一个表，并且可以指定输出文件名。而后两个命令不能指定文件名，它将按表名生
成文件名，并且放到指定的目录下。

参数说明:


#### load


```
Usage: uliweb load [options] <appname, appname, ...>
```

将数据装入到数据库中。

参数说明:

```
Options:
  -d DIR                输出目录，缺省为当前项目下的data目录
  -b BULK               批量插入条数，缺省为100条
  -t, --text            以文本格式装入数据
  --delimiter=DELIMITER
                        文本文件使用的字段分隔符，缺省为 ','
  --encoding=ENCODING   文本文件编码，缺省为 'utf-8'
  -p, --project         只处理项目中的所有表。缺省为False，表示可以处理整个数据库中的表，可能在项目之外
  -z ZIPFILE            导出数据为zip文件名
  --engine=ENGINE       指定数据库连接名.
```

当使用 `-z` 参数时，如果不指定 `-d` 参数，则会自动在 `./data` 下创建一个临时文件夹，如果指定，则在
指定目录下创建临时文件夹，如果给出 `-v` 则可以在导出前看到输出的目录。并且在导出完成之后，会自动将临时
文件夹删除。

#### loadtable


```
Usage: uliweb loadtable [options] <tablename, tablename, ...>
```

只装入指定的表名数据到数据库中。参数同load。


#### loadtablefile


```
Usage: uliweb loadtablefile [options] tablename text_filename
```

将指定的文件装入到对应的表中。

参数说明:


#### reset


```
Usage: uliweb reset <appname, appname, ...>
```

重置整个数据库或指定的app。


#### resettable


```
Usage: uliweb resettable <tablename, tablename, ...>
```

重置指定的表。


#### sqlhtml


```
Usage: uliweb sqlhtml <appname, appname, ...> > output.html
```

对指定的app或整个数据库生成表结构的说明文档。


#### validatedb


```
Usage: uliweb validatedb [-t] <appname, appname, ...>
```

对指定的app或整个数据库进行结构校验，检查数据库中的字段与源码中的Model定义是否
一致。


### auth app


#### createsuperuser

创建超级用户。

