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
    YamlLayout  (基于Yaml CSS框架的布局，不过现在很少用)
    QueryLayout (查询条件使用的Layout)
    
如果你使用Bootstrap作为前端可以考虑使用BoostrapLayout或BootstrapTableLayout。因为
Layout的处理要结合CSS，所以当不满足你的需要时，可以考虑自已来写Layout类。

### 如何使用某个Layout

在定义Form时，通过设置Form类的 `layout_class` 来指明用哪个Layout类。目前缺省是使用
BootstrapLayout。你可以通过:

    from uliweb.form import Form
    Form.layout_class = NewLayout
    
来统一修改所有Form的缺省Layout类，也可以只针对某个Form的子类来修改 `layout_class` 属性。

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
        
    def html(self):
        return '\n'.join([x for x in [self.begin(), self.body(), self.buttons_line(), self.end()] if x])
    
    def __str__(self):
        return self.html()
    
    def get_widget_name(self, f):
        return f.build.__name__
    
    def is_hidden(self, f):
        return self.get_widget_name(f) == 'Hidden'
    
    def begin(self):
        if not self.form.html_attrs['class'] and self.form_class:
            self.form.html_attrs['class'] = self.form_class
        return self.form.form_begin
    
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


    
## get_form (0.1.5 new)

可以方便替换contrib中对于Form的定义，也可以替换一些不同模块下的form，同时也可以增加一些复用。
使用get_form，首先需要向apps/settings.ini中的INSTALLED_APPS中添加'uliweb.contrib.form'，
安装完毕后，在配置文件的FUNCTIONS就引用了get_form这个函数

因此如果想要使用get_form，可以采用下面的方式


```
from uliweb.core.SimpleFrame import functions

Form = functions.get_form('form_name')
...
```

