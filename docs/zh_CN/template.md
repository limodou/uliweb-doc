# 模板(Template)

## 0.4 更新说明

从0.4版本开始，uliweb的模板由原来的 web2py 的基础上改造来的，改为基于 tornado 的模板系统。当然
tornado的模板用法与uliweb的还是有不少差异，因此在它的源码上进行了修改。新的模板最大的变化主要是生成
过程，原来uliweb的模板解析与生成是一体化的，所以速度慢。在使用了 wheezy.web 提供的性能测试代码比较
之后非常明显。通过学习tornado等其它的模板示例，发现，它们之所以快，就是因为模板的解析与生成是分离的，
所以解析的时间在根本没有计算，只计算了生成的代码执行的时间，所以当然快了。不过我也没有直接把原来的uliweb
的模板改造成解析与执行分离的模式（其实也是可以做到的），而是基于tornado进行了改造。并且象tornado的模板
会带有一个Loader的类，用来装载模板，还可以实现模板的缓存。不过tornado的缓存机制当文件发生变化时不能
自动更新，要重启服务器。而我改造之后，实现了对依赖文件的时间变化的检查，从而自动更新缓存。当然，也可以
通过配置来关掉自动检查或缓存的机制。实现了解析与执行的分离还有一个好处就是可以在命令行下直接打印出模板
编译后的python代码，非常方便。

不兼容部分说明：

1. `{{super}}` 功能取消
1. `extend` `include` 后面不能使用变量，只能是字符串
1. `{{=}}` `{{<<}}` 后面的 `=` 和 `<<` 前面不能有空格
1. `out` 对象消失，但是为了兼容仍然可能使用 `out.write` 和 `out.xml` ，不过建议改为： `out_write` 和
   `out_write(escape(x))` 的形式
1. 自定义 tag 实现进行了调整， `use` `link` 作为内置的机制，但是具体的处理还是要通过 `template` APP 来支持。
1. template_plugins 中的 call 函数不再传入 `app, var, env` 变量，因此将不能对这些对象进行修改。但
   目前还是兼容了以前的用法
1. 根据新的 tag 定义的要求重新编写了 `rbac` APP 中的 `role` 和 `permission` tag

对 tornado 模板的改造(不能说我的改造就是合理的，但是一是为了兼容，二是为了让用户迁移到新的模板上时代价小)：

1. 实现了对缓存的模板进行依赖检查的功能，如extend, include的其它模板文件的变化，会重新刷新变化的模板及被依赖
   的模板。原tornado则没有这个机制。
1. 缓存使用了简单的 LRU 算法，并且可以控制个数，以避免内存占用过多
1. 实现了多行解析，及缩近重排。tornado主要以单行python代码解析为主，所以多行python代码解析上是有问题的。
   uliweb的新模板为了兼容，实现了多行与单行的同时支持，缺省启用多行模式，它会在最后对代码的缩近进行重新
   处理
1. 实现了对 `def` 块的支持
1. 去除了一些与uliweb不同的功能，如：import , from, raw 等标签的解析


## 特点


* 简单，易学
* 可以嵌入Python代码
* 不用过分关心Python代码的缩近，只要注意块结束时加pass，模板会自动对缩近进行重排
* Python代码与HTML可以交叉使用
* 支持模板的继承
* 支持类django的block的功能
* 提供一些方便的内置方法
* 支持环境的扩展(可以扩展可以直接在模板中使用的对象和方法)
* 先编译成Python代码，然后再执行


## 基本语法

Uliweb的模板的语法很简单，只有以下几种类型的标记：


* `{{= result}}` 这是用来输出的标记。其中result可以是变量也可以是一个函数调用，它会自动对输出的内容进行转义
* `{{<< result}}` 这是用来输出非转义的内容，与上面相反。
* `{{ ... }}` 只使用{{}}的话表示里面为Python代码，可以是任何的Python代码，如：
    import之类的。如果是块语句，需要在块结束时使用pass。
* `{{extend "template"}}` 其中template必需用引号引起来，表示字符串。
* `{{include "template"}}` 其中template必需用引号引起来，表示字符串。
* `{{block blockname}}{{end}}` 用于定义一个块。在子模板中，对于要覆盖的block需要进行定义，则生成的结果将用子模板中的block定义替换父模板的。
* `{{super}}` 0.4中不再支持。
* `{{# ... }}` 单行注释
* `{{## ... ##}}` 片段注释。其中可以包含模板标签。(0.1.6増加) 如:

    ```
    {{##
    {{=name}}
    ##}}
    ```
* `#uliweb-template-tag:begin,end` 单独占一行，并且要写在最开始化，用来定义模板中的标签字符串，如，把 begin
  和end改为 `{%` `%}`
* `out_write` 用于在模板代码片段中输出文本，如果是在HTML片段中可以使用 `{{=}}` 或 `{{<<}}` 来输出。
  此函数缺省不转义，如果要输出转换字符串，可以 `out_write(escape(x))`


## 模板环境

Uliweb的模板在运行时也象view一样会运行在一个环境中，在这个环境中，有一些对象和方法是在内置环境中定义的，
也有一些是在Uliweb的框架环境中定义的对象或方法。内置的环境你无法扩展，但是框架环境允许你扩展，方法很象
view的扩展方式，如在任何一个有效的app的settings.py中可以定义:


```
def prepare_template_env(sender, env):
    from uliweb.utils.textconvert import text2html
    env['text2html'] = text2html
```

然后在 `settings.ini` 中进行配置：

```
[BINDS]
yourapp.prepare_default_env = 'prepare_default_env', 'yourapp.prepare_default_env'
```

经过上面的处理，你就可以直接在模板中使用text2html这个方法了。

上面的 `yourapp.prepare_default_env` 是用来定义一个名字，主要目的是可以方便替换。 `prepare_default_env`
是对应的信号名，表示准备环境变量的信号。 `yourapp.prepare_default_env` 是上面方法的路径。

目前已经有一些缺省的对象和方法可以直接用在模板中，它们目前与view是一样的，因此你可以参考 [视图](views.html) 文档进行了解。


## 内置环境

Uliweb的模板本身已经定义了一些方法可以直接使用。


* `escape()` 可以用来转换HTML的特殊符号，主要是 `<>&` 。
* `out_write()` 在代码片段中向模板输出内容

## 编码

模板缺省是使用utf-8编码进行处理。如果你传入unicode字符串，将自动转为utf-8编码。如果不
是unicode，则不做处理。建议全部使用utf-8编码。


## 用法


### 简单地变量输出


```
{{= "hello"}}
{{= title}}
```

如果使用了变量，则要么由view进行传入，要么在模板的其它地方进行定义，如：


```
{{title="hello"}}
{{= title}}
```


### HTML代码直接输出


```
{{<< html}}
```


### Python代码示例


```
{{import os
out_write("<h1>Hello</h1>")
}}
```


### 模板继承

父模板 (layout.html)


```
<html>
<head>
<title>Title</title>
</head>
<body>
{{block main}}{{end}}
</body>
</html>
```

子模板 (index.html)


```
{{extend "layout.html"}}
{{block main}}
<p>This is child template.</p>
{{end}}
```


### 包括其它的模板


```
<html>
<head>
<title>Title</title>
</head>
<body>
{{include "child.html"}}
</body>
</html>
```


### 模板注释


```
{{# This is a comment line}}
{{# This is another comment line}}
```

可以在每行模板代码前使用 `#` 标识当前行为注释行，其用法同 Python 的注释行


```
{{##
{{=name}}
##}}
```

使用 `{{##` 和 `##}}` 可以注释一个片段，其中可以含有模板标签，这些标签将被
忽略。


### 模板自引用(0.1.4)

假设我们有一个全局性的 layout.html 模板，许多模板都要从它继承以获得最基础的布局信
息等。如果，我们有一个优化要在全局生效，那么我们可能直接想到去修改 layout.html
模板，这的确是一个办法。但是如果这个 layout.html 是一个可以复用的公共模板，它可
能不由你来维护或者它的实现比较通用，如果对其修改会造成不通用，那么直接修改这个
模板可能不是一个好办法。在0.1.4版本中提供了对同名模板的自引用处理机制，它可以用
在 `extend` 和 `include` 中。Uliweb 在处理模板时会根据App的定义顺序来查找模
板。因为模板是定义在不同的app中，因此会有同名模板出现。同时这也正是Uliweb中模板
替換的机制。因此，针对上面的问题，我们可能想在自已的App中定义一个同名的模板，但是
这样只会替換原来的模板。因此我们其实需要的是可以从同名模板的上一个模板继承的机制。
例如：A, B两个App，B定义在A之后，它们都有一个同名的layout.html模板，所以在模板
搜索时，会先找到B/layout.html。在0.1.4中，如果我们在B的layout.html中输入:


```
{{extend "layout.html"}}
```

即和自身的名字相同，在这种情况下，Uliweb会使用A/layout.html作为父模板来继承。这
样，我们就可以象正确的模板继承一样对同名的模板实现继承的处理了。

`{{include}}` 模板时，对应的模板也可以有类似的处理机制。

### 模板的块调试(0.2.2)

Uliweb的模板在结构变得复杂时，了解哪些块是在哪里定义的就变成比较困难的问题。uliweb
提供命令行和运行时对块信息的调试输出。在命令行可以：

```
uliweb find -t index.html --tree --blocks --with-filename
```

可以输出指定模板的继承和包含使用情况。还可以输出其中使用到的block定义，包括每个block
所在的模板文件名。

在运行时，可以打开：

```
[GLOBAL]
DEBUG_TEMPLATE = True
```

这样输出的页面就会有类似：

```
<!-- BLOCK title (apps/theme/templates/theme/skeleton.html) -->
<!-- END title -->
```

这样的输出。不过要注意只用它来进行调试，不然有些地方可能会破块页面或其它非HTML
输出的正确性。

如果要使用动态输出，要注意需要配置 `uliweb.contrib.template` 这个APP，它会在启动
时进行必要的初始化。

## uliweb.contrib.template App

Uliweb为了方便使用，同时还提供了 uliweb.contrib.template 这个app，具体的功能描述见 [uliweb.contrib.template](app_template.html) 。


## 命令行

在 [命令行](manage_guide.html#find) 的文档中有详细的关于模板相关的操作，主要是集中在 `find -t template_file` 中，再配合以不同的
参数。

## 问题描述


### 在模板中定义多行文本的限制

目前模板中不特别支持定义多行的字符串，因为它是按行来处理，并且不作特殊的语法判断的。
比如:


```
{{t = """
<html>
<head>
<script>
if tag == 'a':

</script>
"""}}
```

因为其中有 `if` 语句，所以会被模板识别为Python的 `if` 语句，会造成后面的代
码缩近而产生问题。因此如果多行字符串存在特殊的 `if`, `for` 之类的会引发
缩近的关键字时，可能会引发问题。

