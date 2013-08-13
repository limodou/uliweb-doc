# Settings说明


## 加载顺序

在Uliweb中，配置信息一般是放在settings.ini文件中的，目前有以下几个级别的settings.ini
信息:


```
default_settings.ini
apps/
    app/settings.ini
    settings.ini
    local_settings.ini
```

从上往下看，我们可以看到有缺省的settings信息，也有app级别的settings信息，还有整
个项目的settings信息，最后是项目的本地settings信息。它们的加载顺序是从上到下。
对于app下的 settings.ini文件，它会按照app在 `INSTALLED_APPS` 中的定义顺序来处理。

## 同名变量处理与强制替换

因此，后加载的项一旦发现有重名的情况，会进行以下特殊的处理:


1. 如果值为list, dict, set，则进行合并处理，即对于list，执行extend()，对于dict
   执行update，同时如果dict的值为dict或list，则会进行递归合并处理。
1. 如果是其它的值，则进行替換，即后面定义的值覆盖前面定义的值
1. 如果写法为:

    ```
    name <= value
    ```

则不管value是什么都将进行替換。


## 基本格式

settings.ini的写法是类ini格式，但是和标准的ini有所区别:


1. 基本写法是:

    ```
    [section]
    name = value
    ```

section --
    节的名字，它应该是一个合法的标识符，即开始为字母或 `_` ，后续可
    以是字母或 `_` 或数字。大小写敏感。

name --
    key，不应包含 '='，可以不是标识符。
    
    {% alert class=danger %}
    name不能与Ini初始化时传入的env中的key重名，如果有会报错。比如不能是 `set`,
    因为 `set` 是作为内置类型在初始化时自动添加到 env 中的。
    {% endalert %}

value --
    值，并且是符合python语法的，因此你可以写list, dict, tuple, 三重字符串和
    其它的标准的python的类型。可以在符合python语法的情况下占多行。也可以是简单
    的表达式。


1. 不支持多级，只支持两级处理
1. 注释写法是第一列为 `'#'`
1. 可以在文件头定义 `#coding=utf-8` 来声明此文件的编码，以便可以使用 `u'中文'` 这样的内容。
1. 可以使用 `_('English')` 这样的翻译字符串

settings中的value只能定义基本的 Python 数据结构和表达式，因为它们将使用 eval 来
执行，所以不能随意写代码，也不能导入其它的模块。在uliweb启动时，将自动向settings
中注入特殊变量，如：

* `_` 此为翻译函数
* `set` 集合type

这些是可以直接使用的。

## 国际化支持

可以直接在settings中使用 `_` 进行语言的翻译。注意应使用在value部分。例如：

```
[DEFAULT]
Project = _('Project')
```

在需要进行翻译时，使用 `i18n` 命令可以自将settings.ini中的翻译串提取出来。

## 配置项引用

在定义 value ，我们可以直接引入前面已经定义好的配置项，有两种类型：

1. section内部引用，即引用的配置项是在同一节中当前配置项之前定义的其它的项，如：

    ```
    [DEFAULT]
    a = 'http://abc.com'
    b = a + '/index'
    ```
    
    一个section内部引用，直接在value部分写对应的配置项名称即可。但是要注意，因为
    key并不要求一定是标识符，所以，如果key的定义不是标识符，则直接引用的话，可能
    会因为eval执行时出错。这样就要使用第二种方法。
    
2. 跨section引用。它需要在配置项前面添加所在的section的名称，如：

    ```
    [DEFAULT]
    a = 'http://abc.com'
    [OTHER]
    b = DEFAULT.a + '/index'
    c = DEFAULT['a'] + '/index'
    d = OTHER.b + '/test'
    ```
    
    上面示例中， `b` 引用了 `DEFAULT` 中的配置项。 `c` 是采用dict下标的写法，适
    用于key不是标识符的情况。 `d` 则是以添加section名字的方式来实现section内部
    引用。

## 字符串引用扩展

引用方式一般是为了解决某个值在多个配置项中重复出现，而采用的减化手段。一般可以
使用表达式的方法进行值的加工。如果是字符串，还可以直接在字符串中定义如 `{{expr}}`
这样的格式串来引用配置项的值。如：

```
[DEFAULT]
a = 'http://abc.com'
b = '{{DEFAULT.a}}/index'
```

在 ``{{}}`` 内的值会自动被替換为相应的配置项的值。这样有时写起来比表达式可能更方便。

## settings的使用

settings在读取后会生成一个对象，要先获得这个对象再使用它。获取settings对象可以
根据不同的场景，使用不同的方法：

1. web环境中，如果是在view函数中进行处理，则直接可以使用settings对象。如：

    ```
    @expose('/index')
    def index():
        return str(settings)
    ```
    
    因为uliweb会自动向所有的view函数注入settings对象，所以可以直接使用。
    
2. 命令行或web环境中非view函数

    最通用的做法，可以在需要使用settings的代码中通过导入来使用settings对象，如：
    
    ```
    from uliweb import settings
    ```
    
    那么建议是在函数内部导入，不要写在模板顶层。这样确保settings在使用时一定被
    创建好了。uliweb会保证settings在创建时，是线程安全的。

有了settings对象，我们就可以调用它的方法和属性来引用配置文件中的各个值了。settings
对象，你可以理解为一个二级的字典或二级的对象树。如果key或section名都是标识符，通
常情况下使用 `.` 的属性引用方式就可以了，不然可以象字典一样使用下标或 `get()` 等
方法来使用。常见的使用方式有:

1. `settings[section][key]` 以字典的形式来处理
1. `settings.get_var('section/key', default=None)` 这种形式可以写一个查找的路径的形式
1. `settings.section` 或 `settings.section.key` 以 `.` 的形式来引用section和key，不过要求section和key是标识符，且不能是保留字。
1. `for k, v in settings.section.items()` 可以把settings.section当成一个字典来使用，因此字典的许多方法都可以使用，如 in, has 之类的。

## 关于settings写入的说明

settings在设计时是希望可以读和写的。读大家很容易理解，但是写的作用是什么呢？

写的作用主要是方便一些工具的自动生成配置。因此在简单情况下， `settings.save(fileobj)`
是可以将当前的settings值保存到某个文件对象中去。

但是由于现在settings的值可以是一个表达式，并且，表达式可以包含变量；另外，由于
存在多个settings.ini文件，并且会对重名的变量名的可变值（list, dict, set）进行合
并处理，使得按原样保存变得困难。所以现在很少进行写入处理，如果要处理，则建议不
使用含变量的表达式，并且只处理一个文件，不处理多个文件。

## 关于Lazy的处理说明

Lazy的处理是在0.2版本中加入的，它是与配置项的引用有关。考虑以下场景：

* 某个app定义了一串配置项，如：

    ```
    [PARA]
    domain = 'http://localhost:8000'
    login_url = domain + '/login'
    ```
* 然后当部署到某个环境中时，用户希望在local_settings.ini中覆盖上面的domain的值
    为实际的地址。
    
这时会有这样的问题：在解析app的settings.ini文件时，domain的值已经解析出来了，因
此在处理login_url时，它的值也就固定下来了。等local_settings.ini再覆盖domain，
login_url已经不会再重新计算了。

所以为了解决因为多个settings.ini按顺序导入，但是变量提前计算的问题，在0.2版本中
引入了Lazy的处理方式。即，在读取多个settings.ini时，并不计算配置项的值，只是放
到这个配置项对应的数组中，等全部读取完毕，由uliweb主动调用settings的freeze()方法
开始对所有未计算的值进行求值。通过这样的方法就延迟了求值的时间，保证了最终想到的
结果。

## 重要配置参数说明

以下按不同的节(section)来区分


### GLOBAL


```
[GLOBAL]
DEBUG = False               #是否当有异常时，输出调试页面
DEBUG_CONSOLE = False       #是否在调试页面上显示console窗，用来输入代码
TEMPLATE_SUFFIX = '.html'   #模板文件后缀
ERROR_PAGE = 'error' + TEMPLATE_SUFFIX #错误页面文件名
WSGI_MIDDLEWARES = []       #WSGI中间件
HTMLPAGE_ENCODING = 'utf-8' #页面文件编码
FILESYSTEM_ENCODING = None  #文件系统编码，在linux上，建议进行相应的设置
DEFAULT_ENCODING = 'utf-8'  #缺省编码
TIME_ZONE = None            #时区设置
LOCAL_TIME_ZONE = None      #本地时区
TEMPLATE_TEMPLATE = ('%(view_class)s/%(function)s', '%(function)s')
                            #不同view方法的模板路径形式，前者为类形式，
                            #后者为函数形式
TEMPLATE_DIRS = []          #全局的模板路径，当所有app中都找不到模板时，将在
                            #这个目录下进行查找
```

其中 `TEMPLATE_TEMPLATE` 用于对应不同的view形式的模板路径方式。对于类，缺省是
在templates下为 `classname/function.html` 的形式。而函数形式的view则直接对应
templates下的 `function.html` 。


### LOG

详情参见 [日志处理说明](log.html) 。


### FUNCTIONS

用于定义公共的一些函数，例如:


```
[FUNCTIONS]
flash = 'uliweb.contrib.flashmessage.flash'
```

在此定义之后，可以有以下两种引用形式:


```
from uliweb import function
flash = function('flash')
flash(message)

#或

from uliweb import functions
functions.flash(message)
```


### DECORATORS

用于定义公共的一些decorator函数，类似于FUNCTIONS的使用方式，但是区分为全部是decorator。

使用形式为:


```
from uliweb import decorators
@decorators.check_role('superuser')
def index():
    pass
```


### BINDS

用于绑定某个信号的配置，例如:


```
[BINDS]
audit.post_save = 'post_save'
```

在配置中，每个绑定的函数应有一个名字，在最简单的情况下，可以省略名字，函数名就
与绑定名相同。

BINDS有三种定义形式:


```
function = topic            #最简单情况，函数名与绑定名相同，topic是对应的信号
bind_name = topic, function #给出信号和函数路径
bind_name = topic, function, {kwargs} #给出信号，函数路径和参数(字典形式)
```

其中function中是函数路径，比如 `appname.model.function_name` ，例用这种形式，uliweb
可以根据 `appname.model` 来导入函数。

上面的 `bind_name` 没有特别的作用，只是要求唯一，一方面利用它可以实现：一个函数
可以同时处理多个 topic 的情况，只要定义不同的 `bind_name` 即可。另一方面，可以
起到替換的作用，如果某个绑定不想再继续使用或替换为其它的配置，可以写一个同名的
`bind_name` 让后面的替換前面的。


### EXPOSES

用于配置URL，在一般情况下，你只要在views.py中定义 `@expose(url)` 即可，但是在复杂情况
下，特别是可以允许URL被替换的情况下，考虑把URL定义在settings.ini中，如:


```
[EXPOSES]
login = '/login', 'uliweb.contrib.auth.views.login'
logout = '/logout', 'uliweb.contrib.auth.views.logout'
```

URL在Uliweb中是可以给每个URL起个名字的，以便在反向获取时只使用这个名字，同时它也可以用来方便进行替換。

它也有三种定义方式，类似于BINDS的定义:


```
function = url            #最简单情况，函数名与url名相同
url_name = url, function  #给出url, 函数路径和url名
url_name = url, function, {kwargs} #给出url，函数路径，url名和参数(字典形式)
```

## pyini模块

整个settings的处理都是由pyini模块来处理的。它存在于uliweb/utils目录下，在程序中
的使用如:


```
from uliweb.utils import pyini

x = pyini.Ini('inifile')
```

这样就可以打开一个ini文件。如果有多个ini文件要进行合并处理，则使用 `read()` 继续处理即可，如:


```
x.read('another.ini')
```

settings.ini文件可以保存，如:


```
x.save()
```

