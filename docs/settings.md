# Settings说明


## 调用说明

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
个项目的settings信息，最后是项目的本地settings信息。它们的加载顺序是从上到下，
因此，后加载的项一旦发现有重名的情况，会进行以下特殊的处理:


1. 如果值为list, dict，则进行合并处理，即对于list，执行extend()，对于dict执行update
1. 如果是其它的值，则进行替換，即后面定义的值覆盖前面定义的值
1. 如果写法为:

    ```
    name <= value
    ```

则不管value是什么都将进行替換。


## settings.ini格式

settings.ini的写法是类ini格式，但是和标准的ini有所区别:


1. 基本写法是:

    ```
    [section]
    name = value
    ```

其中section是节的名字，可以是一般字符串或标识符。大小写敏感。

    name --
    是key，不应包含 '='

    value --
    是值，并且是符合python语法的，因此你可以写list, dict, tuple, 三重字符串和
        其它的标准的python的类型。可以在符合python语法的情况下占多行。


1. 不支持多级，只支持两级处理
1. 注释写法是第一列为 `'#'`
1. 可以在文件头定义 `#coding=utf-8` 来声明此文件的编码，以便可以使用 `u'中文'` 这样的内容。
1. 可以使用 `_('English')` 这样的编译字符串，_()函数将被定义为 ugettext_lazy
1. 可以使用 `[include:/project/local.ini]` 这样的声明，用来在当前位置引入外部的 ini 文件。

settings的处理是由Uliweb在启动时按照以上的顺序自动解析并且合并的。对于app下的settings.ini文件，它会按照app的定义顺序来处理。


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


## settings的使用

settings在读取后会生成一个对象，它有几种使用方式:


1. `settings[section][key]` 以字典的形式来处理
1. `settings.get_var('section/key', default=None)` 这种形式可以写一个查找的路径的形式
1. `settings.section` 或 `settings.section.key` 以 `.` 的形式来引用section和key，不过要求section和key是标识符，且不能是保留字。
1. `for k, v in settings.section.items()` 可以把settings.section当成一个字典来使用，因此字典的许多方法都可以使用，如 in, has 之类的。

在views方法中，可以直接使用settings对象。在非view方法中，可以先导入再使用:


```
from uliweb import settings
```


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

