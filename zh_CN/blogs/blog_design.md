# 设计Blog表结构

目前我们的首页还没有完成，但是因为还没有数据，所以我们还是先实现添加新博客的功能。
因此首先要实现表结构的定义，然后实现添加新blog的功能。

## 安装依赖包

在 [第一章 介绍](introduction.html) 中，我们提到了sqlalchemy和alembic，但是当时
我们没有安装。现在就让我们先来安装它们。

安装它们一种方式是手工安装：

```
pip install sqlalchemy
pip install uliweb-alebmic
pip install MySQL-python
```

这里alembic没有使用原始的版本，而是我修改过的。因为我在alembic中添加了一些对Uliweb
特性的一些支持，直接使用原来的alembic是没有的。并且原始的不能直接与Uliweb集成。

本例使用的数据库是常见的Mysql，所以需要安装 `MySQL-python` 包。除了 `MySQL-python`
我还试过 pymysql ，所以你也可以考虑使用它。它还支持 py3 版本。

如果觉得上面的安装比较麻烦，还可以在命令行执行：

```
uliweb install uliweb.contrib.orm
```

这样，会自动根据 uliweb.contrib.orm 下的 `requirements.txt` 来安装以上三个包。

{% alert class=info %}
如果是在Linux下安装MySQL-python，需要安装python-devel和mysql-devel的包，因为有
一些C模块需要编译。而 pymysql 是纯python的包，所以安装方便。不过效率上比 MySQL-python 差一些。
{% endalert %}

## 使用Mysql数据库

在安装了 `uliweb.contrib.orm` 之后，缺省已经有了数据库的设置，缺省使用 sqlite 。不过
如果数据库发生变化，sqlite不支持 `alert table` 这样的命令，所以不能很方便使用
alembic 来进行表结构迁移。所以我们把数据库换成 Mysql 的。我们可以在 local_settings.ini
中进行配置，这样不影响别人使用你的代码。

在local_settings.ini中添加以下内容：

```
[ORM]
CONNECTION = 'mysql://blog:blog@localhost/blog?charset=utf8'
```

这里我们使用sqlalchemy的格式来配置数据库连接串。其中，用户名为 `blog`，口令是 `blog`，
数据库是`blog`(你可以改为实际的用户名、口令和数据库)。同时我们还通过类似于 query_string
指定了客户端连接时使用的编码是 `utf8` 。

接着让我们在Mysql中创建对应的数据库，创建用户，以及给用户设置权限。这些操作都
需要通过Mysql相关的工具[^1]来进行。注意，这些是不能通过 Uliweb 来完成的。

[^1]: 这里向大家推荐 [heidisql](http://www.heidisql.com/) 这个工具，体积小，
    有绿色版，功能强大。
    
如果不会使用Mysql建议去学一下，不行暂时使用缺省的sqlite也是可以的。

## 关于应用编码的问题

为了减少编码转換的错误，建议整个应用全部使用utf-8编码，包括.py源代码，模板，数据库，配置文件等。

## 创建blog app

```
uliweb makeapp blog
```

注意，要把 `blog` 添加到 `apps/settings.ini` 的 `INSTALLED_APPS` 中。

## 创建Blog相关的Model

### 相关表

与Blog相关的表考虑如下： 

Blog
:   这是Blog的主表，用来存放所有Blog信息

BlogCategory
:   Blog分类表

User
:   用来关联用户，因为我们已经配置了 `uliweb.contrib.auth` 所以我们可以直接使用
    它。
    
我们不会实现评论功能，而是使用社会化评论，如 disqus，所以这里就不设计评论表了。

### Model开发流程介绍

Model创建者：

1. 在app下创建models.py，然后编写Model类
1. 在app下的settings.ini中对Model进行配置

Model使用者：
1. 从uliweb中导入functions，然后使用 `functions.get_model('name')` 来获得Model类
1. 直接导入 `from uliweb.orm import get_model` ，然后再使用 `get_model('name')` 
   来获得Model类
1. 所有的Model类一定要通过get_model()来获得，不要直接从models.py中导入，Uliweb
   会通过get_model()进行初始化。
1. 如果存在反向获取，如 A 中定义了一个到 B 的关系，那么如果通过B反向获取A的信息
   时，要A, B全部使用 `get_model()` 来获得。

### BlogCategory表结构设计

因为Blog将引用BlogCategory，所以BlogCategory最好先定义。

以下为参考表结构：

```class=linenums
#coding=utf8

from uliweb.orm import *
from uliweb.i18n import ugettext_lazy as _

class BlogCategory(Model):
    name = Field(str, max_length=80, verbose_name=_('Name'))
    
    def __unicode__(self):
        return self.name
```

第4行的作用是定义i18n的翻译函数，这样所有使用 `_()` 的地方都可以进行i18n翻译串
的提取，然后在运行时动态使用对应的语言。关于i18n我们在后面会专门介绍。

所有的新的Model都要从Model类派生，一个Model就对应数据库的一张表。Uliweb会使用
Model的小写字母作为表名。所以我们一般如下约定：

* 首字母大写表示类，用于Model的处理
* 表名则使用小写

`Field()` 是一个函数，它用来将类型与真正的数据库的字段进行对应，以生成真正的字段
实例。其实我们也可以使用效为原始的类，如 `str` 对应的是 `StringProperty` ，不过
这种方法有些冗余，也不方便记忆，所以一般都使用 `Field()` 来定义。

常见的类型有： `str`, `int`, `float`, `bool`, `datetime.datetime`, `datetime.date`, 
`datetime.time`, `CHAR`, `TEXT`, `BLOB`, `DECIMAL`, `PICKLE`, `FILE` 。

其中大写的表示不是python自带的类型。

不同的字段可以传入不同的参数，通常的属性有： 

verbose_name
:   表示显示用的名称。可以是中文。在本例中通过定义 `_('Name')` 来实现i18n的处理

default
:   缺省值

server_default
:   数据库缺省值，将会在Create语句中的DEFAULT子句中出现

index
:   是否创建索引

nullable
:   是否可以允许 NULL 值

unique
:   是否允许重复

required
:   是否必输项。如果为 `True`, 则不能为 `empty` 值，不同的字段empty的定义不同

除了以上参数，不同的字段还有不同的参数。详情可以参见 [ORM文档](../orm.html)

这里 str 类型可以定义 `max_length` 表示最大长度。`str` 是与 `varchar` 对应，而 `CHAR`
是与 `char` 对应。一个表示可变长，一个表示定长。

一般每个Model建议定义一个 `__unicode__` 的函数，这样你就可以使用 `unicode(obj)`
来显示一个对应的主要信息。同时它们也将用在其它的函数中。

Model的字符串类型的值，如 str, CHAR, TEXT 都会自动处理为unicode，所以在使用它们
时要特殊注意和中文字符串之间的编码要一致，不一致时需要进行转換。建议都使用unicode
或utf8编码。

### Blog表结构设计

考虑以下的参考结构:

```
class Blog(Model):
    title = Field(str, max_length=200, verbose_name=_('Title'), required=True)
    content = Field(TEXT, verbose_name=_('Content'), required=True)
    html = Field(TEXT, verbose_name=_('HTML'))
    created_time = Field(datetime.datetime, verbose_name=_("Created Time"), 
        auto_now_add=True, index=True)
    modified_time = Field(datetime.datetime, verbose_name=_("Modified Time"), 
        auto_now_add=True, auto_now=True)
    category = Reference('blogcategory', verbose_name=_('Category'), index=True)
    author = Reference('user', verbose_name=_('Author'))
    
    def __unicode__(self):
        return self.title
```

其中：

html
:   将用来存储转成Html之后的内容。因为我们这个Blog将使用markdown语法来写，所以
    需要将其转为Html。转换工具将使用我写的 [par](https::/github.com/limodou/par) 这个包。
    转为Html是为了在展示时提高效率，否则每次都要进行转换。以后我们还可以考虑实现
    页面的静态化，这样展示速度就会更快了。
    
created_time
:   它使用了一个 `auto_now_add` 属性，表示当添加时，自动使用服务器的时间来自动填充。
    因此，你并不需要给它传值。同时它还指定了 `index=True` ，表示将按这个字段来
    创建索引，主要是为了排序时更快。
    
modified_time
:   和 `created_time` 类似，不过它多了一个 `auto_now` 它的作用是当修改时自动填充。
    如果你既想在添加时，又想在修改时自动填充这个字段，就要象上面的代码一样，同时
    传入 `auto_now_add=True` 和 `auto_now=True` 。
    
category, user
:   分别引用了 BlogCategory 和 User 表。在Uliweb中可以定义三种关系： 

    Reference
    :   一对多
    
    OneToOne
    :   一对一
    
    ManyToMany
    :   多对多
    
    在关系中，我们使用字符串形式的表名来关联。
    
### 配置Model

要想使用定义好的Model，还需要在 settings.ini 中进行配置，这里在 blog app 下还没
有settings.ini，所以创建一个，然后输入：

```
[MODELS]
blogcategory = 'blog.models.BlogCategory'
blog = 'blog.models.Blog'
```

这里， `blogcategory` 和 `blog` 就是表名。对应的值是它们的类所在的路径。这里 key 一般是小写，大写也没关系。

因为 User 是在 `uliweb.contrib.auth` 中定义的，它已经配置好了。

## 创建表

在创建表之前要确保你的数据库已经建好，用户已经建好，权限也给了。

在Uliweb中，通过命令行可以自动建表，并且可以修改表结构。

对于建表有两种操作方法：

1. 使用 `uliweb syncdb` 它可以自动检查Model是否已经在数据库中存在，如果不存在
   则自动创建，但如果存在，则不会创建。它不会处理表结构的变化。
1. 使用 `uliweb alembic` 命令，先比较，后同步。它可以处理表的新増，删除，修改等
   情况，所以功能更为强大。

那么，在这里我们先使用 `syncdb` 来建表：

```
uliweb syncdb -v
```

输入 `-v` 参数是为了能更方便地看到输出。输出结果如下：

```
Connection : mysql://blog:***@localhost/blog?charset=utf8

[default] Creating [1/5, blog] blogcategory...CREATED
[default] Creating [2/5, blog] blog...CREATED
[default] Creating [3/5, uliweb.contrib.auth] user...CREATED
[default] Creating [4/5, uliweb.contrib.auth] usergroup_user_users...CREATED
[default] Creating [5/5, uliweb.contrib.auth] usergroup...CREATED
```

我们可以看到数据库是 mysql ，密码使用星号隐藏了。一共有5张表，因为都不存在所以
最后都是 `CREATED` 的状态。这里 blog 有两张表，其它三张是因为配置了 uliweb.contrib.auth 
所带的表。