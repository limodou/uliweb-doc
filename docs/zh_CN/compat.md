# 使用_compat.py实现py2,py3的兼容

six是一个比较流行的py2和py3兼容的包，不过它有些大和复杂。在werkzeug中，提供了一个类似的包叫 _compat.py，
它比较轻量。因此uliweb在它的基础上进行了一些定制。那么使用 _compat.py 实现py2和py3的兼容应该如何做？

## 引入future特性

主要是引用 print, unicode, 绝对路径导入相关的future支持，如：

```
from __future__ import print_function, absolute_import, unicode_literals
```

以上导入，将使你的.py文件可以使用 `print()`，字符串缺省认为是unicode。

## 不兼容的语法支持

从 `_compat.py` 中设置了一些py2, py3不兼容的语法支持，主要有：


|name        | 2.x        | 3.x        |
|------------| -----------| -----------|
|unichr      | unichr     |     chr    |
|unicode     | unicode    |     str    |
|range       | xrange     |     range  |
|string_types| (str, unicode) | (str, )|
|pickle      | cPickle    |     pickle |
|input       | raw_input  |     input  |
|open        | open       | from io import open |
|StringIO    | StringIO   | from io import StringIO |
|BytesIO     | BytesIO    | from io import BytesIO |
|pickle      | import cPickle as pickle | import pickle |
|u(转unicode) | 与unicode进行比较| 与str进行比较 |
|b(转bytes) | 与unicode进行比较 | 与bytes进行比较 |
|exec_       | exec 语句   | exec 函数   |
|print       | 语句        | 函数        |
|callable    | callable   | hasattr(x, '__call__' |

示例：

```
from ._compat import input, with_metaclass, string_types
```

## metaclass 支持

示例：

```
from ._compat import with_metaclass

class CommandMetaclass(type):
    def __init__(cls, name, bases, dct):
        option_list = list(dct.get('option_list', []))
        for c in bases:
            if hasattr(c, 'option_list') and isinstance(c.option_list, list):
                option_list.extend(c.option_list)
        cls.option_list = option_list

class Command(with_metaclass(CommandMetaclass)):
    option_list = ()
    help = ''
    args = ''

    def create_parser(self, prog_name, subcommand):
        """
        Create and return the ``OptionParser`` which will be used to
        parse the arguments to this command.

        """
```

## 导入位置结构变动模块

在py3中，有些模块的位置结构发生了变化，或者模块名改为了纯小写，所以为了兼容统一提供了 `import_` 函数，原型为：

```
def import_(module, objects=None, py2=None):
    """
    :param module: py3 compatiable module path
    :param objects: objects want to imported, it should be a list
    :param via: for some py2 module, you should give the import path according the
        objects which you want to imported
    :return: object or module

    Usage:
        import_('urllib.parse', 'urlparse')
        import_('urllib.parse', ['urlparse', 'urljoin'])
        import_('urllib.parse', py2='urllib2')
    """
```

其中 `module` 为按py3的结构定义的模块路径，如 `urllib.parse`，`objects` 为计划导出的对象。`py2` 表示当特殊
情况下， `_compat.py` 未提供缺省映射时，可以指定在py2环境时，使用哪个py2的模块来导入 `objects`。

关于哪些模块可以通用 `import_` 来导入，可以看 `uliweb/utils/_compat.py` 的源码。