=============
template
=============

Uliweb中已经可以自动处理模板了，为什么还要提供template功能？它的作用有以下几点:

#. 提供了一些有关模板处理的配置项
#. 为模板添加了两个新的tag：use和link

模板处理的配置项
------------------

打开uliweb.contrib.template的settings.ini，可以看到::

    [TEMPLATE]
    USE_TEMPLATE_TEMP_DIR = False
    TEMPLATE_TEMP_DIR = 'tmp/templates_temp'
    RAISE_USE_EXCEPTION = True

其中:

USE_TEMPLATE_TEMP_DIR
    表示是否使用编译缓存功能。Uliweb的模板是采用先编译成Python源代码再运行的方式。在缺省情况下，编译后的内容是放在内存中的，使用后就丢弃了。将这个选项置为True，可以将生成的Python源代码保存到一个临时目录下，如果下一次使用时，没有修改模板文件，则不再编译，直接使用缓存的文件进行执行。
    
TEMPLATE_TEMP_DIR
    与上面的选项配套使用。用来指明编译后的模板文件缓存的目录。
    
RAISE_USE_EXCEPTION
    在使用use标签时，如果找不到对应的模块是否抛出异常，缺省为抛出。
    
use 标签
----------------

在处理静态文件时，如css, js文件，比较麻烦的就是你要手工将相关的链接信息写入html中，不仅你要考虑哪些css和js要导入，它们的顺序是如何的，有可能还要考虑对于依赖其它的app的静态文件的处理，比如某个ui组件是依赖于jquery的，应如何处理和避免重复引入。因此template use设计了一种动态导入静态链接的功能，并且可以支持依赖app的静态链接导入。

use 的语法形式为::

    {{use "name"}}
    {{use "name", value1, var2=value2}}
    
use后面为要导入的模块名，并且根据需要可以添加相应的变量。可以是位置参数或关键字参数。一般来说use相关的模板都是由app的提供者写好的，用户只是按要求使用即可。

使用use的好处
~~~~~~~~~~~~~~~~~~~~

你可以自由在模板中使用{{use}}，根据use定义的次序，uliweb会自动安排返回的css, js等代码的顺序。并且会去除重复的内容。如多次使用相同的{{use}}不会有重复的内容出现。并且，它可以自动检查<head>中已经存在的链接，避免重复。

你可以主动定义链接插入的位置，有两种：toplinks和bottomlinks。它们的写法是::

    <!-- toplinks -->
    <!-- bottomlinks -->
    
你可以把它们定义在模板中的任何地方。如果没有定义，那么分两种情况：

#. 存在<head>标签，则toplinks对应于<head>之后。bottomlinks对应于</head>之前。
#. 不存在<head>标签，则全部显示在最前面。

use 使用说明
~~~~~~~~~~~~~~~~~~~~

name为模块名，它需要定义在某个app的 `template_plugins` 目录下，这个目录需要是Python的package的写法(即目录下有一个 `__init__.py`)，文件主名和name是一致，如，name为jquery，则文件名为jquery.py。

以jqutils.py为例，在plugs/ui/jquery/jquitls.py中::

    def call(app, var, env, ajaxForm=False, hoverIntent=False, spin=False):
        a = []
        a.append('jqutils/jqutils.css')
        if spin:
            a.append('jqutils/spin.min.js')
        a.append('jqutils/jqrselect.js')
        a.append('jqutils/jqutils.js')
        if ajaxForm:
            a.append('jqutils/jquery.form.js')
        if hoverIntent:
            a.append('jqutils/jquery.hoverIntent.minified.js')
        return {'toplinks':a, 'depends':[('jquery', {'ui':True})]}

你只要在某个.py中定义一个call函数，use标签在找到后，会自动调用。其中app, var, env是use会根据模板运行环境来提供。后面的参数是与{{use "name",xxxx}}中定义的参数相对应的。use会自动把name后的参数传入到call函数中。

.. note::
    因为uliweb的模板是编译后运行的，因此use中传入的参数只会在编译时生效，在运行时就无效了。所以对于运行时才生效的变量应该通过在view中传入或在模板中进行定义。

在call中，你可以修改env，这样可以添加新的变量，不过目前很少有这么做的。另一个主要的作用就是返回链接信息。这些链接信息可以是.css, .js文件，比如上面的'jqutuils/spin.min.js'。use标签会自动根据后缀是.css, .js的转为静态的链接。其它的保持不变，因此你可以使用::

    a.append('<!--[if lt IE 9]>')
    a.append('bootstrap/asset/html5.js')
    a.append('<![endif]-->')
    a.append('bootstrap/bootstrap.min.css')

传入一些代码片段。

返回时，需要是一个dict，它有两个key，一个是 'toplinks', 一个是 'bottomlinks'。这是和前面所说的toplinks和bottomlinks的定义对应的。同时返回的dict中还可以包含depends或depends_after键字，它是用来指示外部依赖模块的。它的写法就是::

    'depends':['name1', 'name2']
    'depends':[('name1', {'var1':'value1'})]
    
有两种主要写法。第一种是列出外部依赖的use模块，全部是使用缺省参数调用，即只传入app, var, env。第二种是带参数的依赖写法，每项内容为一个tuple，第一个元素是模块名，第二个是一个dict，列出相关要传入的参数。

.. note::
    depends用于定义所依赖的模块在本模块之前被定义。而depends_after用于定义所依赖的模块在当前模块之后被定义，例如:less.js的处理就要在.less文件之后被定义。
    
link 标签
-----------------

使用use是需要有人预先写好相关的模块，它的好处是可以一次性返回多个.css, .js的信息。但是有些情况可有很简单，那么就可以考虑使用link标签，格式为::

    {{link 'path/to/xxx.css', media='screen', to='toplinks'}}
    
其中media对应是'screen'或'print'，缺省为'screen'。to用来指示是输出到toplinks还是bottomlinks。缺省是'toplinks'。