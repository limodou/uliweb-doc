# Generic 说明


## Genric是什么？

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


{% alert class=info %}
本文档附带了一个示例，可以从 uliweb-doc/projects/genric_blog 中找到。
{% endalert %}

## ListView

ListView用来处理列表显示。在最简单的情况下，你可能只需要在view中返回一个结果集，
然后在模板中对它进行展示。不过，这样一些处理将会集中在模板中。而ListView通过丰
富的参数，可以比较方便地进行：设置条件、处理字段、字段值的加工、不同的展示方式、
下载支持等。


### ListView参数说明


```
class ListView(SimpleListView):
    def __init__(self, model, condition=None, query=None, pageno=0, order_by=None,
        fields=None, rows_per_page=10, types_convert_map=None, pagination=True,
        fields_convert_map=None, id='listview_table', table_class_attr='table',
        table_width=True, total_fields=None, template_data=None,
        default_column_width=100, meta='Table', render=None):
```

上面是ListView的初始化函数的定义，可以看到它提供了大量的参数。同时用户也可以根
据需要从ListView类进行派生。ListView是从SimpleListView派生来的，它主要用来处理
与Model相关的列表展示，而SimpleListView主要是处理查询后的结果，不直接与Model
绑定。下面对每个参数进行说明:


model --
    ListView要绑定的Model，这个Model将是显示的主体。

condition --
    查询条件。在执行时，ListView将会按 model.filter(condition)的形式来获得结果
    集。

query --
    结果集。如果用户传入了一个在model上的结果集，则它将结合condition条件，使用
    query.filter(condition)来获得结果。这里就不再是model对象了，而是传入的query
    对象。所以用户要保证这个query是操作model得到的结果集。

order_by --
    对查询结果进行排序。它可以是排序字段的列表，写法要符合sqlalchemy的要求，比如:

    ```
    (Model.c.name, Model.c.age.desc())
    ```

    可以有多个排序字段，可以按升序或降序排序。

pageno --
    页号。ListView支持分页查询。第一页是从0开始。

rows_per_page --
    每页显示的记录条数。

pagination --
    是否使用分页方式的标志。缺省为使用。如果为False则不使用分页方式。

fields --
    用于传入需要显示的字段列表。如果没有给出，则自动使得后面的meta字段所指定的，
    定义在Model中的特殊子类的fields属性。具体的参见下面的关于字段列表定义的说明。

types_convert_map --
    用来定义字段类型与显示值处理函数的映射。具体说明，参见下面关于字段的展示的
    说明。它同下面的fields_convert_map类似，只不过fields_convert_map只处理特定
    名字的字段，只能是一个字段；而types_convert_map是处理特定类型的字段，可能是
    多个字段。

fields_convert_map --
    用来定义字段与显示值处理函数的映射。具体说明，参见下面关于字段的展示的
    说明。

id --
    生成页面时<table>元素的id属性名。

table_class_attr --
    用于指明<table>元素的class属性值。

table_width --
    是否指定表格以像素计算的宽度，如果是，则会根据每列的宽度进行计算总宽度，然后
    设置表格的总宽度。

default_column_width --
    缺省每列的像素宽度，缺省为100px。

total_fields --
    用于合计字段的计算。

template_date --
    将传入模板中的变量dict。

meta --
    如果使用Model中的字段定义，则使用指定名字的子类中的fields属性。缺省为 `'Table'` ，
    你可以指定其它的名字。

render --
    如果不希望ListView按缺省的数据加工方法对数据进行处理，可以传入自定义的render
    函数。它是一个回调，调用形式为: `render(record, obj)` ，record为正在处理的记录，
    它的值是一个二元的tuple，形式为: `(name, display)` 。obj为当前正在处理的对
    象。



### 字段列表定义

在ListView中，用户可以有两种定义列表显示字段的方式：


1. 通过fields字段，传入字段列表
1. 通过在Model类中定义一个子类，来定义字段列表

第一种方法可以在运行时根据需要动态修改显示字段的列表，而第二种相对静态。代码示
例如下:


```
fields = ['name', 'age',
            {'name':'plan_stat','verbose_name':'计划状态', 'width':80},
        ]
```

上面代码是在view代码中定义fields的示例。它支持简单的字段，即只列出字段名称。一
般这种情况下，字段名称在Model中应有对应的属性。比如上例中，应该在传入的Model
对象中有'name, 'age', 'main_sys'这几个字段。对于复杂的字段，如上例中的dict方式
定义的字段，它主要是用于Model中不存在的字段，因此你需要定义以下几个属性:


name --
    字段的名字，英文名

verbose_name --
    显示用的名字。如果没有，则使用name值

width --
    可选，这个是与生成的表格相关的。generic.py缺省可以提供使用<table>生成的清
    单。也支持使用jquery easyui的datagrid生成的表格。这个参数是用来定义列的宽
    度。缺省不定义的话宽度是100px。

sortable --
    可选。这个也是与使用jquery easyui有关的，其它的情况下，要么你从ListView派生
    新的子类，对生成<table>进行了处理，可以考虑定义它，如果不是，则没有什么用。


因此上面name和verbose_name一般是必须的，其它的根据需要来使用。并且，定义哪些值
还和将来展示时使用的包有关系，这块也可以自已去扩展。

第二种方法示例:


```
class Test(Model):
    name = Field(str, max_length=30, verbose_name='姓名')
    age = Field(int, verbose_name='年龄'

    class Table:
        fields = [
            {'name':'name', 'width':150},
            'age',
        ]
```

上面的定义也支持不存在的字段，支持简单定义和复杂定义。


### 执行流程描述

先给出代码示例:


```
def list(self):
    from uliweb.utils.generic import ListView

    def title(value, obj):
        return obj.get_url()

    view = ListView(self.model, fields_convert_map={'title':title})
    return view.run()
```


1. 从 generic 中导入 ListView 。
1. 根据需要对需要传入 ListView 中的参数或回调函数进行处理
1. 创建 ListView 实例
1. 返回 view.run()，它将返回一个 dict ，包含内容为:

    ```
    {'table':以table方式显示的表格数据,
     'table_id':table的id,
     'total':总条数,
     'pageno':当前页号,
     'page_rows':每页显示的条数
    }
    ```

同时它还包含了传入到template_data中的数据。

所以在最简单的情况下，对应的模板可以写为:


```
{{extend "BlogView/layout.html"}}

{{block content}}
<a href="/add">添加Blog</a>
{{<< table}}
{{end}}
```

直接展示 `{{<<table}}` 即可。


### 字段转換

ListView中可以对某个字段的值进行转換，同时这种转換支持对不存在的字段进行处理。
这里要使用 fields_convert_map 这个参数，它是一个 dict ，key就是要转換的字段名，
value是对应的转換函数。转換函数定义为:


```
def convert(value, obj):
```

其中value为对应字段的值，obj为对应的记录对象。你需要返回一个字符串。举例如下:


```
def title(value, obj):
    return '<a href="/view/%d">%s</a>' % (obj.id, value)

fields_convert_map = {'title':title}
view = ListView(model, fields_convert_map=fields_convert_map)
```

这样就可以在显示 title 字段时调用 title() 函数返回一个链接。

如果返回值是 `None` 时，则表示将使用缺省的转換处理。它有着特殊的用途，主要是
在下载处理时。 `ListView` 在下载时，也可以指定 `fields_convert_map` ，但同时
展示时，你也可以也指定 `fields_convert_map` ，这样就存在两个转換映射。 generic
在处理时，会将这两个 `fields_convert_map` 进行合并。但是如果某个convert函数不想
要怎么办，一种方法是删除相应的 key，另一种方法是定义新的convert，简单地让它返回
 `None` 就可以了。

### 不存在字段或自定义字段支持

如果是处理不存在或自定义字段，第一步是在传入的 fields 中或在 class Table 中定义这个字
段的复杂方式，即至少要定义为一个dict，而且包含: name, verbose_name 属性。然后定义
一个convert函数，并且配置到 fields_convert_map 中。要记住，因为字段本身在 Model
中可能不存在，所以 value 是无值的，你只能使用 obj 或通过缺省值来传入其它的参数。
举例:


```
fields = ['title', {'name':'action', 'verbose_name':'操作'}]

def action(value, obj):
    return '<a href="/delete/%d">删除</a>' % obj.id

fields_convert_map = {'action':action}
view = ListView(model, fields_convert_map=fields_convert_map)
```

采用这种方式，我们定义了一个不存在的 action 字段，它的内容是删除链接。


### 跳转到 View 页面

View页面一般是用来显示详细信息的，因此在显示 List 内容时，我们需要某种方法从 List
页面跳转到 View 页面。那么通常的办法就是选一个合适的字段，对它写一个 convert 函数，
返回一个跳转到view页面的链接即可。代码不再提供。


### Ajax请求处理


### 与jquery easyui的结合


### 分页处理

ListView可以分页也可以不分页。缺省情况下 `pagination=True` 表示分页。当处于分页
情况下，用户可以传入pageno和rows_per_page来控制起始的页号和每页显示的条数。如何获
得这些信息，你需要在ListView之外进行获取。


{% alert class=info %}
那么，为什么不将这个处理直接封装到 ListView中呢？因为随着前端使用的控件不同
可能会返回不同的分页关键字，比如有的使用 page和rows。所以你一般要在调用 ListView
之前进行转換。

{% endalert %}

### 查询与条件

在ListView中，第一个参数是Model的名字或类，那么为了返回正确的记录，你还可以传入
condition或query。其中condition对应合适查询条件，而query则对应合适的结果集。最终
的结果将由于传入这些参数而发生变化。整个查询的伪代码为:


```
if 传入了query:
    结果集 = query
else:
    结果集 = self.model.all()
if condition is not None:
    结果集 = 结果集.filter(condition)
if 需要分页:
    结果集 = 结果集.offset((页号-1)*每页条数).limit(每页条数)
```

### 下载处理

ListView 提供下载功能，包括 .csv 和 .xls 下载功能。对于 xls 格式的下载，还需要
安装 xlrd, xlutils, xlwt 这几个 Exccel 读取和写入的模块。

简单的示例：

```
elif 'download' in request.GET:
    def plan_type(value, obj):
        return
    def planedit_status(value, obj):
        return
    
    fields_convert_map = {
        'plan.type':plan_type,
        'planexecute.status':planedit_status,
    }
    return view.download('tasks_planlist.xls', action='download', timeout=0,
        fields_convert_map=fields_convert_map)
```

view为ListView的实例。先根据 URL 来判断是否需要下载，则调用 view 的 `download` 
方法来下载。

download 函数的原型为：

```
def download(self, filename, timeout=3600, action=None, 
    query=None, fields_convert_map=None, type=None, domain=None):
```

参数的说明分别为：

filename --
    下载的文件名。如果后缀为 `.csv` 则自动转为 csv 格式。如果后缀是 `.xls` 则自动
    转为Excel格式。

timeout --
    下载后的文件可以实现缓存。缺省是3600秒钟。在上面的示例中被设置为 0，表示不缓存
    ，这样每次都将重新生成。
    
action --
    可以选择 `'download'`, `'inline'` ，如果是 `'download'` 则浏览器将下载。如果
    是 `'inline'` 则浏览器将直接打开（有些浏览器可能无法支持，主要是针对IE）。

query --
    有时下载的查询语句可能和显示不同，所以这里还可以指定新的查询语句。如果没有指
    定，则使用缺省的查询结果（和显示结果条件相同）。
  
fields_convert_map --
    字段数据转換映射。当希望将某些列的值转为易于理解的方式是，通过定义转換函数来
    实现数据的转換。它将与查询中已经存在的 fields_convert_map 进行合并，而不是简单
    地替換。所以查询时使用的转換函数，在下载时依然可以使用，你只需要定义有变化的
    转換函数即可。
    
type --
    用来指明生成的下载文件的格式，可选值为 `csv` 和 `xls` 。如果没有指定，则根据文件
    名后缀来自动判断。目前仅支持这两种格式。
    
domain --
    当数据中存在 `<a href="xxxx">yyyy</a>` 数据时，并且下载的格式为 xls ，则会自动
    转为Excel中的链接。在转換链接时，domain 将会和链接的地址进行合并处理，这样
    可以把形式为相对路径的链接转为绝对路径。从而在点击时是正确的。

## SimpleListView

因为ListView是针对某个Model的，因此它也有一定的局限，比如在处理复杂的多表关联或
数据加工的结果就无能为力。所以SimpleListView是不与某个Model关联的，也因此你需要
定义一个表头，然后将其传入SimpleListView中。同时在convert中的obj参数值也将不再是
某个Model的对象，而有可能是一个dict或SQLAlchemy的ResultProxy对象。同时SimpleListView
也支持简单的select语句，但是在这种情况下表头还是要定义的。

SimpleListView 是 ListView 的父类，除了不能直接使用 Model 外，基本功能与 ListView 是
一致的。

### 参数说明


```
class SimpleListView(object):
    def __init__(self, fields=None, query=None,
        pageno=0, rows_per_page=10, id='listview_table', fields_convert_map=None,
        table_class_attr='table', table_width=False, pagination=True, total_fields=None,
        template_data=None, default_column_width=100, total=None, manual=False, render=None):
```

SimpleListView的参数和 ListView的差不多，与ListView相似的参数就不再解释了，只
强调一下与ListView不同或新増的参数：


total --
    记录总数。与后面的manual一般联用。这是为了避免通过循环的方式得到记录总数。

manual --
    是否手动传入记录总数。如果不是手动，则表示SimpleListView会自动对结果进行计数，
    它一般是采用循环的方式，这样每次显示都要从头到尾遍历一遍，效率会很低。所以
    可以在外部先统计好再传入，从而提高效率。

## SelectListView(0.1.7新増)

从上面我们可以看到已经有两类的列表展示类： `ListView` 和 `SimpleListView` 。一种
主要是针对一张表的情况，另一种主要是针对自定义结果的情况。还有一种情况就是：我们
希望把一条 `select` 语句作为列表的方式显示出来，这样有可能涉及的表就不只一张，采用
上面的方式就无法满足。因此我们可以考虑 `SelectListView` 。它的主要特点就是：

* 通过定义fields来列举将要在select中显示的字段
* 通过condition来定义条件

这样， `SelectListView` 会自动生成 `select` 语句。

`SelectListView` 是从 `ListView` 继承来的。所以使用上基本上与 `ListView` 是一致的。

### fields定义

定义方式和fields的类似。 `SelectListView` 的第一个参数仍然是 Model 类。每个 fields
项可以是一个字典或是一个字符串。如：

```
fields = [
    'username',
    {'name':'group.id', 'hidden':True},
    {'name':'group.name', 'verbose_name':'小组名称', 'width':150}
]
```

上面即有字符串的形式，也有字典的形式。这里对 `name` 有特殊的要求。如果name中存在
`.` 则 `SelectListView` 会认为是 `model.fieldname` 的形式，因此它会尝试导入 `model`
然后去查看是否存在 `fieldname` 的字段。如果没找到，则视为未定义的字段，将在后续按
`fields_convert_map` 来处理。所以，通过这种方式就可以实现定义不同的表中的字段。

上面的示例中， `hidden` 可以用来控制展示时是否隐藏。

### 数据转換

在显示时，有些值我们想进行必要的数据加工，比如文字改变显示的样式，添加一个链接等，
我们可以定义一个convert函数，如：

```
def _group(value, obj):
    return '<a href="/group/%d">%s</a>' % (obj['group.id'], obj['group.name'])
```

`obj` 在 `SelectListView` 中将是一个 **dict** ，所以你可以直接通过 `obj` 来引用每条记录
中的其它值。所以上述的代码就是根据 `group.id` 和 `group.name` 来生成一个链接。

## AddView


### 参数说明


```
class AddView(object):
    success_msg = _('The information has been saved successfully!')
    fail_msg = _('There are somethings wrong.')
    builds_args_map = {}

    def __init__(self, model, ok_url=None, ok_template=None, form=None,
        success_msg=None, fail_msg=None, use_flash=True,
        data=None, default_data=None, fields=None, form_cls=None, form_args=None,
        static_fields=None, hidden_fields=None, pre_save=None, post_save=None,
        post_created_form=None, layout=None, file_replace=True, template_data=None,
        success_data=None, meta='AddForm', get_form_field=None, post_fail=None,
        types_convert_map=None, fields_convert_map=None, json_func=None,
        file_convert=True, upload_to=None, upload_to_sub=None, 
        fileserving_config='UPLOAD', protect=False, protect_field_name=None):
```


model --
    此AddView所要处理的Model类或名称

ok_url --
    成功后转換的URL地址。注意，它可以是一个回调函数，形式为:

    ```
    def get_url(id):
        return '<a href="/view/%d">查看</a>' % id
    ```

    为什么需要使用回调。因为它是基于这样的处理：在添加完记录后，需要跳转到view页
    面。但是在调用AddView时，因为相应的对象还没有创建，所以没有对应的id，这样就
    没有办法在调用时就传入还不存在的URL。因此采用回调的方式，会将保存后的id传入
    回调函数，这样就可以动态创建新对象的URL地址了。如果不是跳转到view页面，则可
    以考虑不采用回调。

ok_template --
    如果用户没有定义ok_template，并且不是json的返回方式，则将使用这个参数定义的
    模板来展示页面。

form --
    对应的form对象。在缺省情况下，用户不需要传入Form相关的参数，AddView会自动根
    据model、fields或meta参数来自动生成一个Form对象。但是在某些特殊的情况下，也
    可以将一个生成好的form对象传给AddView，这样AddView就不会自动创建Form对象了。

form_cls --
    form是对应Form的对象。而form_cls是对应的Form类本身。AddView会自动使用form_cls
    来创建form对象。使用form_cls的主要作用是定义校验处理，详情见下面的[数据校验处理]。

form_args --
    此参数将在生成Form实例时传入。它是一个dict，主要可以使用的参数如:

    ```
    {'action':提交对应的url,
     'method':提交方法，缺省为POST,
     'html_attrs':创建<form>时将使用的HTML的样式,
            #它也是一个dict，可以使用 {'id':Form的id值, 'class':类名} 等
     'buttons':对应的按钮
    }
    ```


static_fields --
    标识哪些是静态字段。有时我们定义在fiells或AddForm中的字段并不都是需要编辑的，
    而是只读的字段，通过这个参数可以指定哪些是只读字段。不过要注意的是，这些字段
    在用户提交后不会在提交数据中存在。

hidden_fields --
    隐藏字段。指定的字段将生成为 `<input type="hidden" name="field_name" value="xxx"></input>`

success_msg --
    成功后的提示信息。这里AddView会自动调用flash函数。在uliweb中缺省提供了一个
    uliweb.contrib.flashmessage的app，你需要把它加入到settings.ini中的INSTALLED_APPS中去。
    flash的工作原理是通过session来保存下一个页面要显示的内容。所以在返回结果或跳
    转到新页面时，新的页面或模板需要对session中的flash的信息进行处理。如果你使用
    plugs项目，它有一个 ui.jquery.pnofity 的app是flashmessage的jquery的版本，可以
    通过js的方式显示一个弹出窗口来展示，效果要好于flashmessage。因为flashmessage
    是静态信息。

fail_msg --
    出错后的提示消息。

use_flash --
    是否信息提示采用flash方式，缺省为True。如果为False，则不会使用flash函数来显示
    提示信息。

data --
    传入到Form对象中的数据，它将作为初始值传入。如果用户提交后出错，则只会显示
    用户提交的数据。data只是在第一次显示时生效。它是一个dict，key就是对应的字段
    名。value为对应的字段类型的值。

default_data --
    在保存数据到Model中时，如果用户没有输入值，则使用default_data中的数据，它作
    为相应字段的缺省值。与data的区别：data是作为Form的初始值，default_data作为
    Model的初始值。

fields --
    可添加字段的列表。一个Model中可能有很多字段，但不是所有字段都需要在添加时录
    入数据，因此可以通过fields来传入可编辑的字段列表。它也支持添加不存在的字段。
    如果存在，则还需要提供get_form_field回调函数，详情见[处理不存在或自定义字段]的说明。
    fields的处理和ListView的类似，它是一种动态的处理方式。如果是相对静态，可以
    直接在Model中定义一个 AddForm 的class，在其中定义 fields。如果不想用AddForm
    的名字，那么可以通过传入meta参数来改变。

get_form_field --
    如果在fields或AddForm中给出Model中不存在的字段时，AddView会自动调用这个回调
    函数来获得想要的字段对象。具体描述参见下面的[处理不存在或自定义字段]。

pre_save --
    在保存前要执行的回调函数，它的定义为:

    ```
    def pre_save(data):
        ...
    ```

    其中，data是一个dict，并且它将直接会传入到AddView所关联的Model中，所以你可以
    在这里通过修改data的值或添加新的值，从而影响保存到Model的数据。因此可以在这里
    来设置缺省值，或对数据进行进一步加工。

post_save --
    在保存后要执行的回调函数，它的定义为:

    ```
    def post_save(obj, data):
        """
        obj 为保存后创建的对象
        data 为保存时使用的data数据
        """
    ```

    如果在保存完某个对象后，还要进行其它的Model的操作，那么在post_save中是合适的
    位置。

post_created_form --
    在创建完Form实例后将要调用的回调函数。它允许你对生成的Form作进一步的加工，比
    如将原来非必输项的某个字段的required属性改为True，从而变成必输项。它的定义为:

    ```
    def post_created_form(fcls, model):
        """
        fcls 是对应的Form类
        model 是对应的Model类
        """
    ```


layout --
    uliweb中的Form支持不同的布局处理。一个布局是用来处理Form展示的类，它可以决
    定是使用table还是div来展示一个form。具体layout的用途和对应的layout_cls有关。
    详情参见[Form的布局处理]

file_replace --
    AddForm可以支持在上传Form数据时同时上传文件。这个参数用来控制，如果出现同名
    文件时，是否要替換重名的文件。现在Uliweb在上传时，可以控制是不是要对文件名
    进行特殊处理，比如使用UUID来生成文件名。这样其实是不会重名的。但是如果不进
    行特殊处理是有可能重名。如果重名，并且不进行替換，那么文件名会自动在后面添
    加 `(n)` 这样的信息。

file_convert --
    是否对上传的文件名进行转換，如果不转換则将保留原来的文件名。同时结合上面的
    `file_replace` 将会对重名文件进行特殊的处理。

template_data --
    将同时传入模板中的其它的数据。

success_data --
    此参数可以有几个值，它是与返回json数据有关。如果在执行run()时传入了 run(json_result=True)
    则表示返回结果为一个json的数据。这时，如果成功则会根据success_data的值来决定
    返回的json内容。

    True --
        表示使用缺省的结果返回，那么它会简单的调用创建对象的to_dict()方法生成一个
        dict，然后返回。

    function --
        如果要自已加工，则可以传入一个回调函数，形式为:

        ```
        def success_data(obj, data):
            """
            obj为新创建的对象
            data为保存时使用的数据
            """
        ```

        这个函数需要返回一个dict值。



json_func --
    当返回结果为json是，一般情况下会使用uliweb的json函数。但是有些情况，如在ie中使用
    了iframe处理方式来调用jquery的jquery.form插件时，会有问题，原因是json返回的content_type
    不正确。这里不能简单地返回 `application/json` 的类型，而是要返回 `text/html`
    类型，示例代码如:

    ```
    json_func=partial(json, content_type='text/html;charset=utf-8')
    ```


meta --
    静态字段集定义所对应的class名。

post_fail --
    上传数据校验失败后的回调函数处理。

types_convert_map --
    类型转換映射。

fields_convert_map --
    字段转換映射。它与上面的types_convert_map都是用来对静态字段进行转換处理的。
    关于字段转換，详情参见ListView中的[字段转換]说明。

json_func --
    在返回json数据时使用的json函数。缺省为uliweb中的json，在特殊情况下，如需要指
    定json数据的content_type时可以：
    
    ```
    from functools import partial
    partial(json, content_type='text/html;charset=utf-8')
    ```
    
file_convert --
    是否进行文件名转換。在保存文件时，如果置为True，则可以根据文件服务的配置使用
    相应的文件名转换方法对上传的文件进行转換。缺省使用的是UPLOAD的配置。
    
upload_to --
    保存文件时对应的起始目录。缺省是使用UPLOAD的配置地址 `./uploads` 。可以指定为
    其它的目录。
    
upload_to_sub --
    保存文时对应的子目录。它将与 upload_to 合并生成最终的目录。
    
fileserving_config --
    使用哪个文件服务配置，缺省为UPLOAD。
    
protect(0.2.2新増) --
    是否对表单进行保护。缺省为False。当打开时，在展示表单时，将在后台自动生成一个
    token，将其保存在Session中，并将token的值插入到Form的一个隐含字段中。当Form
    下次再提交时，先检查这个token是否存在，如果不存在则报错。如果存在，则取出后删除。
    这样可以防止多次提交。

### 简单代码示例


```
def add(self):
    from uliweb.utils.generic import AddView

    def get_url(id):
        return url_for(BlogView.view, id=id)

    view = AddView(self.model, ok_url=get_url)
    return view.run()
```

这是一段View的代码。它创建了一个AddView，而是定义了一个get_url函数用以响应保存
成功后的URL跳转。

对应的模板为:


```
{{extend "BlogView/layout.html"}}

{{block content}}
<h2>添加</h2>
{{<< form}}
{{end}}
```

View中会返回一个form对象，它就是用来接受用户输入的表格。可以直接在模板中通过
`{{<<form}}` 来显示出来。


### 执行流程描述

在处理完列表展示之后，我们一般要做的第一件事就是添加记录。在添加记录前应该先有一
个入口，我们一般会放在 List 的页面中。作为一个标准的 HTML 的页面编辑的处理，先
考虑采用以下的处理流程:


```
from uliweb import request

self.form = self.make_form(form)    #创建form

if request.method == 'POST':        #如果是POST则表示用户进行了提交
    flag = self.form.validate(request.values, request.files) #对数据进行校验
    if flag:    #返回True，表示校验成功
        d = self.default_data.copy()    #对缺省值进行拷贝
        d.update(self.form.data)        #与提交的数据进行合并
        if self.pre_save:               #处理pre_save回调
            self.pre_save(d)

        r = self.process_files(d)       #处理文件
        obj = self.model(**data)        #保存Model对象
        obj.save()

        if self.post_save:              #处理post_save回调
            self.post_save(obj, d)
        if json_result:                 #如果需要json数据，则进行json化处理
            return to_json_result(True, self.success_msg,
                self.on_success_data(obj, d), json_func=self.json_func)
        else:
            flash = functions.flash     #如果是普通的HTML方式，则获得flash函数
            flash(self.success_msg)     #显示成功信息
            if self.ok_url:             #如果指定了ok_url则进行跳转
                return redirect(get_url(self.ok_url, id=obj.id))
            else:                       #否则根据传入的模板进行处理
                response.template = self.ok_template
                return d
    else:       #返回False，表示校验失败，进行出错处理
        d = self.template_data.copy()   #拷贝模板数据
        data = self.prepare_static_data(self.form.data) #准备静态数据
        self.form.bind(data)            #将数据与Form进行绑定，作为初始值
        d.update({'form':self.form})    #将form对象放入模板数据中
        if self.post_fail:              #处理post_fail回调函数
            self.post_fail(d)
        if json_result:                 #如果需要json数据，则进行json化处理
            return to_json_result(False, self.fail_msg,
                self.form.errors, json_func=self.json_func)
        else:
            flash = functions.flash
            flash(self.fail_msg, 'error')#显示出错信息
            return d
else:                               #显示编辑页面
    data = self.prepare_static_data(self.form.data) #对静态数据进行处理
    self.form.bind(data)            #将数据与Form进行绑定，作为初始值
    return self.display(json_result)#展示页面
```

从上面的流程我们大概可以了解整个AddView所做的处理。上面并不是真正的代码，不过已
经和真正的代码非常接近。简单描述起来，一个添加或编辑处理大概分三个步骤:


1. 如果是 GET 请求，则显示编辑界面
1. 如果是 POST 请求，则对数据进行校验，如果成功则保存，返回结果
1. 如果失败，则返回出错结果

上面的代码之所以看上去复杂，是因为要支持用户的扩展，所以在许多地方都添加了回调
和参数，允许用户对执行过程进行扩展。用户可以根据需要传入不同的回调来进行特殊的
处理。除了采用回调方式外，用户也可以对AddView类进行继承。


### 录入字段的配置

前面说到，AddView支持通过fields参数来设定哪些字段可以编辑，也可以支持在Model中
定义一个AddForm的class，示例如下:


```
class Blog(Model):
    __verbose_name__ = 'Blog'

    #author = Reference('user', verbose_name='作者', required=True)
    create_date = Field(datetime.datetime, verbose_name='发表时间', auto_now_add=True)
    title = Field(str, max_length=255, verbose_name='标题', required=True)
    content = Field(TEXT, verbose_name='内容', required=True)
    deleted = Field(bool, verbose_name='删除标志')

    class AddForm:
        fields = ['title', 'content']
```

这样，在AddForm中我们只定义了两个可录入的字段，其它的字段，要么使用缺省值，要么
可以自动生成，要么是在特殊情况下使用的。


### 处理不存在或自定义字段

如果在添加时希望有一些不在Model中的字段，可以先在fields或AddForm中定义这个字段名，
然后在写一个get_form_field的回调，再将其传入AddView中即可，示例如下:


```
def get_form_field(name):
    #其中name为对应的字段名
    from uliweb.form import StringField

    if name == 'undefined': #这里只是以'undefined'为例，实际可能叫别的
        return StringField('不存在的字段')

fields = ['title', 'content', 'undefeined']
view = AddView('blog', ok_url=get_url, fields=fields,
    get_form_field=get_form_field)
return view.run()
```

上面是通过动态传入fields参数来添加不存在的字段，也可以在Model中的AddForm中定义。


### 数据校验处理

从AddView的功能，我们大概可以了解到它会自动将Model转为一个Form，并且会有一些简单
的校验。如果在Field定义时我们指定了required=True，则这个字段在Form中将成为必输
项，如果用户不输入内容或输入为空的内容，则校验会失败。除了必输项，我们有可能需要
对某个字段或某几个字段进行校验，该如何操作。这里其实就直接使用了Form类本身的校验
功能。Form的校验分为两种，一种是单个字段的校验，一种是多个字段的联合校验。示例
代码如下:


```
class RegisterForm(Form):
    form_buttons = Submit(value=_('Register'), _class="button")
    form_title = _('Register')

    username = StringField(label=_('Username'), required=True)
    password = PasswordField(label=_('Password'), required=True)
    password1 = PasswordField(label=_('Password again'), required=True)
    next = HiddenField()

    def validate_username(self, data):
        from uliweb.orm import get_model

        User = get_model('user')
        user = User.get(User.c.username==data)
        if user:
            return _('User "%s" is already existed!') % data

    def form_validate(self, all_data):
        if all_data.password != all_data.password1:
            return {'password1' : _('Passwords are not match.')}
```

上面是一个用户注册的Form，它要对用户名进行校验，还要对两次输入的密码进行校验。
对于用户名的校验采用了定义一个validate_fieldname的方式，其中fieldname是Form
中的字段。另一种方法是定义form_validate，它可以传入所有数据all_data，这样可以
同时检查多个字段。而validate_fieldname方法，只传入指定的字段值，所以无法同时检
查其它字段的值。如果有错误，对于validate_fieldname则只要返回一行出错原因的文本
即可。而form_validate则要返回一个出错的dict。其中key是出错的字段名。如果返回
None，则认为无错。在简单的情况下，你可以只写一个form_validate即可，所有的校验
都放在这里面处理。

这里的Form只是一个示例，在一般使用AddView或EditView时，你并不需要在Form中定义
任何Field。如果定义的话，它会和Model中的字段同时展示出来。


### Form的布局处理


## 其它说明事项


### URL定义规范

为了处理的一致性，我们一般可以假设CRUD的功能采用以下的URL定义规则，假设我们采用
class-based View的写法，如:


```
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
```

整个View有一个前缀，所以后面的方法都是以这个前缀为基础，你可以根据需要调整路径，
每个功能对应的 URL 为:


list --
    `/prefix` 这里因为 list 对应的URL和前缀是一样的，所以我们使用 `expose('')` 生成
    和前缀一样的 URL。

add --
    `/prefix/add` 这里直接使用class-based的缺省函数映射方式，即: 前缀+'/'+方法

edit --
    `/prefix/edit/<id>` 方法同上

view --
    `/prefix/view/<id>` 方法同上

delete --
    `/prefix/delete/<id>` 方法同上


如果你相把 <id> 放在动作前面，那么你要在每个方法前使用如:  `@expose('<id>/edit')`
这样的方式。如果这个view函数还有其它的decorator，那么你要把 `@expose` 放在前上面，
以保证函数名是正确的。同时其它的 decorator 在处理时一定要保证生成的新的函数名与
原来的函数名是一致的。

