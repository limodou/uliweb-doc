=============
Generic 说明
=============

Genric是什么？
---------------

在编写View相关的代码时，我们遇到最多的处理恐怕就是：列表显示、添加、删除、更新、修改
了，一般的叫法是CRUD(Create, Read, Update, Delete)这里没有List。那么Generic的目的
就是把这些常见的处理进行封装，并且它可以和Uliorm相结合，可以比较容易地对表中的
记录进行处理。在Uliweb的utils/generic.py中提供了上述的功能。

generic的整个设计思路是为了将处理程流进行复用。首先是根据按执行的功能分为不同的类。
然后将完整的处理流程封装到类中。但是在实际处理过程中，总会有各种各样的特殊的要求，
因此，你有两种扩展的方式：一种是派生新的类，另一种是将必要的参数和回调传入初始化
函数。一般的方式是采用第二种，因为这种方式相对简单。

generic主要是对Model的界面处理进行了自动化，所以它主要是和Model相结合使用。

在generic中，针对不同的处理提供了不同的View Class，下面分别进行介绍。

.. note::

    本文档附带了一个示例，可以从 uliweb-doc/projects/genric_blog 中找到。

ListView
-----------

ListView用来处理列表显示。在最简单的情况下，你可能只需要在view中返回一个结果集，
然后在模板中对它进行展示。不过，这样一些处理将会集中在模板中。而ListView通过丰
富的参数，可以比较方便地进行：设置条件、处理字段、字段值的加工、不同的展示方式、
下载支持等。

ListView参数说明
~~~~~~~~~~~~~~~~~~~~~~

::

    class ListView(SimpleListView):
        def __init__(self, model, condition=None, query=None, pageno=0, order_by=None, 
            fields=None, rows_per_page=10, types_convert_map=None, pagination=True,
            fields_convert_map=None, id='listview_table', table_class_attr='table', 
            table_width=True, total_fields=None, template_data=None, 
            default_column_width=100, meta='Table', render=None):

上面是ListView的初始化函数的定义，可以看到它提供了大量的参数。同时用户也可以根
据需要从ListView类进行派生。ListView是从SimpleListView派生来的，它主要用来处理
与Model相关的列表展示，而SimpleListView主要是处理查询后的结果，不直接与Model
绑定。下面对每个参数进行说明:

model
    ListView要绑定的Model，这个Model将是显示的主体。
condition
    查询条件。在执行时，ListView将会按 model.filter(condition)的形式来获得结果
    集。
query
    结果集。如果用户传入了一个在model上的结果集，则它将结合condition条件，使用
    query.filter(condition)来获得结果。这里就不再是model对象了，而是传入的query
    对象。所以用户要保证这个query是操作model得到的结果集。
order_by
    对查询结果进行排序。它可以是排序字段的列表，写法要符合sqlalchemy的要求，比如::
    
        (Model.c.name, Model.c.age.desc())
        
    可以有多个排序字段，可以按升序或降序排序。
pageno
    页号。ListView支持分页查询。第一页是从0开始。
rows_per_page
    每页显示的记录条数。
pagination
    是否使用分页方式的标志。缺省为使用。如果为False则不使用分页方式。
fields
    用于传入需要显示的字段列表。如果没有给出，则自动使得后面的meta字段所指定的，
    定义在Model中的特殊子类的fields属性。具体的参见下面的关于字段列表定义的说明。
types_convert_map
    用来定义字段类型与显示值处理函数的映射。具体说明，参见下面关于字段的展示的
    说明。它同下面的fields_convert_map类似，只不过fields_convert_map只处理特定
    名字的字段，只能是一个字段；而types_convert_map是处理特定类型的字段，可能是
    多个字段。
fields_convert_map
    用来定义字段与显示值处理函数的映射。具体说明，参见下面关于字段的展示的
    说明。
id
    生成页面时<table>元素的id属性名。
table_class_attr
    用于指明<table>元素的class属性值。
table_width
    是否指定表格以像素计算的宽度，如果是，则会根据每列的宽度进行计算总宽度，然后
    设置表格的总宽度。
default_column_width
    缺省每列的像素宽度，缺省为100px。
total_fields
    用于合计字段的计算。
template_date
    将传入模板中的变量dict。
meta
    如果使用Model中的字段定义，则使用指定名字的子类中的fields属性。缺省为 `'Table'` ，
    你可以指定其它的名字。
render
    如果不希望ListView按缺省的数据加工方法对数据进行处理，可以传入自定义的render
    函数。它是一个回调，调用形式为: ``render(record, obj)`` ，record为正在处理的记录，
    它的值是一个二元的tuple，形式为: ``(name, display)`` 。obj为当前正在处理的对
    象。
    
字段列表定义
~~~~~~~~~~~~~~~~~~~

在ListView中，用户可以有两种定义列表显示字段的方式：

#. 通过fields字段，传入字段列表
#. 通过在Model类中定义一个子类，来定义字段列表

第一种方法可以在运行时根据需要动态修改显示字段的列表，而第二种相对静态。代码示
例如下::

    fields = ['name', 'age',
                {'name':'plan_stat','verbose_name':'计划状态', 'width':80},
            ]

上面代码是在view代码中定义fields的示例。它支持简单的字段，即只列出字段名称。一
般这种情况下，字段名称在Model中应有对应的属性。比如上例中，应该在传入的Model
对象中有'name, 'age', 'main_sys'这几个字段。对于复杂的字段，如上例中的dict方式
定义的字段，它主要是用于Model中不存在的字段，因此你需要定义以下几个属性:

name
    字段的名字，英文名
verbose_name
    显示用的名字。如果没有，则使用name值
width
    可选，这个是与生成的表格相关的。generic.py缺省可以提供使用<table>生成的清
    单。也支持使用jquery easyui的datagrid生成的表格。这个参数是用来定义列的宽
    度。缺省不定义的话宽度是100px。
sortable
    可选。这个也是与使用jquery easyui有关的，其它的情况下，要么你从ListView派生
    新的子类，对生成<table>进行了处理，可以考虑定义它，如果不是，则没有什么用。
    
因此上面name和verbose_name一般是必须的，其它的根据需要来使用。并且，定义哪些值
还和将来展示时使用的包有关系，这块也可以自已去扩展。

第二种方法示例::

    class Test(Model):
        name = Field(str, max_length=30, verbose_name='姓名')
        age = Field(int, verbose_name='年龄'
        
        class Table:
            fields = [
                {'name':'name', 'width':150},
                'age',
            ]
            
上面的定义也支持不存在的字段，支持简单定义和复杂定义。

执行流程描述
~~~~~~~~~~~~~~~~~~~~~~~~

先给出代码示例::

    def list(self):
        from uliweb.utils.generic import ListView
        
        def title(value, obj):
            return obj.get_url()
        
        view = ListView(self.model, fields_convert_map={'title':title})
        return view.run()

#. 从 generic 中导入 ListView 。
#. 根据需要对需要传入 ListView 中的参数或回调函数进行处理
#. 创建 ListView 实例
#. 返回 view.run()，它将返回一个 dict ，包含内容为::

    {'table':以table方式显示的表格数据,
     'table_id':table的id,
     'total':总条数,
     'pageno':当前页号,
     'page_rows':每页显示的条数
    }
    
   同时它还包含了传入到template_data中的数据。

所以在最简单的情况下，对应的模板可以写为::

    {{extend "BlogView/layout.html"}}
    
    {{block content}}
    <a href="/add">添加Blog</a>
    {{<< table}}
    {{end}}

直接展示 ``{{<<table}}`` 即可。    

字段转換
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ListView中可以对某个字段的值进行转換，同时这种转換支持对不存在的字段进行处理。
这里要使用 fields_convert_map 这个参数，它是一个 dict ，key就是要转換的字段名，
value是对应的转換函数。转換函数定义为::

    def convert(value, obj):
    
其中value为对应字段的值，obj为对应的记录对象。你需要返回一个字符串。举例如下::

    def title(value, obj):
        return '<a href="/view/%d">%s</a>' % (obj.id, value)
        
    fields_convert_map = {'title':title}
    view = ListView(model, fields_convert_map=fields_convert_map)
    
这样就可以在显示 title 字段时调用 title() 函数返回一个链接。

不存在字段支持
~~~~~~~~~~~~~~~~~~~

如果是处理不存在的字段，第一步是在传入的 fields 中或在 class Table 中定义这个字
段的复杂方式，即至少要定义为一个dict，而且包含: name, verbose_name 属性。然后定义
一个convert函数，并且配置到 fields_convert_map 中。要记住，因为字段本身在 Model
中可能不存在，所以 value 是无值的，你只能使用 obj 或通过缺省值来传入其它的参数。
举例::

    fields = ['title', {'name':'action', 'verbose_name':'操作'}]
    
    def action(value, obj):
        return '<a href="/delete/%d">删除</a>' % obj.id
        
    fields_convert_map = {'action':action}
    view = ListView(model, fields_convert_map=fields_convert_map)

采用这种方式，我们定义了一个不存在的 action 字段，它的内容是删除链接。

跳转到 View 页面
~~~~~~~~~~~~~~~~~~~
    
View页面一般是用来显示详细信息的，因此在显示 List 内容时，我们需要某种方法从 List
页面跳转到 View 页面。那么通常的办法就是选一个合适的字段，对它写一个 convert 函数，
返回一个跳转到view页面的链接即可。代码不再提供。

Ajax请求处理
~~~~~~~~~~~~~~~~~~~

与jquery easyui的结合
~~~~~~~~~~~~~~~~~~~~~~~~

分页处理
~~~~~~~~~~~~

ListView可以分页也可以不分页。缺省情况下 ``pagination=True`` 表示分页。当处于分页
情况下，用户可以传入pageno和rows_per_page来控制起始的页号和每页显示的条数。如何获
得这些信息，你需要在ListView之外进行获取。

.. note::

    那么，为什么不将这个处理直接封装到 ListView中呢？因为随着前端使用的控件不同
    可能会返回不同的分页关键字，比如有的使用 page和rows。所以你一般要在调用 ListView
    之前进行转換。

查询与条件
~~~~~~~~~~~~~

在ListView中，第一个参数是Model的名字或类，那么为了返回正确的记录，你还可以传入
condition或query。其中condition对应合适查询条件，而query则对应合适的结果集。最终
的结果将由于传入这些参数而发生变化。整个查询的伪代码为::

    if 传入了query:
        结果集 = query
    else:
        结果集 = self.model.all()
    if condition is not None:
        结果集 = 结果集.filter(condition)
    if 需要分页:
        结果集 = 结果集.offset((页号-1)*每页条数).limit(每页条数)
        
SimpleListView
--------------------

因为ListView是针对某个Model的，因此它也有一定的局限，比如在处理复杂的多表关联或
数据加工的结果就无能为力。所以SimpleListView是不与某个Model关联的，也因此你需要
定义一个表头，然后将其传入SimpleListView中。同时在convert中的obj参数值也将不再是
某个Model的对象，而有可能是一个dict或SQLAlchemy的ResultProxy对象。同时SimpleListView
也支持简单的select语句，但是在这种情况下表头还是要定义的。

参数说明
~~~~~~~~~~~~~

::

    class SimpleListView(object):
        def __init__(self, fields=None, query=None, 
            pageno=0, rows_per_page=10, id='listview_table', fields_convert_map=None, 
            table_class_attr='table', table_width=False, pagination=True, total_fields=None, 
            template_data=None, default_column_width=100, total=None, manual=False, render=None):

SimpleListView的参数和 ListView的差不多，与ListView相似的参数就不再解释了，只
强调一下与ListView不同或新増的参数：

total
    记录总数。与后面的manual一般联用。这是为了避免通过循环的方式得到记录总数。
manual
    是否手动传入记录总数。如果不是手动，则表示SimpleListView会自动对结果进行计数，
    它一般是采用循环的方式，这样每次显示都要从头到尾遍历一遍，效率会很低。所以
    可以在外部先统计好再传入，从而提高效率。
    
AddView
-------------------

展示之后，我们一般要做的第一件事就

其它说明事项
-------------------

URL定义规范
~~~~~~~~~~~~~~

为了处理的一致性，我们一般可以假设CRUD的功能采用以下的URL定义规则，假设我们采用
class-based View的写法，如::

    #coding=utf8
    
    from uliweb import expose
    from uliweb.orm import get_model
    
    @expose('/blog')
    class BlogView(object):
        def __init__(self):
            self.model = get_model('blog')
            
        @expose('')
        def list(self):

        def add(self):
        
        def edit(self, id):
        
        def view(self, id):
        
        def delete(self, id):
        
整个View有一个前缀，所以后面的方法都是以这个前缀为基础，你可以根据需要调整路径，
每个功能对应的 URL 为:

list
    ``/prefix`` 这里因为 list 对应的URL和前缀是一样的，所以我们使用 ``expose('')`` 生成
    和前缀一样的 URL。
add
    ``/prefix/add`` 这里直接使用class-based的缺省函数映射方式，即: 前缀+'/'+方法
edit
    ``/prefix/edit/<id>`` 方法同上
view
    ``/prefix/view/<id>`` 方法同上
delete
    ``/prefix/delete/<id>`` 方法同上
    
如果你相把 <id> 放在动作前面，那么你要在每个方法前使用如:  ``@expose('<id>/edit')``
这样的方式。如果这个view函数还有其它的decorator，那么你要把 ``@expose`` 放在前上面，
以保证函数名是正确的。同时其它的 decorator 在处理时一定要保证生成的新的函数名与
原来的函数名是一致的。

