# 模板(Template)

Uliweb目前内置的模板系统采用web2py的，所以语法与web2py的模板系统完全一样。在原基础上进
行了必要的修改。


## 特点


* 简单，易学
* 可以嵌入Python代码
* 不用过分关心Python代码的缩近，只要注意块结束时加pass，模板会自动对缩近进行重排
* Python代码与HTML可以交叉使用
* 支持模板的继承
* 支持类django的block的功能(此功能由Uliweb扩展)
* 提供一些方便的内置方法
* 支持环境的扩展(可以扩展可以直接在模板中使用的对象和方法)
* 先编译成Python代码，然后再执行


## 基本语法

Uliweb的模板的语法很简单，只有以下几种类型的标记：


* `{{= result}}` 这是用来输出的标记。其中result可以是变量也可以是一个函数调用，它会自动  对输出的内容进行转义
* `{{<< result}}` 这是用来输出非转义的内容，与上面相反。
* `{{ ... }}` 只使用{{}}的话表示里面为Python代码，可以是任何的Python代码，如：
    import之类的。如果是块语句，需要在块结束时使用pass。
* `{{extend template}}` 其中template可以是字符串，如 `"layout.html"` 或变量。它表示从父模板继承。
* `{{include template}}` 包括其它的模板。如果template省略，表示是子模板插入的位置。一个父模板只能定义一个插入点。
* `{{block blockname}}{{end}}` 用于定义一个块。在子模板中，对于要覆盖的block需要进行定义，则生成的结果将用子模板中的block定义替换父模板的。
* `{{super}}` 引用父模板。这是当存在扩展父模板的情况下，扩展的块可以通过 `{{super}}` 来引用父模板对应块的内容。
* `{{# ... }}` 单行注释
* `{{## ... ##}}` 片段注释。其中可以包含模板标签。(0.1.6増加) 如:

    ```
    {{##
    {{=name}}
    ##}}
    ```



## 模板环境

Uliweb的模板在运行时也象view一样会运行在一个环境中，在这个环境中，有一些对象和方法是在内置环境中定义的，也有一些是在Uliweb的框架环境中定义的对象或方法。内置的环境你无法扩展，但是框架环境允许你扩展，方法很象view的扩展方式，如在任何一个有效的app的settings.py中可以定义:


```
from uliweb.core.dispatch import bind

@bind('prepare_view_env')
def prepare_template_env(sender, env):
    from uliweb.utils.textconvert import text2html
    env['text2html'] = text2html
```

经过上面的处理，你就可以直接在模板中使用text2html这个方法了。

目前已经有一些缺省的对象和方法可以直接用在模板中，它们目前与view是一样的，因此你可以参考 [视图](views.html) 文档进行了解。


### 环境配置化

不过，直接在 `__init__.py` 中使用 `@bind` 不利于配置化，所以更多是采用写入
`settings.ini` 的 `BINDS` 的方法:


```
[BINDS]
template.prepare_view_env = 'prepare_view_env', 'uliweb.contrib.template.prepare_view_env'
```

其中，key是唯一标识绑定函数的名字，一般的写法是 appname.topic_name 。value是一个
tuple，第一项是 topic 的名字，它一般是在框架中预定义的。这里 `prepare_view_env`
表示view和模板环境初始化处理。第二项是方法路径，它是由：方法对应的模块名.方法名 组成。

同时将程序中的 `@bind('prepare_view_env')` 去掉。


## 内置环境

Uliweb的模板本身已经定义了一些方法可以直接使用。


* out对象 它可以用来输出信息，详见下面的说明。
* `cycle(*args)` 可以在给定的值中进行循环输出，每次返回一个。


## out 对象

out 对象是模板中内置的用来输出文本的对象。你可以在模板中直接使用它，但一般是不需要的。它有以下的方法：


* write(text, escape=True) 输出文本。escape表示是否要进行转义。
* noescape(text) 输出不转义的文本。


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
out.write("<h1>Hello</h1>")
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

同时 extend 支持后面的模板文件名是一个变量，如:


```
{{extend layout}}
```

这样，你可以在渲染模板时，传入一个layout的变量。

另外，在复杂的情况下，可以是多级的模板继承关系，如:


```
           / extend C1
A extend B - extend C2
           \ extend C3
```

也就是说，C1, C2, C3作为父模板，可能有一些相同的block的定义可以扩展，如果它们可重定义的block一样，并且在你的应用中希望统一进行预处理，然后其它的模板再使用这个预处理后的模板。那么可以采用一个新的方法，首先B模板定义为:


```
{{extend layout}}
```

即，它要继承的模板名是一个变量。然后在A中根据需要传入layout的值，如:


```
{{extend "B", layout="C1"}}
```

这样，在扩展B模板时，动态传入了layout变量的值，因此B中的layout将使用C1模板。

**下面的include也有类似的功能** 。


### 引用父模板块内容

假设 B 扩展了 A 模板，重定义了 title 块，如果在 B 中想要引用 A 的内容，则可以使用
`{{super}}` 语法，如:


```
{{extend "A"}}
{{block title}}{{super}} - B{{end}}
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


## uliweb.contrib.template App

Uliweb为了方便使用，同时还提供了 uliweb.contrib.template 这个app，具体的功能描述见 [uliweb.contrib.template](app_template.html) 。


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

