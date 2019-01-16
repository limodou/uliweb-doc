# 0.2.4

* 修正 ORM 与 SQLAlchemy 0.9.1 不兼容的Bug. 旧的写法:

    ```
    cond = None
    cond = (Blog.c.id==5) & None
    ```

    在 0.9.1 中将不是正确的，因为 None 不会被忽略掉（0.8.x 只在 and 时会这样），
    所以你可以将 `cond = None` 改为：

    ```
    from sqlalchemy.sql import true
    cond = true()
    ```

    或者

    ```
    from uliweb.orm import true
    cond = true()
    ```

* 向 functions 中添加 `__contains__` , 这样如果要检查一个 API 是否在 functions
  中存在，只要:

    ```
    'flash' in functions
    ```
* 重构 generic.py, 删除对 `functions.flash` 和 `functions.get_fileserving`
  的缺省依赖。
* 修复在 view 函数中对 `yield` 的支持， 你还可以在 gevent 环境中使用，例如：

    ```
    @expose('/test')
    def test():
        yield "<ul>"
        for i in range(10):
            yield "<li>%d</li>" % (i + 1)
            sleep(1)
        yield "</ul>"
    ```

* 修复 `rawsql()` 在不同数据库引擎中出错的 bug
* 修复 `jsonp()` 在处理中文时的 bug
* 添加 `trim_path()` 函数向 `utils/common.py`这，可以用它将一个路径处理为指定长
  度，过长的部分会转为 `...`

    ```
    >>> a = '/project/apps/default/settings.ini'
    >>> trim_path(a, 30)
    '.../apps/default/settings.ini'
    ```

    缺省的限制长度是 30。
* 在命令行使用了 `-v` 参数时，将输出 ORM 连接信息。并且口令将会替換为 `'*'` ，例如：

    ```
    $>uliweb syncdb -v
    Connection : mysql://blog:***@localhost/blog?charset=utf8

    [default] Creating [1/1, blog] blog...EXISTED
    ```
* 添加 `makeapp` 命令可以一次创建多个 app 的支持，如使用：

    ```
    uliweb makeapp a b c
    ```

    一次创建 `a`, `b`, `c` app。
* 重构 `save_file()` 的处理, 添加 `headers` 和 `convertors` 参数。

    `headers` 用于创建 csv 的头时，以替換原来字段的名字，但是你也可以象下面来
    创建别名：

    ```
    User.c.username.label(u"Name")
    ```

    而 `convertors` 用于转換字段的值，例如：

    ```
    def name(value, data):
        """
        value is the column value
        data is the current record object
        """
        return value + 'test'
    save_file(do_(select([User.c.name])), 'test.csv', convertors={'name':name})
    ```
* 修复 `call_view()` 调用 `wrap_result` bug。