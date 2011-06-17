===============
体系结构和机制
===============

组织结构
----------

如果你从 svn 中下载 Uliweb 源码，它不仅包括了 Uliweb 的核心组件，同时还包括了
uliwebproject 网站的全部源码和一些示例程序。 Uliweb 采用与 web2py 类似的管理方
式，即核心代码与应用放在一起，到时会减少部署的一些麻烦。但是对于项目的组织是采
用 Django 的管理方式，而不是 web2py 的方式。一个完整的项目将由一个或若干个 App
组织，它们都统一放在 apps 目录下。但 Uliweb 的 app 的组织更为完整，每个 app 有
自已独立的：

* settings.ini 它是配置文件
* templates目录用于存放模板
* static目录用于存放静态文件
* views文件，用于存放view代码

这种组织方式使得Uliweb的App重用更为方便。

在uliweb的下载目录下，基本结构为::

    contrib/        #内置的app模块
    core/           #核心模块
    form/           #form处理模块
    i18n/           #国际化处理模块
    lib/            #内置的一些库文件，如: werkzeug
    locale/         #i18n翻译文件
    mail/           #邮件处理
    middleware/     #middleware汇总
    orm/            #缺省ORM库
    template_files/ #用在makeproject, makeapp, support命令上的模板文件
    utils/          #输助模块
    wsgi/           #wsgi相关的一些模块
    manage.py       #Uliweb的命令行管理程序
    
apps的结构为：

::

    apps/
        __init__.py
        settings.ini
        app1/
            __init__.py
            settings.ini
            templates/
            static/
        app2/
            __init__.py
            settings.ini
            templates/
            static/
        fcgi_handler.fcgi
        wsgi_handler.py
        
    
App管理
-----------

一个项目可以由一个App或多个App组成，而且每个App的结构不一定要求完整，但至少要求
是一个Python的包的结构，即目录下需要一个__init__.py文件。因此一个App可以：

* 只有一个settings.int 这样可以做一些初始化配置的工作，比如：数据库配置，i18n的
  配置等
* 只有templates，可以提供一些公共的模板
* 只有static，可以提供一些公共的静态文件
* 其它的内容

Uliweb在启动时对于apps下的App有两种处理策略：

#. 认为全部App都是生效的(这种情况比较少见)
#. 根据apps/settings.ini中的配置项INSTALLED_APPS来决定哪些App要生效

Uliweb在启动时会根据生效的App来导入它们的settings.ini文件，并将其中配置项进行合
并最终形成一个完整的 ``settings`` 变量供App来使用。同时在处理生效的App的同时，
会自动查找所有``views``开头的文件和``views``子目录并进行导入，这块工作主要是为
了收集所有定义在views文件中的URL。

这样当Uliweb启动完毕，所有App下的settings.ini和views文件将被导入。因此，你可以
在settings.ini文件中做一些初始化的工作。

在实际的项目中，apps目录下的settings.ini文件是最后被导入的配置文件，你可以在其
中存放最后生效的配置项，用来替换某些缺省配置。

对于templates和static，Uliweb会首先在当前App下进行搜索，如果没有找到，则去其它
生效的App相应的目录下进行查找。因此，你可以把所有生效的App的templates和static
看成一个整体。所以你完全可以编写只包含templates或static的App，主要是提供一些公
共信息。

URL处理
------------

目前Uliweb支持两种URL的定义方式。

一种是将URL定义在每个view模块中，通过expose来定义。

另一种是在settings.ini中的[EXPOSES]中进行定义。这种方式更适合配置化。

URL的格式采用werkzeug的routing模块处理方式。可以定义参数，可以反向生成URL。在
Uliweb中定义了两个方便的函数：

* expose 用来将URL与view方法进行映射
* url_for 用来根据view方法反向生成URL

MVT框架
------------

Uliweb 也采用 MVT 的框架。

Model
  目前 Model 是基于 SqlAlchemy 封装的 ORM 。 
View
  则采函数或类的方式。当 Uliweb 在调用 view 函数时，会自动向函数注入一些对象，
  这一点有些象 web2py 。不过 web2py 是基于 exec ，而 Uliweb 是通过向函数注入
  变量 (func_globals) 来实现的。这种方式会在某种程序上减少一些导入代码，非常
  方便。不过，它只对直接的 view 方法有效，对于 view 函数中又调用的函数无效。
  因此你还可以直接通过 ::

    from uliweb import request, response
    
  这样的方式来导入一些全局性的对象。
Template
  一般你不需要主动来调用， Uliweb 采用自动映射的做法，即当一个 view 函数返回
  一个 dict 变量时，会自动查找模板并进行处理。当返回值不是 dict 对象时将不自
  动套用模板。如果在 response 中直接给 response.template 指定模板名，可以不
  使用缺省的模板。缺省模板文件名是与 view 函数名一样，但扩展名为 .html 。

在使用模板时也有一个环境变量，你可以直接在模板中直接使用预置的对象。同时Uliweb
还提供了对view函数和模板环境的扩展能力。

扩展处理
---------

Uliweb提供了多种扩展的能力：

* plugin 扩展。这是一种插件处理机制。 Uliweb 已经预设了一些调用点，这些调用点
  会在特殊的地方被执行。你可以针对这些调用点编写相应的处理，并且将其放在
  settings.py 中，当 Uliweb 在启动时会自动对其进行采集，当程序运行到调用点位置
  时，自动调用对应的插件函数。
* middleware 扩展。它与 Django 的机制完全类似。你可以在配置文件中配置
  middleware 类。每个 middleware 可以处理请求和响应对象。
* views 模块的初始化处理。在 views 模块中，如果你写了一个名为 __begin__ 的函数
  ，它将在执行要处理的 view 函数之前被处理，它相当于一个入口。因此你可以在这里
  面做一些模块级别的处理，比如检查用户的权限。因此建议你根据功能将 view 函数分
  到不同的模块中。

