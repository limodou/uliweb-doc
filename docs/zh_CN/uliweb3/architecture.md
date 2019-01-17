# 体系结构和机制


## 组织结构

Uliweb 认为一个项目是由不同的模块组成，所以采用了类似于Django App的方式来进行
项目的组织，它们都统一放在 apps 目录下。同时 Uliweb 的App可以是任何符合Uliweb
要求的Python包（使用uliweb makeapp appname创建即可），并且可以是独立的Python
模块放在非apps的地方，只要可以导入就可以了。Uliweb 的 app 的组织重点考虑了功能
及开发的独立性、复用性和配置化，每个 app 可以有自已独立的：


* settings.ini 它是配置文件
* templates目录用于存放模板
* static目录用于存放静态文件
* views文件，用于存放view代码

这种组织方式使得Uliweb的App重用更为方便。

apps的结构为：


```
apps/
    .gitignore
    __init__.py
    settings.ini
    local_settings.ini
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
```

通过运行 `uliweb makeproject projectname` 就可以创造一个空的项目。同时在 0.1.6
中会自动添加 `.gitignore` 和 `local_settings.ini` 文件。其中 `.gitignore`
已经自动添加了 `local_settings.ini` 文件。因为 `local_settings.ini` 主要是
解决不同环境的不同配置问题，所以不应该放入版本中。


## App管理

一个项目可以由一个App或多个App组成，而且每个App的结构不一定要求完整，因此一个App可以：


* 只有一个settings.ini 这样可以做一些初始化配置的工作，比如：数据库配置，i18n的
    配置等
* 只有templates，可以提供一些公共的模板
* 只有static，可以提供一些公共的静态文件
* 其它的内容

Uliweb在启动时对于apps下的App有两种处理策略：


1. 认为全部App都是有效的(这种情况比较少见)
1. 根据 `apps/settings.ini` 和 `apps/local_settings.ini` 中的配置项 `INSTALLED_APPS` 来决
    定哪些App是有效的

Uliweb在启动时会根据有效的App来导入它们自已的settings.ini文件，并将其中配置项进行合
并最终形成一个完整的 `settings` 变量供App来使用。同时在处理生效的App的同时，
会自动查找所有 `views` 开头的文件和 `views` 子目录并进行导入，这块工作主要是为
了收集所有定义在views文件中的URL。

这样当Uliweb启动完毕，所有App下的settings.ini和views文件将被导入。因此，你可以
在App下的 `__init__.py` 文件中做一些初始化的工作。不过对于大部分的配置工作，建
议采用在 `settings.ini` 中定义，然后再绑定对应的事件主题的方式，其目的是实现配置化。


## App依赖

不同的App之间由于功能上的相互关系可能会产生依赖，因此Uliweb允许在定义App时定义所依赖
的其它的App，这样在配置有效App时，可以减少配置的工作量，在启动时，会自动处理依赖的
App。


## Settings处理

Uliweb会按以下顺序来处理 `settings.ini` 文件:


1. `uliweb/core/default_settings.ini` 它是最初始的settings信息
1. 按定义的顺序导入每个App下的 `settings.ini` 信息
1. 导入 `apps/settings.ini` 信息
1. 导入 `apps/local_settings.ini` 信息

如果出现同名配置项，则对于不可变数据类型，后定义的项将覆盖前面定义的值。如果是可
变数据类型，则将进行数据合并。


## 分散开发，集中使用

Uliweb采用分模块开发，集中使用的原则。即开发时，代码和资源分散在不同的App中，但是
在使用时，将把它看成一个整体进行处理。比如查找某个模板，将在所有的App的templates
中进行查找，按照定义时的倒序进行处理。


## URL处理

目前Uliweb支持两种URL的定义方式。

一种是将URL定义在每个view模块中，通过expose来定义。

另一种是在settings.ini中的[EXPOSES]中进行定义。这种方式更适合配置化。

URL的格式采用werkzeug的routing模块处理方式。可以定义参数，可以反向生成URL。在
Uliweb中定义了两个方便的函数：


* expose 用来将URL与view方法进行映射
* url_for 用来根据view方法反向生成URL


## MVT框架

Uliweb 也采用 MVT 的框架。


Model --
    目前 Model 是基于 SqlAlchemy 封装的 ORM 。

View --
    则采函数或类的方式。当 Uliweb 在调用 view 函数时，会自动向函数注入一些对象，
    这一点有些象 web2py 。不过 web2py 是基于 exec ，而 Uliweb 是通过向函数注入
    变量 (func_globals) 来实现的。这种方式会在某种程序上减少一些导入代码，非常
    方便。不过，它只对直接的 view 方法有效，对于 view 函数中又调用的函数无效。
    因此你还可以直接通过

    ```
    from uliweb import request, response
    ```

    这样的方式来导入一些全局性的对象。

Template --
    一般你不需要主动来调用， Uliweb 采用自动映射的做法，即当一个 view 函数返回
    一个 dict 变量时，会自动查找模板并进行处理。当返回值不是 dict 对象时将不自
    动套用模板。如果在 response 中直接给 response.template 指定模板名，可以不
    使用缺省的模板。缺省模板文件名是与 view 函数名一样，但扩展名为 .html 。


在使用模板时也有一个环境变量，你可以直接在模板中直接使用预置的对象。同时Uliweb
还提供了对view函数和模板环境的扩展能力。


## 扩展处理

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

