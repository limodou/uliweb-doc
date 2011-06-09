====================================
Simple Todo (Uliweb 版本) 之 基础篇
====================================

本版本是从 http://simple-is-better.com/news/detail-309 来的，原版本基于web.py开
发的，看到这个应用相对简单，因此我将其改造为uliweb的版本。在uliweb版本中，我会列
举详细的开发过程，同时会指出与web.py的一些差异，有兴趣的可以比较。不过，因为我
没有学过web.py，因此只能从原始代码中进行理解，并推测，如果有说得不对的地方欢迎
与我交流，共同学习。

为什么叫基础篇？因为有基础必然有提高篇，其实目前uliweb已经提供了一些相对实用的
模块或app，可以用来快速开发。在提高篇中我希望使用这些内容重新再写一下Todo这个应
用。因此你会看到有关于plugs和generic view的一些使用。

原始的web.py的版本代码可以从上面的网址找到，那么为了简化，我使用了它的一些文件，
比如样式之类的。好，下面让我们开始体验如何使用uliweb开发这样的todo程序。

.. attention::
    关于如何安装uliweb这里不再描述了，有兴趣地找一找Hello, Uliweb文档。
    
    
构建流程
----------

创建项目
===========

进入一个初始目录（假定为$project），开始创建项目。

进入命令行，执行::

    uliweb makeproject simple_todo
    
上面的命令会在$project下创建一个simple_todo的目录，这个就是我们的项目的目录。
    
创建todo App
=============

uliweb的project是由若干个app组成，所以进入simple_todo目录，然后在命令行执行::

    cd simple_todo
    uliweb makeapp todo
    
执行成功后，会在simple_todo/apps下生成一个todo的目录，它就是我们将用来写代码的
主要目录。

功能分析
-----------

通过阅读源码和查看运行结果的画面，我们可以了解到：这个todo可以支持：

* 显示列表（无翻页）
* 显示的同时可以删除和修改
* 在显示页面上可以直接添加

原教程的数据库配置是使用mysql，这里我使用sqlite，因为比较方便。

基本页面布局
--------------

为了实现整体的页面布局效果，这里我会创建一个基础的layout.html，它是其它模板的父
模板。（看了原始代码，好象web.py没有模板继承的概念，因此你会看到一个完整的模板
是分散到index.html, header.html和foot.html中去了，这里我们要重构一下。）

在simple_todo/apps/todo/templates下创建layout.html文件。

templates目录是专门用来存放模板文件的地方。

首先是layout.html，以下是修改后的代码::

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>{{=settings.SITE.SITE_NAME}}</title>
    <link href="{{=url_for_static('styles/reset.css')}}" rel="stylesheet" type="text/css" />
    <link href="{{=url_for_static('styles/index/style.css')}}" rel="stylesheet" type="text/css" />
    </head>
    
    <body>
    <div class="page">
        <div class="header box">
            <h1><a href="/">{{=settings.SITE.SITE_NAME}}</a></h1>
        </div>
        <div class="main box">
        {{block content}}{{end}}
        </div>
        <div class="foot">
            Copyright&copy; {{=settings.SITE.SITE_NAME}} 作者： {{=settings.SITE.EMAIL}}
        </div>
    </div>
    </body>
    </html>

在这里，原来web.py中的变量写法是$config.site_name，变成了{{=settings.SITE.SITE_NAME}}。
在uliweb中，有自已的settings.ini文件，用来存放配置信息，而web.py是使用Python源
文件，uliweb使用类ini文件(**它其实是使用自已定义的pyini的格式**)。    

最重要的一点::

    <div class="main box">
    {{block content}}{{end}}
    </div>

这里定义了一个block，它和django的差不多。不过结束标记不是{{endblock}}而是{{end}}。
原来的web.py版本没有类似的用法。    

再有就是这里了::

    <link href="{{=url_for_static('styles/reset.css')}}" rel="stylesheet" type="text/css" />

使用{{=url_for_static()}}来生成静态链接。原来的程序是使用::

    $config.static/styles/reset.css
    
这是不一样的地方。

.. attention::
    注意，整个uliweb的教程全部使用utf-8编码（主要指模板及程序文件），以后也建议你使用utf-8编码。

静态文件处理
---------------

为了方便，我从原来的版本中拷贝了styles目录到simple_todo/apps/todo/static
中去。

settings.ini配置
------------------

下面配置一下settings.ini文件。

打开simple_todo/apps/settings.ini文件，将其改为::

    [GLOBAL]
    DEBUG = True
    
    INSTALLED_APPS = [
        'uliweb.contrib.staticfiles',
        'todo',
        ]
        
    [SITE]
    SITE_NAME = '任务跟踪'
    EMAIL = 'limodou@gmail.com'

其中在INSTALLED_APPS中添加了todo。 'uliweb.contrib.staticfiles'是用来专门处理
静态文件的app。

然后是定义了SITE，在下面又定义了SITE_NAME和EMAIL。这里可以使用大写或小写。象django
是必须使用大写的。uliweb的settings.ini格式看上去和ini格式差不多，都是以section
为分隔，然后是key=value的形式。不过，这里的value可以是任意简单的python数据结构，
比如dict, list, tuple, string, unicode等。如果第一行加上#coding=<encoding>，还
可以声明这个ini文件的编码格式。

第一次运行
------------

上面的代码目前还无法运行。不过我想看一看大概是什么样了，怎么办。因为目前，我们只
完成了：

* layout.html模板
* settings.ini的基本定义（数据库还没定义）

所以还差得远了。为了运行，我们首先要修改一下simple_todo/apps/todo/views.py，改
为::

    #coding=utf-8
    from uliweb import expose
    
    @expose('/')
    def index():
        return {}

上面的代码，将定义一个views函数。使用@expose来定义它对应的url。这是与web.py和django
不同的地方。在uliweb中，url一般是定义在views.py文件中的，通过decorator与view函数
进行绑定。

上面index()将返回一个{}。那么表示它将使用缺省的模板，模板名就和view函数名一样，
在这里是index。所以我们还需要在todo/templates中定义一个index.html。

本来，index.html中需要定义如果展示todo的内容，但是因为目前数据库等内容还没有创建，
所以我们只想显示空的内容。

在todo/templates下创建index.html，内容为::

    {{extend "layout.html"}}

的确，目前只有这一行代码。它表示从layout.html这个父模板中进行继承。

好，目前差不多了，让我们回到命令行，在simple_todo目录下运行::

    uliweb runserver
    
如果没有错误，则会看到::

    * Loading DebuggedApplication...
    * Running on http://localhost:8000/
    * Restarting with reloader...
    * Loading DebuggedApplication...

说明，开发服务器已经准备完毕了，可以通过访问 http://localhost:8000 来看效果了。
可以看到如下的效果:

.. image:: _static/first.png

添加数据库配置
-----------------

基本架子已经搭好。下面是进行数据库配置。

打开apps/settings.ini，修改为::

    [GLOBAL]
    DEBUG = True
    
    INSTALLED_APPS = [
        'uliweb.contrib.staticfiles',
        'uliweb.contrib.orm',
        'todo',
        ]
        
    [SITE]
    SITE_NAME = '任务跟踪'
    EMAIL = 'limodou@gmail.com'
    
    [ORM]
    CONNECTION = 'sqlite:///database.db'
    AUTO_CREATE = False

这里的重点是添加'uliweb.contrib.orm'这个app，然后是将它要使用的配置信息放在[ORM]
中，这里主要是配置了sqlite数据库，并且使用了相对路径，因此，以后再运行时，database.db
将会在simple_todo这个目录下。

注意AUOT_CREATE=False，它的作用就是当使用某个Model时，不自动创建Model。缺省情况
下是自动创建，这样只要Model不存在，Uliweb就会自动创建。但是发现对于sqlite，如果
在事务中，执行了非select, update, delete等语句，会引发事务自动提交，造成不一致。
因此这里我就把它关掉了。

.. attention::
    Uliweb有自已的ORM，你可以选择使用，也可以选择不使用。这里是使用了自带的ORM。
    同时Uliweb的ORM是基于sqlalchemy开发的，因此上面的数据库连接串是和sqlalchemy
    一致的。
    
原来版本中使用的是mysql，如果你想试一下，可以将上面的CONNECTION的内容改为::

    CONNECTION = 'mysql://todo:123456@localhost/todo?charset=utf8'
    
最后的charset=utf8可以根据需要来选择，这里会强制设置client使用utf8编码。

创建Todo的Model
------------------

有了库，下面就是创建表结构。在todo下创建models.py文件，写入以下内容::

    #coding=utf-8
    from uliweb.orm import *
    
    class Todo(Model):    
        title = Field(str, verbose_name="标题", max_length=255, required=True)
        post_date = Field(datetime.datetime, verbose_name='提交时间', auto_now_add=True)
        finished = Field(bool, verbose_name='是否完成')

这里我们定义了3个字段。因为我没有发现web.py版本中有创建表的内容，所以我根据代码
理解大概有这么几个字段。不过原版本好象没有实现完成状态的设置，所以我这里预留了。

让我看一下代码。在Uliweb中，可以通过从Model派生出新的子类。它和django的Model类似。
不过这里在定义字段时有两种方式，一种是直接使用真正的字段类，如：StringProperty,
DatetimeProperty，不过这种不是很好记忆，而且输入字符比较多，因此还提供简化的定义
方式。通过Field()函数来定义，它的第一个参数是字段的类型，都是基本的Python type对象，
如：str, bool, int, flat, datetime, date等。但是有一些数据库结构中有，但是不存在
对应的Python类型，如：TEXT，等，或需要单独导入的某些特殊的类，如：decimal.Decimal
等，在uliweb，分别定义了大写的类型，如：TEXT, BLOB, DECIMAL可以直接使用。

其它的参数相对直观。对于post_date字段，使用了auto_now_add=True，它的作用就是
当创建新记录时，会自动使用系统当前时间填充，这样你可以不用给它赋值。这一点和
django的一样。

.. attention::
    在定义Model时，我们一般使用首字母大写的单词作为Model的名字。但是uliweb会自
    动将其转为小写。所以Todo类对应的表名，其实是todo。
    
定义完Todo后，我们还有一项配置工作，那就是把Model配置到settings.ini中去。有两种
做法，一种是放到apps/settings.ini中去，但是这样不方便移植，所以还可以放到todo/settings.ini
中去。不过现在没有这个文件，因此让我们创建一个，然后输入以下内容::

    [MODELS]
    todo = 'todo.models.Todo'

key是todo，即真正的表名，值是todo对应的类的路径，格式为：app_name.models.Model_name    

下面，让我们在命令行下创建这个表。其实，如果不设置前面的AUTO_CREATE = False，则
随着运行，Todo表会自动创建，但是现在让我们手工创建，顺便看一看会不会报错。

在命令行下运行::

    uliweb -v syncdb
    
可以看到::

    Creating todo...
    
然后还可以输出相应的建表的sql语句::

    > uliweb sql

    CREATE TABLE todo (
            post_date DATETIME,
            finished BOOLEAN,
            id INTEGER,
            title VARCHAR(255),
            PRIMARY KEY (id),
            CHECK (finished IN (0, 1))
    )
    
如果我们到simple_todo目录下看，可以发现database.db已经创建好了。

等等，上面怎么好象多了一个id的字段。没错，和django一样，uliweb orm会自动为每个
表创建一个id的字段。

显示Todo
-------------

下面开始写展示Todo列表的代码了，让我们先从模板开始。我们需要再次编辑index.html了，
让我们写入下面的代码::

    {{extend "layout.html"}}
    
    {{block content}}
    <div class="box">
        <div class="box todos">
            <h2 class="box">待办事项</h2>
            <ul>
                {{for todo in todos:}}
                    <li>
                        {{=todo.title}}
                        &nbsp;
                        <span class="action">
                            <a href="/todo/edit/{{=todo.id}}">修改</a>,
                            <a href="/todo/delete/{{=todo.id}}" 
                                onclick="return confirm('删除以后不能恢复的，确定？')">删除</a>
                        </span>
                    </li>
                {{pass}}
            </ul>
        </div>
        <div class="box post">
            <h2>新增</h2>
            <form action="/todo/new" method="post" id="post_new">
                <p><input type="text" name="title" class="long_txt" /></p>
                <p><input type="submit" class="submit" value="添加" /></p>
            </form>
        </div>
    </div>
    {{end}}
    
这段代码是我从web.py版本中拷贝并修改的，它主要包含两部分：

#. 显示Todo列表的循环
#. 显示添加新的Todo的内容

第一部分比较简单，我们希望向模板中传入一个todos的变量，它其实是所有todo的一个列表。
然后，在模板中进行循环。Uliweb的模板可以直接写Python代码，所以for后面的':'不要忘了。
同时for结束（包括其它的块语句结束，如：if, def, while等）都要在后面加上{{pass}}，
用来标识块缩近结束。所以在uliweb中你不用考虑缩近，但是要在适应的位置加上{{pass}}。

在循环中，我们会显示Todo的标题，同时展示两个链接。这里我使用了和web.py版本不同的
格式，原来的是/todo/id/edit，看上去更RESTFul一些，我使用的是/todo/edit/id，为什么？
其实也可以和原版本保持一致，不过，我想在views.py中展示如何使用class view的写法，
如何省事，所以就使用了这种格式。写成原来的格式也是可以的。

模板准备好了，下面写views.py了。

最开始我们运行时，我们看到在views.py中定义了一个函数，这是和django相一致的。现在
django 1.3已经支持class方式的view了，Uliweb中也支持类似的方式，不过和django的差
异很大。同时和web.py的方式也不同。我看web.py的方式和django的更接近一些。

通过看原版本代码，web.py的类只用来处理一个URL，同时可以区分不同的方法，如：GET, POST
等。而uliweb对GET, POST的区分是通过URL的定义来实现的，class本身可以同时支持多个URL。
因此，在原版本中，你会在todo.py中看到针对不同的请求，分别定义了：New, Edit, Delete, Index。
而我将只用一个Todo类来定义，增加不同的方法。

views.py 的代码如下::

    #coding=utf-8
    from uliweb import expose
    
    @expose('/todo')
    class Todo(object):
        def __init__(self):
            from uliweb.orm import get_model
            
            self.model = get_model('todo')
        
        @expose('/')    
        def index(self):
            return {'todos':self.model.all()}

我把原来的代码删除了。简单解释一下：

#. 在Uliweb中class view的class可以是new style class，也可以是classic style class，
   不过建议使用new style class。
#. 类上也可以加@expose()，这样，类中所有的方法都会带上这个前缀，除非你覆盖它，正
   如下面的index一样。
#. 你可以在__init__中写一些初始化的代码。上面就是定义了要使用的model。这里get_model()
   的使用是uliweb的一个创新（我认为是这样的）。虽然在前面，我们定义Model的时候好
   象麻烦了点，因此还要修改settings.ini。但是这里就方便了。我们甚至不需要知道
   todo表在哪里，就可以直接导入。
#. 对于index，这里又定义了一个@expose('/')，那么它将会覆盖缺省的URL定义。
#. index将返回一个字典。获得一个Model的所以记录就是Model.all()。这里不象django
   一样，还要加上objects，不需要。
#. 原教程中在列出所有todo时还对id进行了升序排列，但是缺省都是按主键排列，而id正好是
   主键，所以这里我就省了。当然，如果你想加的话可以这样::
    
        self.model.all().order_by(self.model.c.id)
        
   这里的语法完全和sqlalchemy是一致的。在Model中有一个和sqlalchemy Table一样的
   c属性，可以用来引用字段。这里就不多说了。
    
让我们运行一下，刷新一下界面。

不好，报错了，说是使用了“Default Template”，这是怎么回事？

因为我们使用了class view的方式，所以对于模板目录有一个小小的变化，那就是要在
templates中定义一个和Todo一样的目录，然后将index.html放到这个下面。这样，所有
在class view中定义的方法对应的模板都放到相应的类目录中。

改完以后，再运行，结果是这个样子。

.. image:: _static/view_index.png


实现新增Todo
-----------------

只要能添加就好办了。下面写添加代码::

    def new(self):
        title = request.POST.get('title')
        if not title:
            error('标题是必须的')
        todo = self.model(title=title)
        todo.save()
        return redirect(url_for(Todo.index))

注意这是Todo的一个新方法，要注意缩近。解释一下：

#. new上没有定义@expose()，所以它的url将会是/todo/new
#. 有人要问，如果有些方法不想有真正的URL怎么办，那么所有以_开头的方法都不会对应
   一个URL，也就不会被人访问到。
#. 在uliweb，有些方法和变量是全局的，比如上面的：request, error, redirect，都是
   可以直接使用的。如果你想显示地使用它们，可以通过::

        from uliweb import request, error, redirect

#. error目前会引发一个异常，所以并不需要return
#. url_for可以反向获取一个URL，这里传入的是一个函数对应，所以url_for(Todo.index)
   其实就是'/'。这种做法主要是因为：代码结构可能不容易变化，而URL却容易变化，通过
   反向获取，会减少URL变化带来的修改。当然，你可以不用，直接写'/'。
#. 在uliweb中，instance=Model(\*\*kwargs)可以用来创建一条记录，当然要注意使用instnace.save()
   来保存。上面我们没有传入post_date，但是由于在Model定义时，我们加入了auto_now_add，
   所以在创建新记录时，它会自动使用服务器的时间。
#. Uliweb的Request, Response目前是使用werkzeug（和Flask基础是一样的）库。

上面的代码将判断是否有title，如果没有则报错。如果有，则保存。让我们运行一下。

让我们输入：这是一个测试

.. image:: _static/new.png

如果我们什么都不输会怎么样？


怎么回事，又报错！晕啊，程序真是不好写，Uliweb不好玩啊。先看下界面吧:

.. image:: _static/error.png

这是一个调试界面，在Uliweb中使用了werkzeug的调试器，可以在Debug状态下，当出错时
显示出错界面，非常不错。上面的错误就是找不到error.html模板。为什么？因为我们没
有定义这样的一个模板。好吧，让我们在todo/templates下创建一个，因为它不是与class view
对应，所以不需要放在Todo目录下。

创建的error.html代码如下::

    {{extend "layout.html"}}
    
    {{block content}}
        <div class="content">
            <h1 style="font-weight:400;">
                出错了！{{=message}}
            </h1>
            <p>
                <a href="javascript: history.back();">返回</a> |
                <a href="/">首页</a>
            </p>
        </div>
    {{end}}
    
这里放置一个message的变量，它是由error传入的。这个模板与web.py版本不完全一样，原
版本还有自动跳转，我这里没有。

这里我没有特别区分URL是GET还是POST，比如上面的new，如果希望使用POST接收，可以
在new上写::

    @expose(methods=['POST'])

修改Todo
--------------

下面开始处理修改Todo了。首先创建模板吧，在Todo目录下创建edit.html，内容为::

    {{extend "layout.html"}}
    
    {{block content}}
        <div class="box post">
            <h2>修改</h2>
            <form action="" method="post">
                <p><input type="text" name="title" class="long_txt" value="{{=todo.title}}" /></p>
                    <input type="submit" class="submit" value="提交" />
                </p>
            </form>
        </div>
    {{end}}

这里没什么可讲的。

然后是写修改的view代码::

    def edit(self, id):
        todo = self.model.get(int(id))
        if not todo:
            error('没找到这条记录')
        if request.method == 'GET':
            return {'todo':todo}
        else:
            title = request.POST.get('title')
            if not title:
                error('标题是必须的')
            todo.title = title
            todo.save()
            return redirect(url_for(Todo.index))
        
解释一下：

#. 现在edit有一个参数，那么自动生成的URL是什么样的？答案是/todo/edit/<id>，这也
   就是为什么我前面要修改/todo/id/edit的原因，就是为了和class view生成的URL相一致。
#. edit这个函数在编辑时会执行两次，第一次是判断request.method=='GET'时，用于显示。
   第二次是在修改后提交时，用于保存。在web.py的版本中，我们看到它是在Edit这个类中
   通过定义了GET和POST方法来进行区分，而在Uliweb中则通过判断语句来进行区分，功能
   一样，思路有所差别。不过，原来的版本中有关于记录是否存在的判断在GET和POST中
   有相同的代码，而在Uliweb的版本中进行了合并。
#. 使用self.model.get(id)就可以获得一个对象。如果不存在，会返回None，而不是异常。
#. todo.title = title 然后 todo.save() 这是典型的ORM操作。

不过写到这里，和web.py版本有所不同。主要是在成功后，web.py版本会利用error页面，
因为它有自动跳转的功能，来显示成功后的信息。而我删除了，所以在我的版本中不会显示
修改成功后的信息。不过，如果要做有很多种方式 ，比如通过session机制。或使用uliweb
中提供的flashmessage app等。这里就不再演示了。

删除Todo
----------

删除比较简单，不需要处理模板，修改views.py代码::

    def delete(self, id):
        todo = self.model.get(int(id))
        if not todo:
            error('没找到这条记录')
        todo.delete()
        return redirect(url_for(Todo.index))

先检查是否id存在，然后删除，接着重定向。

简单重构
--------------

上面的修改和删除都会判断id是否存在，那么可以提成一个函数，函数以_开头就可以了，
所以views.py的最后版本为::

    #coding=utf-8
    from uliweb import expose
    
    @expose('/todo')
    class Todo(object):
        def __init__(self):
            from uliweb.orm import get_model
            
            self.model = get_model('todo')
        
        @expose('/')    
        def index(self):
            return {'todos':self.model.all()}
        
        def new(self):
            title = request.POST.get('title')
            if not title:
                error('标题是必须的')
            todo = self.model(title=title)
            todo.save()
            return redirect(url_for(Todo.index))
            
        def _get_todo(self, id):
            todo = self.model.get(int(id))
            if not todo:
                error('没找到这条记录')
            return todo
        
        def edit(self, id):
            todo = self._get_todo(id)
            if request.method == 'GET':
                return {'todo':todo}
            else:
                title = request.POST.get('title')
                if not title:
                    error('标题是必须的')
                todo.title = title
                todo.save()
                return redirect(url_for(Todo.index))
                
        def delete(self, id):
            todo = self._get_todo(id)
            todo.delete()
            return redirect(url_for(Todo.index))
            
再说一说URL的定义
-----------------------

因为我使用了class view方式，所以你基本上看不到复杂的URL的定义，那么在web.py的版
本中是如何的呢::

    pre_fix = 'controllers.'
    
    urls = (
        '/',                    pre_fix + 'todo.Index',
        '/todo/new',            pre_fix + 'todo.New',
        '/todo/(\d+)',          pre_fix + 'todo.View',
        '/todo/(\d+)/edit',     pre_fix + 'todo.Edit',
        '/todo/(\d+)/delete',   pre_fix + 'todo.Delete',
    
    )
        
这里可以看到它使用的是正则式，标准的正则式，和django一样。那么如果在Uliweb中定义
象上面的URL会是什么样子::

    /todo/<int:id>
    /todo/<int:id>/edit
    /todo/<int:id>/delete
    
就是这个样子。Uliweb中的URL定义也是来自于werkzeug，它是一种简化的定义方式，我认
为比原始的正则式要简单很多。

后记
----------

非常感谢Ken提供了Todo的web.py的教程，才使得Uliweb版本的教程得以出现。我一直很想
把有关class view的内容讲得更清楚，这次多少涉及了大部分，还有一些没有涉及。另外就
是如何利用我已经实现的一些app来简化开发。从上面的处理可以看到，最基本的就是：CRUD
的操作了。django是通过generic view和admin来实现。Uliweb目前也有一个类似的generic
view的东西，我想有机会在下一个提高教程中向大家展示这个东西。当然，它会基于更多的
依赖，所以未必会适合你，但是却是一个我认为不错的扩展的思路。

写得比较仓促，欢迎与我讨论。程序代码可以从 https://github.com/limodou/uliweb-doc
中的simple_todo中找到，包括我使用sphinx写的教程。