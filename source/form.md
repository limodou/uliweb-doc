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


## get_form

0.1.5 new

可以方便替换contrib中对于Form的定义，也可以替换一些不同模块下的form，同时也可以增加一些复用。
使用get_form，首先需要向apps/settings.ini中的INSTALLED_APPS中添加'uliweb.contrib.form'，
安装完毕后，在配置文件的FUNCTIONS就引用了get_form这个函数

因此如果想要使用get_form，可以采用下面的方式


```
from uliweb.core.SimpleFrame import functions

Form = functions.get_form('form_name')
...
```

