# 迷你留言板

也许你已经学过了 [Hello, Uliweb](hello_uliweb.html) 这篇教程，对Uliweb已经有了一个感性的
认识，那么好，现在让我们进入数据库的世界，看一看如何使用简单的数据库。


## 准备

在 uliweb-doc 项目中已经有完整的GuestBook的源代码，你可以从它里面检出:


```
git clone git@github.com:limodou/uliweb-doc.git
cd uliweb-doc/projects/uliweb3/guestbook
uliweb runserver
```

然后在浏览器输入 [http://localhost:8000/](http://localhost:8000/) 这样就可以看到了。
目前缺省是使用sqlite3。如果你安装了python 2.6它已经是内置的。否则要安装相应的数
据库和Python的绑定模块。目前Uliweb使用 [SqlAlchemy](http://www.sqlalchemy.org) 
作为数据库底层驱动，它支持多种数据库，如：mysql, sqlite, postgresql, 等。在开始
这个例子之前要安装SQLAlchemy, 如：

```
pip install SQLAlachemy
```

在Uliweb 0.2.2版本中，为了安装方便，在uliweb.contrib.orm中添加了一个requirements.txt，里
面有最基础的ORM支持需要的包，所以可以这样安装：

```
uliweb install uliweb.contrib.orm
```

这样会自动安装 SQLAlchemy, mysqldb-python, alembic(修改版)

好了，让我们从头开始做这个练习。

## 创建工程

建议在一个空目录下开始你的工作，例如:


```
uliweb makeproject guestbook
```


## 创建APP

进入前面创建的目录，然后使用 makeapp 建一个新的App。执行:


```
cd guestbook
uliweb makeapp GuestBook
```

这样就自动会在项目的apps目录下创建一个 `GuestBook` 的App。

## 目录结构

```
GuestBook/ 工程目录
    apps/
        GuestBook/ App
```

## 配置数据库

Uliweb中的数据库不是缺省生效的，因此你需要配置一下才可以使用。Uliweb虽然提供了自已的
ORM，但是你可以不使用它。Uliweb提供了插件机制，可以让你容易地在适当的时候执行初始化的工作。
打开 `GuestBook/apps/settings.ini` 文件，修改 `INSTALLED_APPS` 的内容为:


```
INSTALLED_APPS = [
    'uliweb.contrib.orm',
    'GuestBook',
    ]
```

自已项目中的app建议放在最后，使用uliweb提供的app放在前面。

然后添加下面的内容:


```
[ORM]
CONNECTION = 'sqlite:///guestbook.db'
```

所以 `settings.ini` 将看上去象:


```
[GLOBAL]
DEBUG = True

INSTALLED_APPS = [
    'uliweb.contrib.orm',
    'GuestBook',
    ]

[ORM]
CONNECTION = 'sqlite:///guestbook.db'
```

ORM.CONNECTION 是ORM的连联字符串，它和SQLAlchemy包使用的一样。通常的格式看上去象:


```
provider://username:password@localhost:port/dbname?argu1=value1&argu2=value2
```

对于Sqlite，连接信息有些不同:


```
sqlite_db = create_engine('sqlite:////absolute/path/to/database.txt')
sqlite_db = create_engine('sqlite:///d:/absolute/path/to/database.txt')
sqlite_db = create_engine('sqlite:///relative/path/to/database.txt')
sqlite_db = create_engine('sqlite://')  # in-memory database
sqlite_db = create_engine('sqlite://:memory:')  # the same
```

这里我们使用相对路径格式，所以 `guestbook.db` 将会在guestbook目录下被创建。


## 模板环境的扩展

向 `GuestBook/__init__.py` 中添加:


```
from uliweb.core.dispatch import bind

@bind('prepare_view_env')
def prepare_view_env(sender, env):
    from uliweb.utils.textconvert import text2html
    env['text2html'] = text2html
```

这也是一个dispatch的使用示例，它将向模板的环境中注入一个新的函数 `text2html`,
这样你就可以在模板中直接使用text2html这个函数了。

{% alert class=info %}
这个不是必须的，只是显示了一下如何向模板中注入对象。
{% endalert %}

## 准备Model

在GuestBook目录下创建一个名为models.py的文件，内容为:


```
from uliweb.orm import *

class Note(Model):
    username = Field(CHAR)
    message = Field(TEXT)
    homepage = Field(str, max_length=128)
    email = Field(str, max_length=128)
    datetime = Field(datetime.datetime, auto_now_add=True)
```

很简单。

首先要从 uliweb.orm 中导入一些东西，这里是全部导入。

Uliorm在定义Model时支持两种定义方式：


* 使用内部的Python类型，如：int, float, unicode, datetime.datetime, datetime.date,
    datetime.time, decimal.Decimal, str, bool。另外还扩展了一些类型，如：BLOB, 
    CHAR, TEXT, DECIMAL。所以你在定义时只要使用Python的类型就好了。
* 然后就是象GAE一样的使用各种Property类，如：StringProperty, UnicodeProperty,
    IntegerProperty, BlobProperty, BooleanProperty, DateProperty, DateTimeProperty,
    TimeProperty, DecimalProperty, FloatProperty, TextProperty。

一个Model需要从 `Model` 类派生。然后每个字段就是定义为类属性。Field()是一个函数，它将
会根据第一个参数来查找对应的属性类，因此:


```
class Note(Model):
    username = StringProperty()
    message = TextProperty()
    homepage = StringProperty()
    email = StringProperty()
    datetime = DateTimeProperty()
```

每个字段还可以有一些属性，如常用的：


* default 缺省值
* max_length 最大值
* verbose_name 提示信息

象CharProperty和StringProperty，需要有一个max_length属性，如果没有给出，缺省是255。

其它详细的说明可以在数据文档中查看。


{% alert class=info %}
在定义Model时，Uliorm会自动为你添加 `id` 字段的定义，它将是一个主键，这一
点与Django一样。
{% endalert %}

## 配置及创建表结构

在Model创建之后，需要先对Model进行配置，先要在apps/GuestBook下创建settings.ini(
如果不存在的话)，在其中添加以下内容:

```
[MODELS]
note = 'GuestBook.models.Note'
```

上面 `note` 是Model的名字，一般和表名一样，并且是小写。后面是这个表名对主应的
类的路径。

上面信息配置好之后，在项目目录下，进行数据库表的创建:

```
uliweb syncdb
```

这个命令可以将数据库中不存在的表创建出来。

## 静态文件处理

我们将在后面显示静态文件，现在只需要把 `uliweb.contrib.staticfiles` 添加到 `INSTALLED_APPS`
中就可以了。使用这个App，所有有效的app的static目录将被处理为静态目录，并且URL链接将添加
`/static/` 。现在 `settings.ini` 看上去象:


```
[GLOBAL]
DEBUG = True

INSTALLED_APPS = [
    'uliweb.contrib.orm',
    'uliweb.contrib.staticfiles',
    'GuestBook',
    ]

[ORM]
CONNECTION = 'sqlite:///guestbook.db'
```


## 显示留言


### 增加guestbook()的View方法

打开GuestBook下的views.py文件，加入显示留言的处理代码:


```
from uliweb import expose, functions

@expose('/')
def index():
    Note = functions.get_model('note')
    notes = Note.all().order_by(Note.c.datetime.desc())
    return {'notes':notes}
```

首先从uliweb中导出一些常用的对象和函数。

然后使用expose()来定义URL为 `/` 。

然后是index()函数的定义。

我们通过functions.get_model('note')来获得Note类。我们通过调用Note类的方法all()获得所有
记录。为了按时间倒序显示，使用order_by()方法，传入要按顺的字段。其中
`Note.c.datetime.desc()` 是Sqlalchemy的用法，表示倒序。

以下是一些简单的用法:


```
notes = Note.all()                  #全部记录，不带条件
note = Note.get(3)                  #获取id值为3的记录
note = Note.get(Note.c.username=='limodou') #获取username为limodou的记录
```

当要引用Model中的字段来生成条件时，要在类名后加 `.c` 。

然后我们返回一个字典，这样会自动使用Uliweb的模板套用机制，即自动调用与view方法
同名的模板文件。


{% alert class=info %}
在Uliweb中每个访问的URL与View之间要通过定义来实现，如使用expose。它需要一个URL的
参数，然后在运行时，会把这个URL与所修饰的View方法进行对应，View方法将转化为：

```
appname.viewmodule.functioname
```

的形式。它将是一个字符串。然后同时Uliweb还提供了一个反向函数url_for，它将用来根据
View方法的字符串形式和对应的参数来反向生成URL，可以用来生成链接，在后面的模板中我
们将看到。
{% endalert %}

### 定义index.html模板

在GuestBook/templates目录下创建与View方法同名的模板，后缀为.html。在index.html中
添加如下内容:


```
{{extend "base.html"}}
{{block content}}
<h2><a href="{{=url_for('GuestBook.views.new_comment')}}">New Comment</a></h2>
{{for n in notes:}}
    <div class="info">
    <h3><a href="{{= url_for('GuestBook.views.del_comment', id=n.id) }}">
    <img src="{{= url_for_static('delete.gif') }}"/>
    </a> {{=n.username}} at {{=n.datetime.strftime('%Y/%m/%d %H:%M:%S')}} say:</h3>
    <p>{{<<text2html(n.message)}}</p>
    </div>
{{pass}}
{{end}}
```

第一行将从base.html模板进行继承。这里不想多说，只是要注意在base.html中有一个{{block content}}{{end}}
的定义，它表示子模板可以继承的块。你可以从Uliweb的源码中将base.html拷贝到你的目录下。

h2 标签将显示一个链接，它将用来调用添加留言的view函数。注意模板没有将显示与添加的
Form代码写在一起，因为那样代码比较多，同且如果用户输入出错，将再次显示所有的留言(因为这里
没有考虑分页)，这样处理比较慢，所以分成不同的处理了。

`{{for}}` 是一个循环。记住Uliweb使用的是web2py的模板，不过进行了改造。所有在{{}}中的代码
可以是任意的Python代码，所以要注意符合Python的语法。因此后面的':'是不能省的。Uliweb的模
板允许你将代码都写在{{}}中，但对于HTML代码因为不是Python代码，要使用 `out.write(htmlcode)`
这种代码来输出。也可以将Python代码写在{{}}中，而HTML代码放在括号外面，就象上面所做的。

在循环中对notes变量进行处理，然后显示一个删除的图形链接，用户信息和用户留言。

看到 `{{<<text2html(n.message)}}` 了吗？它使用了我们在GuestBook/__init__.py中定义的text2html函
数对文本进行格式化处理。

`{{pass}}` 是必须的。在Uliweb模板中，不需要考虑缩近，但是需要在块语句结束时添加pass，表示缩
近结果。这样相当于把Python对缩近的严格要求进行了转换，非常方便。

好，在经过上面的工作后，显示留言的工作就完成了。但是目前还不能添加留言，下一步就让我们看如
何添加留言。


{% alert class=info %}
因为在base.html中和guestbook.html用到了一些css和图形文件，因此你可以从Uliweb的
GuestBook/static目录下将全部文件拷贝到你的目录下。
{% endalert %}

## 增加留言


### 增加new_comment()的View方法

在前面的模板中我们定义了增加留言的链接:


```
<a href="{{=url_for('%s.views.new_comment' % request.appname)}}">New Comment</a>
```

可以看出，我们使用了url_for来生成反向的链接。关于url_for在前面已经讲了，这里要注意的就是
函数名为new_comment，因此我们需要在views.py中生成这样的一个方法。

打开views.py，加入以下代码:


```
@expose('/new')
def new_comment():
    from forms import NoteForm
    import datetime

    Note = functions.get_model('note')
    form = NoteForm()
    if request.method == 'GET':
        return {'form':form, 'message':''}
    elif request.method == 'POST':
        flag = form.validate(request.values)
        if flag:
            n = Note(**form.data)
            n.save()
            return redirect(url_for(index))
        else:
            message = "There is something wrong! Please fix them."
            return {'form':form, 'message':message}
```

可以看到链接是 `/new` 。

首先我们导入了NoteForm这个类。它是用来生成录入Form的类，并且可以用来对数据进行校验。一会儿会对它进行介绍。

然后创建form对象。

再根据request.method是GET还是POST来执行不同的操作。对于GET将显示一个空Form，对于POST
表示用户提交了数据，要进行处理。使用GET和POST可以在同一个链接下处理不同的动作，这是一种
约定，一般中读操作使用GET，写或修改操作使用POST。

在request.method为GET时，我们只是返回空的form对象和一个空的message变量。form.html()可
以返回一个空的HTML表单代码。而message将用来提示出错的信息。

在request.method为POST时， 首先调用 `form.validate(request.values)` 对数据进行校验。
它将返回一个二元的tuple。第一个参数表示成功还是出错，第二个为成功时将转换为Python格式后
的数据，失败时为出错信息。

当flag为True时，进行成功处理。一会我们可以看到在表单中并没有datetime字段，因为我们
手工添加一个值，表示留言提交的时间。然后通过 `n = Note(**form.data)` 来生成Note记录，但这里并没有提
交到数据库中，因此再执行一个 `n.save()` 来保存记录到数据库中。

然后执行完毕后，调用 `return redirect` 进行页面的跳转，跳回留言板的首页。这里又使用了url_for来反
向生成链接。

当flag为False时，进行出错处理。


### 定义录入表单

为了与后台进行交互，让用户可以通过浏览器进行数据录入，需要使用HTML的form系列元素来定义
录入元素。对于有经验的Web开发者可以直接手写HTML代码，但是对于初学者很麻烦。并且你还要考虑
出错处理，数据格式转换的处理。因此许多框架都提供了生成表单的工具，Uliweb也不例外。Form模
块就是干这个用的。

在GuestBook目录下创建forms.py文件，然后添加以下代码:


```
from uliweb.form import *

class NoteForm(Form):
    message = TextField(label='Message', required=True)
    username = StringField(label='Username', required=True)
    homepage = StringField(label='Homepage')
    email = StringField(label='Email')
```

这里我定义了4个字段，每个字段对应一种类型。象TextField
表示多行的文本编辑，StringField表示单行文本，你还可以使用象：HiddenField, SelectField,
FileField, IntField, PasswordField, RadioSelectField等字段类型。

也许你看到了，这其中有一些是带有类型的，如IntField，那么它将会转换为对应的Python数据类
型，同时当生成HTML代码时再转换回字符串。

每个Field类型可以定义若干的参数，如：


* label 用来显示一个标签
* required 用来校验是否输入，即不允许为空
* default 缺省值
* validators 校验器

很象Model的定义，但有所不同。


### 编写new_comment.html模板文件

在GuestBook/templates下创建new_comment.html，然后添加以下内容:


```
{{extend "base.html"}}
{{block content}}
{{if message:}}
    <p class="warning">{{=message}}</p>
{{pass}}
<h1>New Comment</h1>
<div class="form">
{{<<form}}
</div>
{{end}}
```

首先是 `{{extend "base.html"}}` 表示从base.html继承。

然后是一个 if 判断是否有message信息，如果有则显示。这里要注意if后面的':'号。

然后显示form元素，这里使用了 `{{<< form}}` 。form是从View中传入的，而{{<<}}
可以对要输出的内容中的HTML标签 不进行转义处理。而 {{=variable}} 将对variable
变量的HTML标签进行转换。因此，如果你想输出原始的HTML文本，要使用{{<<}}来输出。

现在可以在浏览器中试一下了。


## 删除留言

在前面guestbook.html中，我们在每条留言前定义了一个删除的图形链接，形式为:


```
<a href="{{= url_for('GuestBook.views.del_comment', id=n.id) }}">
```

那么下面就让我们实现它。

打开GuestBook/views.py文件，然后添加:


```
@expose('/delete/<id>')
def del_comment(id):
    Note = functions.get_model('note')
    n = Note.get(int(id))
    if n:
        n.delete()
        return redirect(url_for(index))
    else:
        error("No such record [%s] existed" % id)
```

删除很简单，首先通过 `Note.get(int(id))` 来得到对象，然后再调用对象的delete()
方法来删除。


### URL参数定义

请注意，这里expose使用了一个参数，即 `<id>` 形式。一旦在expose中的url定义
中有 `<type:para>` 的形式，就表示定义了一个参数。其中type:可以省略，它可以是int等类型。而
int将自动转化为 `\d+` 这种形式的正则式。Uliweb内置了象: int, float, path, any, string等类型，你可以在 [URL Mapping](url_mapping) 文档中了解更多的细节。如果你只定义了
`<name>` 这种形式，它表示匹配 `//` 间的内容。一旦在URL中定义了参数，则需要
在View函数中也需要定义相应的参数，因此del_comment函数就写为了： `del_comment(id)` 。
这里的id与URL中的id是一样的。

好了，现在你可以试一试删除功能是否可用了。


### 出错页面

当程序出错时，你可能需要向用户提示一个错误信息，因此可以使用error()方法来返回一个出错
的页面。它的前面不需要return。只需要一个出错信息就可以了。

那么出错信息的模板怎么定义呢？在你的templates目录下定义一个名为error.html的文件，并加
入一些内容即可。

创建error.html，然后，输入如下代码:


```
{{extend "base.html"}}
{{block title}}Error{{end}}
{{block header}}<h1>Error!</h1>{{end}}
{{block content}}
<p>{{=message}}</p>
{{end}}
```

这个页面很简单，就是覆盖了一些block的定义。如title, header, content。


## 运行

在前面的开发过程中你可以启动一个开发服务器进行调试。启动开发服务器的命令为:


```
uliweb runserver
```

当启动后，在浏览器输入： `http://localhost:8000/`


## 结论

经过学习，我们了解了许多内容：


1. ORM的使用，包括：ORM的初始化配置，Model的定义，简单的增加，删除，查询
1. Form使用，包括：Form的定义，Form的布局，HTML代码生成，数据校验，出错处理
1. 模板的使用，包括： {{extend}} 的使用，在模板环境中增加自定义函数，子模板变量定义的
    技巧，错误模板的使用，Python代码的嵌入
1. View的使用，包括：redirect, error的使用, 静态文件处理
1. URL映射的使用，包括：expose的使用，参数定义，与View函数的对应
1. 结构的了解，包括：Uliweb的app组织，settings.ini的简单使用，view函数与模板文件
    的对应关系

这里演示的View的处理还是基于函数的方式 ，在另一篇 [Simple Todo (Uliweb 版本) 之 基础篇](todo_basic.html)
中有如何使用Class方式的View。

