# API

## functions API

为了方便使用某些方法，在 settings.ini 中定义了常用的一些API：

get_model(model, engine_name=None) --
    返回指定连接的 `model` 对应的Class。如果是字符串值，则需要根据Model配置的要求在settings.ini
    中定义Model的信息才有效果。也可以传入Model的类。
    如果engine_name不为None，则根据给定的engine_name来查找Model。如果不存在，则
    抛出异常。
    如果engine_name为空时，将会智能搜索。如果某个Model只设置了一个数据库连接，
    则自动使用这个连接，如果存在多个则会抛出异常。

get_object(model, id, cache=False, use_local=False) --
    返回某个Model对应的记录。其中 model 为 Model 名，id为对应的记录的id值。如果指定了 `cache=True` ，则可以从 cache
    中获得缓存的值。（它需要与objcache APP相配合，否则无效）如果指定了 `use_local=True` ，则会从本地的内存缓存
    中获得值。它不使用cache，是直接使用内存。它可以与cache合用，则访问顺序是： use_local > cache > db

get_cached_object(model, id, cache=True, use_local=True) --
    它就是 `get_object()` 的一个简写。

## 配置相关 API

uliweb.orm 提供了一些配置相关的 API，用于控制整个uliorm的工作模式。不过，如果
你不是在脱离uliweb的框架环境下来使用orm模块的话，以下的一些方法在settings.ini
中有相应的配置，因此不需要去手工调用相应的函数。但如果是在其它的非uliweb的环境
下使用uliorm，则有可能需要手工调用这些函数来控制uliorm的行为。


set_auto_create(flag) --
    设置是否自动建表。flag取值为True或False。缺省为False。这一功能在开发时比较
    有用，因为可以不使用uliweb syncdb来建表，但是在生产环境中建议关闭，手动来
    处理。

    {% alert class=info %}
    在使用sqlite时，发现有问题。当处于一个事务中，如果出现非select, update
    之类的语句，sqlite会自动提交事务，造成事务处理不是按你的预期，所以也需
    要关闭这个功能。
    {% endalert %}


set_debug_query(flag) --
    设置调试模式。如果flag为True，则生成的SQL语句将输出到日志中。如果你是通过
    `get_connection()` 得到的一个数据库连接对象，可以简单地设置 `db.echo = True`
    来激活调试模式。

set_encoding(encoding) --
    设置缺省编码。缺省为 `utf-8` 。

## 常用 API

get_connection(connection='', engine_name='default', connection_type='long', **args) --
    建立一个数据库连接，并返回连接对象。

    connection需要按SQLAlchemy的要求来编写。
    get_connection既可以支持原来的单数据库连接模式，也可以支持多数据库连接模式，
    还可以通过 `engine_name` 来直接使用某个定义好的连接。



local_connection(engine_name=None, auto_transaction=False): conn --
    返回缓存的数据库连接。如果不存在，则创建。 `auto_transaction` 是用来控制
    是否自动创建事务。

Connect(engine_name=None): None --
    清除缓存的线程连接，保证下次再访问时可以重建连接。

Begin(ec=None): transaction object --
    开始一个事务。如果存在线程连接对象同时如果不存在当前线程内的连接对象，则自动从连接池中取一个连接
    并绑定到当前线程环境中。ec为数据库引擎对象名，如果没提供，则缺省为 'default'.
    ec也可以为连接对象。

Commit(ec=None, trans=None) --
    提交一个事务。使用当前线程的连接对象。

CommitAll() --
    提交所有线程事务。

Rollback(ec=None, trans=None) --
    回滚一个事务。使用当前线程的连接对象。

RollbackAll() --
    回滚所有线程事务。

do_(sql, ec=None) --
    执行一条SQL语句。使用当前的线程连接。只有当使用非ORM的API时才需要使用它
    来处理，比如直接使用SQLAlchemy提供的：select, update, delete, insert时，可
    以这样:

    ```
    from uliweb.orm import do_

    result = do_(select(User.c, User.c.username=='limodou'))
    ```

