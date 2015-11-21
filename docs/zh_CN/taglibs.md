# Tag库

## 功能说明

前端一直是很痛苦的事,好在有bootstrap.但是bootstrap一升级又痛苦了,从2.X如果升到3.X有很多标签的
结构和写法都有所调整,因此一直在想如何把HTML的生成标准化,这样中间可以有一个转换层,当底层的CSS框架变
化时,只要把转换改一下就好了.那么现在的实现方案就是提供Tag库.你可以使用它定义出一层抽象的HTML结构,
然后通过转换,最终变成真正的HTML代码.

它的实现处理机制是:

1. 在模板中定义特殊的XML结构,相当于是提供最基础的数据.
2. 在模板解析时,先进行扫描,如果存在这样的XML结构,则先进行转换,然后再进行模板的处理.

这样,Tag的处理有些象预处理.

## 使用说明

### Tag的使用

让我们先说一下Tag的使用.当Tag功能启用时,可以在任意的模板中使用如:

```
<t:breadcrumb>
    <a href="#" title="Home"></a>
    <a href="#" title="Library"></a>
    <a active="active" title="Data"></a>
</t:breadcrumb>
```

这里 `<t:breadcrumb>` 就是一个Tag.其中 `t:` 是用来区别于普通的HTML的Tag.一个Tag可以有子元素.
你可以认为Tag就是一个XML的片段.

上面的例子定义了一个面包屑.其中每个 `<a></a>` 定义了一项, `href` 和 `title` 分别对应链接和显示
名称.对于当前活动项,是不需要 `href` 的,但是需要定义一个 `active="active"`, 其中active的值可
以不是 `"active"`. 上面的结果, **可能** 输出为:

```
<ul class="breadcrumb">
  <li><a href="#">Home</a> <span class="divider">/</span></li>
  <li><a href="#">Library</a> <span class="divider">/</span></li>
  <li class="active">Data</li>
</ul>
```

我们可以看到,Tag的结构进行了扩展.由简单的 `<a></a>` 变成了 `<li><a></a></li>` 的形式.并且 `title`
也写在了标签 `a` 中间.在每个 `<a></a>` 的最后(如果不是最后一个)会添加一个分隔符 `<span class="divider">/</span>`.
在活动的`<li></li>`中就没有 `<a></a>` 了,并且它还有一个 `class` 的属性,值就是前面 `active` 的值.

从这个例子,我们可以看出,Tag主要是为了解决数据与形式的问题.因为现在许多的CSS框架提供了许多控件的结构,但是
它也把可变化的数据和结构混在了一起,而Tag要解决的就是把数据和结构如何有效的分离.

那么我们如何实现上面的 `breadcrumb` 的Tag的实现呢.

### Tag的定义

目前Uliweb支持Tag定义在文件中,一个Tag一个文件.并且Tag文件需要放在App下的taglibs目录中.上面的 `breadcrumb`
的具体的实现可以是:

```
<ul class="breadcrumb">
    {%for i, li in enumerate(a):
        active = li['_attrs'].get('active')
        title = li['_attrs'].get('title')
        href = li['_attrs'].get('href')%}
        {%if active:%}
        <li class="{%=active%}">{%=title%}
            {%if i<len(a)-1:%} <span class="divider">/</span>{%pass%}
        </li>
        {%else:%}
        <li><a href="{%=href%}">{%=title%}</a>
            {%if i<len(a)-1:%} <span class="divider">/</span>{%pass%}
        </li>
        {%pass%}
    {%pass%}
</ul>
```

看着是不是有些复杂.让我一点点来说明.

Tag的转换是对模板中定义的Tag数据进行转换的过程.那么先了解一下,Tag的定义结构会得到什么样的数据?

Tag的处理在 `uliweb.core.taglibs` 中,让我们试一下下面的代码:

```
t = """<t:breadcrumb>
    <a href="#" title="Home"></a>
    <a href="#" title="Library"></a>
    <a active="active" title="Data"></a>
</t:breadcrumb>"""
from uliweb.core.taglibs import parse_xml
print parse_xml(t)
```

会得到:

```
OrderedDict([(u'breadcrumb', {
    u'a': [
        {'_attrs': OrderedDict([(u'href', u'#'), (u'title', u'Home')])},
        {'_attrs': OrderedDict([(u'href', u'#'), (u'title', u'Library')])},
        {'_attrs': OrderedDict([(u'active', u'active'), (u'title', u'Data')])}
    ],
   '_attrs': OrderedDict()})
])}
```

它是一个有序字典,如果简化一下,可以看成是:

```
{'breadcrumb':{
    'a':[
        {'_attrs':{'href':'#', 'title':'Home'}},
        {'_attrs':{'href':'#', 'title':'Library'}},
        {'_attrs':{'active':'active', 'title':'Data'}},
        ],
    '_attrs':{}
    }
}
```

其中 `_attrs` 是某个结点的属性信息,如果有文本,则会是 `_text`(上例中看不出来).同名的子元素会转为
数组,象 `a` 就是数组.

所以我们就可以根据这种结构来进行转换.

再回过头来看看转换的代码.它其实就是uliweb的模板语法,只不过它的标记改为了 `{%%}` ,这是为了不与Tag
中可能有的 `{{}}` 产生冲突.

明白了对Tag的数据的结构以及对应的模板,这段代码应该不难理解.特别要说明,在处理过程中可能要用到的变量和
方法:

`_attrs` --
    某个元素的属性

`_text` --
    某个元素的文本子元素.不过建议都定义为子元素的方式,即用 `<>` 包含起来.

`xml(dict)` --
    将某个dict值转为XML.

`xml_full(tag_name, dict)` --
    将某个dict值转为XML,并用 `<tag_name></tag_name>` 包裹.

让我们再看一个简单的例子:

```
t = """<t:breadcrumb>
    <a href="#" title="Home">Home</a>
</t:breadcrumb>"""

tags = {'breadcrumb':"""
{%<< xml(a)%}
"""}
loader = Loader(tags)
print parse_xml(t)
```

上面的输出结果为:

```
OrderedDict([(u'breadcrumb', {
    u'a': {
        '_text': u'Home',
        '_attrs': OrderedDict([(u'href', u'#'), (u'title', u'Home')])
    },
    '_attrs': OrderedDict()})
    ])
}
```

如果再执行:

```
print parse(t, loader)
```

结果为:

```
Home
```

可以看到 `a` 的文本属性为 `_text` 值为 `u'Home'`.

执行 `xml(a)` 则只是输出它的子结点的内容.如果我们要输出 `<a>` ,则要使用 `xml_full()` 函数,如
上面改为:

```
tags = {'breadcrumb':"""
{%<< xml_full('a', a)%}
"""}
```

再执行:

```
print parse(t, loader)
```

则会得到:

```
<a href="#" title="Home">Home</a>
```

所以当我们编写Tag库时,可以用上面的方法先了解解析后的数据结构,然后根据目标状态来编写模板,最后生成想要的结果.

### 关于子目录

如果Tag文件很多,可能我们想分目录存放.因此你可以在 `taglibs` 中定义子目录,然后将Tag文件放在子目录中,然后
在使用时,需要使用 `子目录.tag_name` 的形式. 如: `<t:bs.breadcrumb>` 就表示在 `taglibs` 目录下的 `bs`
子目录中的 `breadcrumb.html` 文件.

## 后话

因为这个功能刚开发出来,所以还没有积累的可用的Tag库,如果大家有兴趣可以供献出来,比如放在plugs项目中.

