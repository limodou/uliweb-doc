# Form使用

在编写Web应用中，经常要使用到的就是和用户的交互，在传统的HTML开发中，一般是使用
Form来进行的，它通过一组Form相关的界面元素，提供各种信息的录入。在ajax的处理过
程中，Form元素也经常被使用。除了前端的展示外，真正的交互是需要后台参与的，它包
括上传数据的解析和处理，然后可能会与数据库进行交互，并返回相应的结果。在Uliweb
中，提供了Form类来进行相关的处理，它的主要功能有:


1. 自动生成前端的展示代码，允许支持自定义布局
1. 对上传后的数据进行校验，如果正确则返回转換后的数据，如果出错，返回出错信息


## Form的定义

在使用Form时，我们做的第一件事就是定义一个Form类，定义之后，我们会创建它的实例，
然后使用这个实例来展示或进行数据的校验处理。一个简单的Form类定义代码如下:


```
from uliweb.form import *

class F(Form):
    title = StringField(label='中文:', required=True, help_string='Title help string')
    content = TextField(label='Content:')
    password = PasswordField(label='Password:')
    age = IntField(label='Age:')
    birthday = DateField(label='Birthday')
    id = HiddenField()
    tag = ListField(label='Tag:')
    public = BooleanField(label='Public:')
    format = SelectField(label='Format:', choices=[('rst', 'reStructureText'), ('text', 'Plain Text')], default='rst')
    radio = RadioSelectField(label='Radio:', choices=[('rst', 'reStructureText'), ('text', 'Plain Text')], default='rst')
    file = FileField(label='file')
```

上面的代码定义了一个Form类，里面有很多的字段，类似于Model的定义。在uliewb/form/uliform.py
中定义了许多Form字段类，分别代表不同类型的字段。所有的字段都继承自 `BaseField` 类，对
于BaseField类的详细说明见下面。

除直接使用类的方式定义Form之外，还可以通过 `make_form` 函数来动态定义。


## BaseField


```
class BaseField(object):
    default_build = Text
    field_css_class = 'field'
    default_validators = []
    default_datatype = None
    creation_counter = 0

    def __init__(self, label='', default=None, required=False, validators=None,
        name='', html_attrs=None, help_string='', build=None, datatype=None,
        multiple=False, idtype=None, static=False, **kwargs):
```

## Form的布局

Form本身只是用来定义用来接受用户输入的数据项，当我们需要将Form转为HTML代码展示在
页面上时，我们可以使用Layout类进行处理。一个Layout类用来处理Form的展示。Layout是基类，
真正使用的是它的子类。在Uliweb中已经缺省实现了若干Layout，分别为：

    Layout  (基类)
    CSSLayout   (使用Div来布局)
    TableLayout   (使用Table来布局)
    BootstrapLayout  (基于Bootstrap, 以div来布局)
    BootstrapTableLayout  (基于Bootstrap，以Table来布局)
    QueryLayout (查询条件使用的Layout)
    
如果你使用Bootstrap作为前端可以考虑使用BoostrapLayout或BootstrapTableLayout。因为
Layout的处理要结合CSS，所以当不满足你的需要时，可以考虑自已来写Layout类。

### 如何使用某个Layout

在定义Form时，通过设置Form类的 `layout_class` 来指明用哪个Layout类。目前缺省是使用
BootstrapLayout。你可以通过:

    from uliweb.form import Form
    Form.layout_class = NewLayout
    
来统一修改所有Form的缺省Layout类，也可以只针对某个Form的子类来修改 `layout_class` 属性。如:

    class MyForm(Form):
        layout_class = NewLayout

在0.5版本之后，layout_class可以是一个字串符，而不是类本身。因此在使用之前需要先将布局类进行
配置，具体配置参见 [Layout类的配置](#layout_setup)

### Layout说明

Layout是基类，它定义了实际使用的Layout的基本属性和要实现的方法。在实际中，你不应该
直接使用它。

```
class Layout(object):
    form_class = ''
    
    def __init__(self, form, layout=None, **kwargs):
        self.form = form
        self.layout = layout
        self.kwargs = kwargs
        self.init()

    def init(self):
        pass

    def html(self):
        return '\n'.join([x for x in [self.begin(), self.hiddens(), self.body(), self.buttons_line(), self.end()] if x])

    def __str__(self):
        return self.html()

    def get_widget_name(self, f):
        return f.build.__name__

    def is_hidden(self, f):
        return f.type_name == 'hidden' or f.hidden

    def begin(self):
        if not self.form.html_attrs['class'] and self.form_class:
            self.form.html_attrs['class'] = self.form_class
        return self.form.form_begin

    def hiddens(self):
        s = []
        for name, obj in self.form.fields_list:
            f = getattr(self.form, name)
            if self.is_hidden(obj):
                s.append(str(f))
        return ''.join(s)
    
    def body(self):
        return ''
    
    def end(self):
        return self.form.form_end
    
    def _buttons_line(self, buttons):
        return ' '.join([str(x) for x in buttons])
    
    def buttons_line(self):
        return str(self._buttons_line(self.form.get_buttons()))
    
    def buttons(self):
        return ' '.join([str(x) for x in self.form.get_buttons()])
```

## Layout 类配置 {#layout_setup}

如果在设置 `layout_class` 时希望使用字符串的形式，需要在settings.ini中配置：

    [FORM_LAYOUT_CLASSES]
    bs3v = '#{appname}.form_helper.Bootstrap3VLayout'
    bs3h = '#{appname}.form_helper.Bootstrap3HLayout'
    bs3t = '#{appname}.form_helper.Bootstrap3TLayout'

上面的示例是设置了三个 Layout 类，其中 `#{appname}` 表示替换为当前的appname。

配置好之后，就可以直接使用字符串的名字了，如：

    class MyForm(Form):
        layout_class = 'bs3v'

## 关于 Bootstrap3 的布局扩展

在 `Uliweb/form/layout.py` 中支持的Bootstrap的布局还是基于2.X版本的，但是因为Bootstrap3
的版本差异比较大，所以不能满足要求。因此在 [uliweb_peafowl](https://github.com/uliwebext/uliweb_peafowl)
项目中新写了几个新的Layout布局类，专门用于Bootstrap 3版本。所以有需要，可以参考并且uliweb_peafowl项目。
    
## get_form (0.1.5)

可以方便替换contrib中对于Form的定义，也可以替换一些不同模块下的form，同时也可以增加一些复用。
使用get_form，首先需要向apps/settings.ini中的INSTALLED_APPS中添加'uliweb.contrib.form'，
安装完毕后，在配置文件的FUNCTIONS就引用了get_form这个函数

因此如果想要使用get_form，可以采用下面的方式


```
from uliweb.core.SimpleFrame import functions

Form = functions.get_form('form_name')
...
```

## make_form 动态创建Form (0.5)

为了方便实现配置化，uliweb提供了动态生成Form的若干种办法，其中可以通过定义简单的数据结构来动态创建一个Form，甚至
包括Layout信息的定义。简单的示例如下：

    from uliweb.form import make_form

    f = {
        'fields':[
            {'name':'username', 'type':'str', 'label':u'用户名', 'placeholder':u'用户名'},
            {'name':'password', 'type':'password', 'label':u'密码', 'placeholder':u'密码'},
            {'name':'remember_me', 'type':'bool', 'label':u'记住我'},
        ],
        'layout_class':'bs3h',
        'layout':{
            'rows':[
                'username',
                'password',
                {'name':'remember_me', 'inline':True, 'label':''},
            ],
            'buttons':[u'<button type="submit" class="btn btn-primary">提交</button>', '<a href="#">忘记密码</a>']
        }
    }

    form_cls = make_form(**f)
    form = form_cls()

以上的代码将创建一个登录Form。动态创建Form类可以使用 `make_form` 函数，它可以使用的参数主要有：

fields --
    用来定义Form的字段，目前支持的所有字段类型可以参见下面的字段类型的详细描述。
layout_class --
    用来指定要使用的Layout类，可以是字段串形式。
layout --
    具体的Layout信息。不同的Layout类可能使用不同的Layout信息，详细要看Layout类的相关说明。
base_class --
    Form的基类。如果提供，新的Form类将是指定基类的子类。主要是考虑动态定义的Form的校验处理，通过
    配置只完成了界面相关的定制，通过基类实现用代码来解决其它的一些不方便配置的功能。
get_form_field --
    根据字段名，动态返回想要的字段类型。这是对于某些在运行时才可以确定字段的情况下使用的。它是一个
    回调函数，形式为： `def func(name, field_info)` ，其中 `name` 是字段名，`field_info`
    是对应的dict信息。
name --
    返回的Form类的名字。如果不提供则缺省为： `MakeForm_`
rules --
    用来定义Form的校验规则，包括前端及后端。后端则会转化为相应的validator的形式，前端校验则需要
    自行编写相应的前端校验代码。


### 常用字段类型



## Form的校验处理 (0.5 Update)

Form的校验的定义有多种形式：

1. 在Form类上，通过rules类属性来定义
2. 在Form类上编写validate_fieldname或form_validate函数来校验，第一种是只校验某个字段，第二种
   是校验整个Form
3. 在定义字段时，传入validators或rules
4. 在make_form时传入rules参数

关于 rules 的处理方式是在 0.5 版本以后才有的。

其中validator是用于后端校验，而rules可以是前端或后端或者两者都要校验。但是要注意的是，因为无法决定
用户使用什么样的前端，所以在这里只是一个定义，并不能真正进行校验，用户需要根据前端校验的规则来自己生成
相应的校验处理代码。所以在使用rules时，后端校验的规则将转为validator函数。而前端校验规则可以通过
`Form.front_rules` 来获取，它的表示形式为：

    {'rules':{
            'fieldname':{
                'rule1':xxx,
            }
        },
     'messages':{
            'fieldname':{
                'rule1':xxx,
            }
        }
    }

单个的rule是一个dict数据结构，形式为：

    {
        'required':(True, 'This field is needed!'),
        'email:front':True，
    }

其中，key为规则名，值可以是tuple, list或单值。如果是tuple或list，则第一个元素是规则所需要的值，
第二个是出错时的错误描述。如果是单值，则使用缺省出错信息。如果规则名后面无 `:` 则表示前后通用。否则
可以通过定义 `:end` 或 `:front` 说明是后端或前端校验使用。

对于设置在Form上或传入 `make_form` 函数的rules参数，定义格式为：

    {
        'fieldname': <单个rule>规则,
        ...
    }

对于 `required` 既可以在 rules 中定义，也可以在定义字段时，设置 `required=True` 参数来设置，
以实现对以前版本的兼容。

### 校验类 (Validator)

Uliweb预定义了一些校验类,可以在uliweb.form.validators中找到以 `TEST_` 开头的类.校验类的基类
是 `Validator`,所有自定义的校验类都需要从这个类进行派生.

```
class Validator(object):
    default_message = _('There is an error!')

    def __init__(self, args=None, message=None, extra=None, next=None, field=None):
        self.message = message or self.default_message
        self.extra = extra or {}
        self.args = args
        self.next = next
        self.result = None
        self.field = field
        self.init()

    def get_message(self):
        if isinstance(self.message, LazyString):
            message = unicode(self.message)
        else:
            message = self.message
        return message % self.extra

    def validate(self, data, all_data=None):
        return True

    def init(self):
        if self.field:
            self.extra['label'] = self.field.label

    def __call__(self, data, all_data=None):
        self.result = data
        if not self.validate(data, all_data):
            return self.get_message()
        if self.next:
            return self.next(self.result)
```

default_message --
    用来定义缺省的提示信息.提示信息中可能会有一些占位符,因此要和 `__init__` 中的 `extra` 参数进行对应.

__init__ --
    初始化函数.

    args --
        用来定义传入的参数,不同的校验类可以传入不同的参数. `args` 的具体类型由校验类自行定义.
    message --
        校验提示信息.如果不提供,则缺省使用 `default_message`.目前message中可以有占位符,支持 `%` 或 `{}`.
        需要使用关键字占位符.
    extra --
        用于提供与消息占位符相匹配的参数.校验类一般会根据args自动分析,但也可以直接提供进行覆盖.类型为 `dict`.
    next --
        表示是否有后续的校验类.用它可以实现多个校验的串接处理.
    field --
        对应的输入字段类.校验类可以用它获取字段中的一些信息,如 `label`,放在extra中.

validate --
    校验处理. `data` 为当前待校验的字段值. `all_data` 为所有待校验的数据.
get_message --
    消息获取函数.
init --
    初始化函数
__call__ --
    供form调用使用

### 自定义校验类

首先从 `Validator` 类派生,然后根据需要覆盖 `default_message`, `__init__` , `init`, `validate` 函数.

## 规则映射

目前针对后端校验，Uliweb定义了一些预置的规则映射，详情如下：

|规则名|校验类|仅后台|
|-----|-----|----|
|required|TEST_NOT_EMPTY| |
|email|TEST_EMAIL| |
|url     |TEST_URL| |
|equalTo |TEST_EQUALTO| |
|in      |TEST_IN | * |
|image   |TEST_IMAGE | * |
|minlength   |TEST_MINLENGTH | |
|maxlength   |TEST_MAXLENGTH | |
|rangelength   |TEST_RANGELENGTH | |
|min   |TEST_MIN | |
|max   |TEST_MAX | |
|range   |TEST_RANGE | |
|date   |TEST_DATE | |
|datetime   |TEST_DATETIME | * |
|time   |TEST_TIME | * |
|number   |TEST_NUMBER | |
|digits   |TEST_DIGITS | |

