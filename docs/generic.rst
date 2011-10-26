=============
Generic 说明
=============

Genric是什么？
---------------

在编写View相关的代码时，我们遇到最多的处理恐怕就是：列表显示、添加、删除、更新、修改
了，一般的叫法是CRUD(Create, Read, Update, Delete)这里没有List。那么Generic的目的
就是把这些常见的处理进行封装，并且它可以和Uliorm相结合，可以比较容易地对表中的
记录进行处理。在Uliweb的utils/generic.py中提供了上述的功能。

在generic中，针对不同的处理提供了不同的View Class，下面分别进行介绍。

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
            default_column_width=100, meta='Table'):

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