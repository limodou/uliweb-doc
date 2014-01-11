# 全局设计

## 界面布局

一个典型的应用，根据用户不同，一般分为：普通用户和系统用户。当然，我们可以根据
实际情况进行更细的划分。因此界面也可以分为普通界面和管理界面。不同的页面它们的
风格应该是统一的，因此一般会考虑将界面通用部分放到统一的模板中，然后具体的页面
分别从这些模板继承。因此对于我们这个项目，我们将创建两个父模板： `layout.html` 和
`admin_layout.html`, 分别对应一般页面和管理页面。

界面设计是一件复杂而又相对专业的工作，现在已经有不少优秀的开源CSS框架可以让我们
直接使用，常见的有 [Bootstrap](http://getbootstrap.com/), 
[Semantic-UI](http://semantic-ui.com/), [Fundation](http://foundation.zurb.com/).
这里我选择Semantic-UI这个css框架。

## 创建 APP

### 创建 home, admin 和 semantic APP

让我们分别创建 home 和 admin 这两个app，其中 home 用来存放普通用户使用的全局性的
内容，包括整站的CSS，JS和模板。而 admin 用来存放后台管理使用的全局性的内容。

为了存放semantic的静态资源，同时创建semantic app。

```
cd uliweb_blogs
uliweb makeapp home
uliweb makeapp admin
uliweb make semantic
```

{% alert class=note %}
在uliweb 0.2.4版本之后，还可以使用 `uliweb makeapp home admin semantic` 一次性
创建多个app。
{% endalert %}

### 配置 APP

App创建之后，需要在 settings.ini 中进行配置，如现在的 settings.ini 内容是：

```
[GLOBAL]
DEBUG = False
DEBUG_CONSOLE = False
DEBUG_TEMPLATE = False

#INSTALLED_APPS = [
#    'uliweb.contrib.staticfiles',
#    'uliweb.contrib.template',
#    'uliweb.contrib.upload',
#    'uliweb.contrib.orm',
#    'uliweb.contrib.session',
#    'uliweb.contrib.cache',
#    'uliweb.contrib.auth',
#    'uliweb.contrib.i18n',
#    'uliweb.contrib.flashmessage',
#    ]
```

前三个 `DEBUG*` 是与调试相关，在 `local_settings.ini` 又重新定义为了 `True` (DEBUG_TEMPLATE)
除外。其目的就是：当部署时，这些开关项不启动。但是在本地调试时启用。

`INSTALLED_APPS` 是最重要的用来设置哪些 App 生效的配置。在Uliweb中，App可以是任何
合法的python包，因此可以引入第三方的App。在配置的时候，需要使用字符串的表示形式，
它表示这个App的导入路径。例如 `uliweb.contrib.orm` 表示，在启动应用时，Uliweb可以
直接导入 `uliweb.contrib.orm` 这个包。

上面这个是自动生成，已经列出了常见的一些App，只不过全部注释掉了，因此我们根据需要
去掉一些注释，并且将我们新建的App添加在后面。因此上面的代码改为：

```
INSTALLED_APPS = [
    'uliweb.contrib.staticfiles',
    'uliweb.contrib.template',
    'uliweb.contrib.upload',
    'uliweb.contrib.orm',
    'uliweb.contrib.session',
#    'uliweb.contrib.cache',
    'uliweb.contrib.auth',
    'uliweb.contrib.i18n',
#    'uliweb.contrib.flashmessage',
    'semantic',
    ’home',
    'admin',
    ]
```

其中：

* `uliweb.contrib.staticfiles` 用来处理静态文件
* `uliweb.contrib.template` 用来处理 use, link 标签
* `uliweb.contrib.upload` 用来处理文件上传下载
* `uliweb.contrib.orm` 用来处理数据库的ORM
* `uliweb.contrib.session` 用来处理session
* `uliweb.contrib.cache` 用来处理cache，暂时用不上
* `uliweb.contrib.auth` 用来定义用户相关的表及用户认证
* `uliweb.contrib.i18n` 用来进行国际化处理
* `uliweb.contrib.flashmessage` 用来实现静态化的flash信息显示，暂时不用

{% alert class=warn %}
有的时候，App的顺序很重要。因为Uliweb的一些机制，如：配置文件导入顺序，模板查找，
静态文件查找等都和顺序有关系。例如，两个App可能有重名的模板，那么Uliweb会最终使用
排列在最后那个App的模板，即后定义的会覆盖前面的同名资源。

这种机制还可以允许用户定义第三方的App，以替換原来的App的实现，以实现新的功能。

所以，建议是把Uliweb内置的App放在最前，第三方的App放在中间，自定义的放在最后。
{% endalert %}

## 向 semantic App 添加资源

### 拷贝文件

为什么不直接把semantic的静态资源直接放到 home 或 admin 中呢？就是因为想要复用。

访问 [semantic-ui](https://github.com/Semantic-Org/Semantic-UI) 的 github 页面，
可以直接下载 zip 文件或 clone 这个项目。找到其中的 `build\packaged` 子目录。将
其拷贝到 `semantic/static/semantic` 目录下。注意，`semantic` 要创建，原来是没有的。

{% alert class=info %}
通常，与app相关的静态资源，我都会在static目录下创建与app同名的子目录，将静态文件
放在这个目录下，主要是防止在进行静态文件抽时，万一有同名的文件会进行覆盖，而放在
不同的子目录下就可以避免这个问题。
{% endalert %}

### 删除 semantic/views.py 文件

因为semantic app只是用来存放静态文件，所以并不需要 `views.py`，因此我们把它删除。

### 创建 use 配置

uliweb.contrib.template app提供了在模板中可以使用的use标签，可以方便引用静态文件。
具体的详情可以参见 [template app](../app_template.html)。use 内容的定义可以使用
.py 文件和配置文件两种方式。这里我们简单使用配置文件的方式。

在 semantic app下创建 settings.ini ，然后输入：

```
[TEMPLATE_USE]
semantic = {'toplinks':[
    'semantic/css/semantic.min.css', 
    'semantic/javascript/semantic.min.js']}
```