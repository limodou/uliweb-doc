# ORM基本使用

## 使用要求

需要安装sqlalchemy 0.7+以上的版本。如果你使用sqlite，则python 2.6+就自带了。如果
使用其它的数据库，则还需要安装相应的包。sqlalchemy本身是不带的。

## 配置

首先将 `uliweb.contrib.orm` 添加到 `apps/settings.ini` 的 `INSTALLED_APPS` 中去。
`uliweb.contrib.orm` 的settings.ini中已经提供了几个缺省的配置项，用来控制ORM
的行为:


```
[ORM]
DEBUG_LOG = False
AUTO_CREATE = True
AUTO_TRANSACTION_IN_NOTWEB = False
AUTO_TRANSACTION_IN_WEB = False
CHECK_MAX_LENGTH = False
CONNECTION = 'sqlite:///database.db'
CONNECTION_ARGS = {}
CONNECTION_TYPE = 'long'
STRATEGY = 'threadlocal'
PK_TYPE = 'int'
CONNECTIONS = {}
TABLENAME_CONVERTER = None
NULLABLE = True
SERVER_DEFAULT = False
MANYTOMANY_INDEX_REVERSE = False
PATCH_NONE = 'empty'


[MIDDLEWARES]

```

你可以在apps/settings.ini中覆盖它们。

下面对这些配置项分别解释一下：

### DEBUG_LOG

用来切换是否显示SQLAlchemy的日志。如果设置为 `True` ，则SQL语句会输出
到日志中。缺省为 `False` 。

### AUTO_CREATE

用于切换是否可以自动建表。在缺省情况下为 `False` ，但是在测试代码中
可以考虑置为 `True` 以便可以自动建表。当它设为 `False` 时，有几种创建数据库表的方法：

* 通过 `uliweb syncdb` 或 `uliweb reset` 等命令来自动建表。不过 `syncdb` 在执行时，只会对数据库不存在的表进行创建处理，对于已经存在，但是表结构变化的表，不会进行更新处理。而 `reset` 则是先将表 `drop` 掉，再创建，所以总是新的。但是它同时也会将表删除。
* 通过 `uliweb alembic` 命令集来处理。它需要安装 `uliweb-alembic` 包。它可以实现表的创建，表结构的修改等处理，所以建议使用这种方式来处理。
* 手工创建 ，不过手工创建比较麻烦不建议这样的。如果要做，可以先通过 `uliweb sqltable tablename` 命令得到对应的建表SQL语句，然后再手工创建。


{% alert class=info %}
为什么不建议在正式运行时打开自动建表。因为：自动建表每次都要检查数据表是否存在，存在性能问题。同时对于sqlite数据库有一个问题：如果在你执行一个事务时，非查询和更新类的语句
会引发事务的自动提交。而自动建表就是会先查找表是否存在，因此会破坏事务的处理。
{% endalert %}

### AUTO_TRANSACTION_IN_NOTWEB (0.3修改)

用于指示是否在非WEB环境下，当执行 `do_` 时自动启动事务，详情参见下面关于多数据库连接的说明。非WEB环境主要是指守护和批处理，因此建议手工来处理事务。

### AUTO_TRANSACTION_IN_WEB (0.3修改)

用于指示是否在WEB环境下自动启动事务。在添加 `uliweb.contrib.orm` 时，会自动安装 transcation_middleware 中间件，因此在缺省情况下，它会通过中间件的方式来自动创建和处理事务。

### CHECK_MAX_LENGTH

是否当字段为 Varchar 或 Char 时检查max_length参数是否设置。这两种类型分别对应 Uliorm 中的 StringProperty 和 CharProperty，缺省情况下，max_length=255，因此 max_length 其实可以不用定义。但是为了让程序更清晰，可以把这个配置设为 `True` ，这样在定义这两种字段时，max_length 就一定要给出，否则报错。

### CONNECTION

用于设置数据库连接串。它是遵循SQLAlchemy的要求的。（


普通的格式为:


```
driver://username:password@host:port/database
```

示例如下:


```
#sqlite
sqlite_db = create_engine('sqlite:////absolute/path/to/database.txt')
sqlite_db = create_engine('sqlite:///d:/absolute/path/to/database.txt')
sqlite_db = create_engine('sqlite:///relative/path/to/database.txt')
sqlite_db = create_engine('sqlite://')  # in-memory database
sqlite_db = create_engine('sqlite://:memory:')  # the same

# postgresql
pg_db = create_engine('postgres://scott:tiger@localhost/mydatabase')

# mysql
mysql_db = create_engine('mysql://scott:tiger@localhost/mydatabase')

# pymysql
mysql_db = create_engine('mysql+pymysql://scott:tiger@localhost/mydatabase')

# oracle
oracle_db = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')

# oracle via TNS name
oracle_db = create_engine('oracle://scott:tiger@tnsname')

# mssql using ODBC datasource names.  PyODBC is the default driver.
mssql_db = create_engine('mssql://mydsn')
mssql_db = create_engine('mssql://scott:tiger@mydsn')

# firebird
firebird_db = create_engine('firebird://scott:tiger@localhost/sometest.gdm')
```

### CONNECTION_TYPE

用于指明连接模式： `'long'` 为长连接，会在启动时建立。
`'short'` 为短连接，只会在每个请求时建立。缺省值为 `'long'` 即长连接。

### CONNECTION_ARGS

用于除连接串之外的一些参数。SQLAlchemy中，创建引擎时要使用:


```
create_engine(connection, **kwargs)
```

而CONNECTION_ARGS将传入到kwargs中。在某些connection中其实还可以带一些类QUREY_STRING
的东西，如在对mysql的连接中，可以在连接串后面添加 `'?charset=utf8`` 。而这个参
数是会直接传给更底层的mysql的驱动。而CONNECTION_ARGS是传给create_engine的，所以
还是有所不同。

### STRATEGY

连接策略。此为sqlalchemy的连接参数，可以选择的值为 `plain` 和 `threadlocal`.
其中 `threadlocal` 是为了实现无连接的执行。在sqlalchemy中，一般我们在执行sql命令
时或者使用engine或connection来执行。这样有时会感觉比较麻烦。于是如果在创建连接
时使用 `strategy='threadlocal'` 来创建，那么会在线程范围内创建一个共享的连接，
这样在执行sql时只要如:


```
select().execute()
```

就可以了。这就是无连接的执行方式。不过这样的方式在我的使用过程中感觉也有一点问题.
主要就是连接池的问题。uliweb在缺省情况下会采用长连接的策略。于是在执行完一个请求
时会close掉连接，这样可以把连接释放回去。但是发现 threadlocal 方式释放有问题，因为
它是共享的，其实无法真正的释放。所以uliweb在每个请求进来时会主动创建连接，然后在
返回时进行释放。它使用的并不是共享方式的连接。那么共享方式的连接主要是在命令行
或批处理执行时使用比较方便。在View处理中，建议都使用 `do_` 来进行包装。

### PK_TYPE

表示主键ID使用的类型。缺省情况下，ID类型为 Integer, 但是如果数据特别多，则有可能超过Integer的最大值，所以可以通过它改为 `bigint` ，这样范围就更大了。

### CONNECTIONS

数据库多连接设置(详情可以参见 [多数据库连接](multidb.html) 的文档)。uliweb是支持多个数据库连接，自然也支持多个数据库。
为了保持和以前使用方式的兼容。在 `CONNECTIONS` 中一般只要设置非缺省的数据库，
而缺省的数据库仍然使用原来的处理方式。 `CONNECTIONS` 的设置格式为:


```
CONNECTIONS = {
    'test': {
        'CONNECTION':'mysql://root:limodou@localhost/test2?charset=utf8',
        'CONNECTION_TYPE':'short',
    }
}
```

上面代码设置了一个名为 `test` 的连接。 `CONNECTIONS` 本身是一个dict，可以
设置多个连接。每个连接可以使用的参数为:


```
DEBUG_LOG = False
CONNECTION =
CONNECTION_TYPE = 'long'
CONNECTION_ARGS = {}
STRATEGY = 'plain'
```

### TABLENAME_CONVERTER

用来设置文件名转换规则，缺省为 `None` 表示Model类名的小写作为表名。如果你还有其它的要求，可以定义一个函数，然后配置到这个参数中，如：

```
def tablename_converter(name):
	return 't_%s' % name
```

然后配置到settings.ini中：

```
TABLENAME_CONVERTER = 'path.to.tablename_converter'
```

### NULLABLE

字段是否可以为 NULL 的全局设置。缺省为 `True` 表示在定义字段时可以，数据库的值可以为 NULL。你可以通过修改为 `False` 来强制要求所有字段不能为 NULL，也可以针对单个字段传入 `nullable=True` 来设置允许为 NULL。

### SERVER_DEFAULT

建表时，字段的缺省值设置。缺省为 `False` 表示没有指定缺省字段。它是全局设置，当置为 `True` ，每种类型都有自已的缺省值。也可以在定义某个字段时，通过传入 `server_default` 来设置数据库字段的缺省值。关于更详细的说明，参见字段定义时的常见参数说明关于 `server_default` 的说明。

### MANYTOMANY_INDEX_REVERSE

对于 ManyToMany 字段是否要建立反向关系的索引。

例如 A 和 B 两个 Model，在A中定义了一个 bs 的ManyToMany的字段，这样在表中会建立 `(a_id, b_id)` 的一个索引。如果这时 `MANYTOMANY_INDEX_REVERSE` 为 `False`, 则并不会创建一个 `(b_id, a_id)` 的索引。如果置为 `True` 则会创建。如果不想这个功能全局生效，还可以在定义 `ManyToMany` 时传入 `index_reverse＝True` 的参数。

### PATCH_NONE (0.3修改) {#patch}

当你使用 0.9 版本的 SQLAlchemy 时，对于 None 在条件中的处理会发生变化。在 0.8 版本中， 这样的代码 None 是会被忽略掉：

```
condition = None
if xxx:
    condition = (Model.c.id == n) & None
```

但是在 0.9 中，None会转为 `NULL` 从而造成上面的代码为 False，所以要么你将上面的代码改为:

```
from sqlalchemy.sql import true
condition = true()
if xxx:
    condition = (Model.c.id == n) & None
```

如果 PATCH_NONE 为 `'empty'` 时，会保证 0.9 对 None 的处理和 0.8一样。也可以设置它的值为 `'exception'` 这样，在 0.9 版本中，当条件与 None 进行与操作时，会抛出异常。

### MIDDLEWARES

安装 uliweb.contrib.orm app会自动添加 TransactionMiddle ，这样将自动启动事务。



## Model 定义

一般情况下，你应该在app下的models.py中创建Model。从uliweb.orm中导入所有东西，然
后创建自已的Model，它应该从 `Model` 类进行派生。然后添加你想要定义的字段。例如:


```
from uliweb.orm import *
import datetime

class Note(Model):
    username = Field(CHAR)
    message = Field(TEXT)
    homepage = Field(str, max_length=128)
    email = Field(str, max_length=128)
    datetime = Field(datetime.datetime, auto_now_add=True)
```


### 表名

缺省情况下，表名应该是Model类名的小写。比如上面的Note的表名应该是 `note` 。

如果你想设置为其它的表名，你可以在Model类中定义一个 `__tablename__` ，例如:


```
class Note(Model):

    __tablename__ = 't_note'
```

如果存在通用的表名定义规则，可以考虑使用配置参数 `TABLENAME_CONVERTER` 。

### 表的映射(0.1.7新増)

什么叫表的映射，就是它只是现有表的一个映射，在执行syncdb, reset, alembic相关命令
时，不会在数据库中执行create table或drop table的操作。因此，它只是用来映射。

这里，映射的表，可以是真正的表，或者是视图(View)。

它的作用？比如有两个项目，其中一个项目功能比较简单，它将使用另一个项目的表，因此
它本身并不需要建表，只要映射就可以了。因此它只需要把另一个项目的App添加到项目中。
另外，在使用alembic时，因为数据库的表是
由两个项目组成的，所以需要某种方式来区分：哪些表要真正创建，哪些表是已经存在直接
映射即可。因此Uliweb 0.1.7就引入了 `__mapping_only__` 属性。需要时，在Model的类
属性中定义即可，如：

```
class User(Model):
    __mapping_only__ = True
```

不过以上的方式是直接配置到代码中，为了更灵活，也可以在settings.ini中进行配置：

```
[MODELS_CONFIG]
user = {'__mapping_only__':True}
```


### 表参数 {#table_para}

在SQLAlchemy中，当你创建一个表时，你可以传入一些额外的参数，例如: mysql_engin等。
所以，你可以在Model类中定义 `__table_args__` ，例如:


```
class Todo(Model):
    __table_args__ = dict(mysql_charset='utf8')
```


{% alert class=info %}
如在MySQL中修改某张表的存储引擎，可以:

```
__table_args__ = {'mysql_engine':'MyISAM'} #'InnoDB'
```
{% endalert %}

常见的参数定义为：

`__table_args__` --
    将传给底层的 Table 的定义，具体内容符合 SQLAlchemy 的要求
    
`__mapping_only__` --
    用来定义表的映射状态，详情见上面的说明。
    
`__tablename__` --
    用来定义数据库的表名。缺省情况下，表名是 Model 的类名小写形式。如果Model与
    数据库中的表名不同，则可以通过这个属性定义数据库中的名字。在使用时，仍然应
    使用配置名，而不是表名。
    
`__dispatch_enabled__` --
    用来设置是否发出信号，如： `post_save`, `pre_save`, `pre_delete` 等。在不希
    望有人处理这些事件时考虑设置。还可以通过调用 `set_dispatch(False)` 来实现全
    局性的禁止，主要是用在批处理中。
    
`__cacheable__` --
    在使用 get() 方法时，如果 `__cacheable__` 为 True，则自动进行缓存处理，如使
    用uliweb内置的 objcache APP 来处理。则 `get(id)` 相当于 `get(id, cache=True)`
    
注意，这些参数都可以定义在 settings.ini 中。

### OnInit 方法

uliorm也允许你在创建表之时在一些初始化工作。只要写一个OnInit的class method，例
如:


```
class Todo(Model):
    @classmethod
    def OnInit(cls):
        Index('my_indx', cls.c.title, cls.c.owner, unique=True)
```

上面的代码是用来创建复合索引。一般的单字段索引，可以在定义字段时直接指定Index=True。


### default_query 方法

uliorm目前支持用户自定义缺省条件，即在查询时，会自动将缺省条件与输入的条件合并
处理，它需要定义为一个类方法，如:


```
class Todo(model):
    @classmethod
    def default_query(cls, query):
        return query.filter(xxx).order_by(yyy)
```

default_query 将传入一个query对象，你可以对它使用Result上的查询相关的处理，比如:
`filter`, `order_by`, `limit`, `offset` 等可以返回结果集的方法。

不过，一旦定义了 default_query 所有的 filter 查询都会使用这个结果，除非你使用 `filter().without()` 来显示指时不需要 default_query 的处理。


### 字段定义

uliorm中定义一个Model的字段为Property，但为了方便，uliorm还提供了Field函数。

所有的字段都是以Property结尾的类。下面是uliorm中的字段类:


```
'BlobProperty', 'BooleanProperty', 'DateProperty', 'DateTimeProperty',
'TimeProperty', 'DecimalProperty', 'FloatProperty',
'IntegerProperty', 'Property', 'StringProperty', 'CharProperty',
'TextProperty', 'UnicodeProperty', 'FileProperty', 'PickleProperty'
```

你可能认为它们不好记忆，所以你可以使用Field来定义。

Field是一个函数，它的第一个参数可以是内置的Python type，也可以是uliorm定义的特殊
类型。其它的参数是和对应的Property类一致的。它会根据你传入的Python type或特殊类
型来自动查找匹配的字段类。

Python type和字段类的对应关系为:


|| 引用简写类型 || 实际类型 ||
|| str || StringProperty, ||
|| CHAR || CharProperty, ||
|| unicode || UnicodeProperty, ||
|| TEXT || TextProperty, ||
|| BLOB || BlobProperty, ||
|| FILE || FileProperty ||
|| int || IntegerProperty, ||
|| float || FloatProperty, ||
|| bool || BooleanProperty, ||
|| datetime.datetime || DateTimeProperty, ||
|| datetime.date || DateProperty, ||
|| datetime.time || TimeProperty, ||
|| decimal.Decimal || DecimalProperty, ||
|| DECIMAL || DecimalProperty, ||
|| PICKLE || PickleProperty, ||

小写的，都是Python内置的类型或类。大写的都是uliorm为了方便记忆而创建的。而上面
看到的关于Node的示例就是使用Field来定义字段的。


### ID 属性

缺省情况下，uliorm会自动为你添加一个 `id` 字段，而你并不需要在Model中进行定义。

如果你不想自动定义ID，则可以在Model添加一个类属性 `__without_id__` 则 uliorm
将不会自动创建 id 属性。


### Property 构造函数

Property 其它所有字段类的基类。所以它的一些属性和方法将会被派生类使用到，它的定
义为:


```
Property(verbose_name=None, fieldname=None, default=None, required=False,
    validators=None, choices=None, max_length=None, hint='',
    auto=None, auto_add=None, type_class=None,
    type_attrs=None, placeholder='', extra=None, 
    sequence=False, server_default=None,
    nullable=__nullable__, index=None, unique=False,
    primary_key=False, autoincrement=False)
```


verbose_name --
    用于显示字段的描述信息。一般是用在显示界面上。

fieldname --
    数据库字段名。缺省情况下和Property的实例名相同。例如:

    ```
    class User(Model):
        username = StringProperty(fieldname='user_name')
    ```

    username就是Property的实例名，而fieldname缺省不给出的话就是 `username`, 上面的
    示例是指定了一个不同的值。因此你通过orm引用属性时要使用 `username`，但是
    直接对数据库查询或操作时，即要使用 `user_name`。在特殊情况下代码中的字段名可能
    和数据库中的字段名不同。

    {% alert %}
    原来此参数名为 name ，后为了清晰表示fieldname，增加了fieldname参数和属性，原来
    的name将不允许直接赋值，它将直接和Property属性的名字相同。主要是在直接处理Property
    实例时，可以根据name来获得Model字段的名字。
    {%endalert%}

default --
    字段的缺省值。注意，default可以是一个函数。在创建一个Model的实例时，对于未
    给出值的属性，uliorm会自动使用default给字段赋值。因此，如果default没有赋值，
    则这个值一般为None。但是对于象IntegerProperty之类的特殊字段来说，缺省值不是None，如
    0。同时，在调用时要注意default函数执行是否可以成功。因为有的时候需要
    在某个环境下，而你在执行时可能不具备所要求的环境，比如default函数要处理request.user，
    但是你有可能在批处理中去创建实例，这样request.user是不会存在的，因此会报错。
    简单的处理就是把Model.field.default置为None。
    
    default 并不影响建表语句，所以如果想实现建表的default定义，需要使用 `server_default` 。

required --
    指明字段值是否不能为None。如果在创建Model实例时，没有传入required的字段值，
    则uliorm会检查出错。同时这个属性可以用在Form的处理中。

validators --
    当给一个属性赋值时，uliorm会根据这个参数来校验传入值的合法性。它应该是一个
    函数，这个函数应写为:

    ```
    def validator(data):
        xxx
        if error:
            raise BadValueError, message
    ```

    如果校验失败，这个函数应该抛出一个 BadValueError的异常。如果成功，则返回
    None或不返回。

hint --
	 用来定义一个帮助信息，可以用在form中作为Form字段的help_string的值。
	 
auto --
	 可以是一个函数。表示在Update时，如果没提供值则自动设置auto。
	 
auto_add --
	 与 auto 类似，不同之处在于，它只是在Insert时起作用。default的取值是不关心作什么操作的，而 auto 和 auto_add 要关心具体的操作。
	 
choices --
    当属性值的取值范围是有限时可以使用。它是一个list，每个元素是一个二元tuple，
    格式为(value, display)，value为取值，display为显示信息。目前，uliorm并不用
    它来校验传入数据的正确性，用户可以根据需要自定义校验函数，传入validators中
    进行校验处理。

max_length --
    字段的最大长度，仅用在 `StringProperty`, `CharProperty` 中。如果没
    有指定缺省为255。

sequence --
	 用在postgresql数据库中，表示一个sequence字段。
	 
index --
    如果设置为True则表示要使用当前字段生成索引。只适合单字段索引。如果要生成复
    合索引，要生成OnInit类方法，并调用Index函数来生成。缺省为False。

unique --
    表示字段是否可以重复。缺省为False。

nullable --
    指示在数据库中，本字段是否可以为 `NULL` 。缺省为True。

type_class, type_attrs --
    可以用来设置指定的SQLAlchemy的字段类型并设置要传入的字段属性。如果有长度值，
    则是在max_length中指定。

server_default --
    数据库缺省值，它会影响创建表时的Create语句，它会生成 `DEFAULT` 子句。它的取
    值按SQLAlchemy的写法应该使用text来封装，如 `text(0)` 。对于数值类型，正确的写法是使用 	 `text()` 来封装，不过Uliorm作了处理，可以直接使用数值。如： `server_default=0` 。

{% alert class=info %}
关于nullable和server_default在settings.ini中有配置项可以进行全局缺省值的设置：

```
[ORM]
NULLABLE = True
SERVER_DEFAULT = False
```

所以在缺省情况下，当没有给字段值的时候，如果default为None并且server_default也为
None，则存入数据库时会是NULL。如果你可以根据需要来修改这个全局配置，或针对每张表
通过参数来调整。
{% endalert %}

### 字段列表


#### CharProperty

与 `CHAR` 相对应。你应该传入一个 `max_length` 。如果传入一个Unicode字符串它
将转换为缺省编码(utf-8)。


#### StringProperty

与 `VARCHAR` 相对应。你应该传入一个 `max_length` 。如果传入一个Unicode字符串它
将转换为缺省编码(utf-8)。目前uliorm从数据库中取出StringProperty时会使用Unicode，
而不转换为utf-8或其它的编码。因此与UnicodeProperty是一致的。


#### TextProperty

与 `TEXT` 相对应。用于录入大段的文本。


#### UnicodeProperty

与 `VARCHAR` 相对应。但是你需要传入Unicode字符串。


#### BlobProperty

与 `BLOB` 相对应。用于保存二进制的文本。


#### DateProperty DateTimeProperty TimeProperty

这些字段类型用在日期和时间类型上。它们还有其它的参数:


auto_now --
    当设置为True时，在保存对象时，会自动使用当前系统时间来更新字段的取值。

auto_now_add --
    当设置为True时，仅创建对象时，会自动使用当前系统时间来更新字段的取值。

format --
    用来设置日期时间的格式串，uliorm会用它进行日期格式的转换。在缺省情况
    下，当传入一个字符串格式的日期字段时，uliorm会进行以下尝试:

    || 格式串 || 样例 ||
    || '%Y-%m-%d %H:%M:%S' || '2006-10-25 14:30:59' ||
    || '%Y-%m-%d %H:%M' || '2006-10-25 14:30' ||
    || '%Y-%m-%d' || '2006-10-25' ||
    || '%Y/%m/%d %H:%M:%S' || '2006/10/25 14:30:59' ||
    || '%Y/%m/%d %H:%M' || '2006/10/25 14:30' ||
    || '%Y/%m/%d ' || '2006/10/25 ' ||
    || '%m/%d/%Y %H:%M:%S' || '10/25/2006 14:30:59' ||
    || '%m/%d/%Y %H:%M' || '10/25/2006 14:30' ||
    || '%m/%d/%Y' || '10/25/2006' ||
    || '%m/%d/%y %H:%M:%S' || '10/25/06 14:30:59' ||
    || '%m/%d/%y %H:%M' || '10/25/06 14:30' ||
    || '%m/%d/%y' || '10/25/06' ||
    || '%H:%M:%S' || '14:30:59' ||
    || '%H:%M' || '14:30' ||




#### BooleanProperty

与 `Boolean` 相对应。不过对于不同的数据库底层可能还是不同。具体是由SQLAlchemy
来实现的。


#### DecimalProperty

与 `Numric` 相对应。它有两个参数：


precision --
    总长度，不计算小数点位数。

scale --
    小数长度。



#### FloatProperty

与 `Float` 对应。它有一个参数：


precision --
    总长度。



#### IntegerProperty

与 `Integer` 对应。


#### FileProperty

与 `VARCHAR` 对应。用于保存文件名，而不是文件对象。缺省的max_length为255。


#### PickleProperty

有时我们需要将一个Python对象保存到数据库中，因此我们可以采用 `BLOB` 字段来处理。
首先将对象序列化为字符串，可以使用Python自带的pickle，然后写入数据库。读出时再
反序列化为Python的对象。使用 `PickleProperty` 可以把这一过程自动化。


### Model的常见属性


table --
    uliorm的Model对应于SQLAlchemy的 `Table` 对象，而 `table` 将是底层的
    Table的实例。所以你可以使用这个属性来执行表级的操作。

c --
    Model的字段集。与 table.c 属性是一样的。

properties --
    所有定义在Model中的属性。

metadata --
    与SQLAlchemy中的metadata相对应的实例。

tablename --
    表名。



## 关系定义

uliorm支持以下几种关系的定义: OneToOne, Reference, SelfReference, ManyToMany.


### OneToOne

OneToOne是用来定义一对一的关系。


```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = OneToOne(Test)
...     name = Field(str)
```

可以使用OneToOne的关系来直接引用另一个对象。例如:


```
>>> a1 = Test(username='limodou')
>>> a1.save()
True
>>> b1 = Test1(name='user', test=a1)
>>> b1.save()
True
>>> a1
<Test {'username':'limodou','year':0,'id':1}>
>>> a1.test1
<Test1 {'test':<Test {'username':'limodou','year':0,'id':1}>,'name':'user','id':1}>
>>> b1.test
<Test {'username':'limodou','year':0,'id':1}>
```

在定义OneToOne时，可以传入一个collection_name的参数，这样，可以用这个名字来反向
引用对象。如果没有给出collection_name，则将使用表名作为引用名。


{% alert class=info %}
注意，OneToOne只是一个关系，它并不会自动根据主表记录自动创建关联表的记录。
{% endalert %}


### Reference

uliorm使用 `Reference` 来定义多对一的关系。


```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = Reference(Test, collection_name='tttt')
...     name = Field(str)
>>> a1 = Test(username='limodou1')
>>> a1.save()
True
>>> b1 = Test1(name='user', test=a1)
>>> b1.save()
True
>>> b2 = Test1(name='aaaa', test=a1)
>>> b2.save()
True
>>> a1
<Test {'username':'limodou1','year':0,'id':1}>
>>> list(a1.tttt.all())[0]   #here we use tttt but not test1_set
<Test1 {'test':<Test {'username':'limodou1','year':0,'id':1}>,'name':'user','id':1}>
>>> a1.tttt.count()
2
```

上面的例子演示了多个Test1记录可能对应一个Test记录。因此，我们可以在Test1中
定义 `Reference` 到Test上。对于Test1的某个实例，假定为b1，我们就可以通过
b1.test来获得对应的Test对象。这里会自动引发一个查询。如果你想从Test的某个对
象来反向获取Test1应该怎么办呢？假定Test的对象实例为a1，则缺省情况下我们可以通
过a1.test1_set.all()来获得a所对应的所有Test1的实例。为什么是all()呢？因为一个
Test对象有可能对应多个Test1对象（这就是多对一关系），所以得到的可能不仅一条
记录，应该是一个结果集。再看一下 `test1_set` ,它就是Test1的表名加 `_set`
后缀。但是，如果Test1中有多个字段都是到Test的Reference会出现什么情况。这时，
Uliweb会抛出异常。原因是，这样会在Test类中出现多个同名的test1_set属性，这是
有冲突的。所以当存在多个到同一个表的引用时，要进行改名。而Reference提供了一个
`collection_name` 的参数，可以用它来定义新的别名。比如上面的 `tttt` 。这样
在获取a1所对应的Test1的记录时，就可以使用 `a1.tttt` 来反向获取了。

Refernce有以下几个参数可以使用:


reference_class --
    第一个参数，指明要关联的Model。可以是Model类，也可以是字符串形式的表名。
    如果是第二种用法，则要与get_model配合使用。详见get_model的用法说明。

collection_name --
    前面已经介绍，是反向获取记录的名字

verbose_name --
    字段的提示信息

reference_fieldname --
    当引用一个Model时，缺省情况下是使用该Model的id字段。但是在特殊情况下，你可
    能希望指定其它的字段。这样可以将要引用的字段名传给 `reference_fieldname`
    参数。这样uliorm会根据被引用的字段来动态创建字段的类型。

required --
    是否是必输项。缺省为False。



{% alert class=info %}
uliorm的Reference关系并不会生成ForeignKey的外键。因为，一旦使用外键，则删除
导入数据时都有一个执行顺序，非常难处理。所以在设计上没有采用外键。

{% endalert %}


### SelfReference

如果你想引用自身,你可以使用 `SelfReference`, 例如:


```
>>> class User(Model):
...     username = Field(unicode)
...     parent = SelfReference(collection_name='children')
```


### ManyToMany


```
>>> class User(Model):
...     username = Field(CHAR, max_length=20)
...     year = Field(int)
>>> class Group(Model):
...     name = Field(str, max_length=20)
...     users = ManyToMany(User)
>>> a = User(username='limodou', year=5)
>>> a.save()
True
>>> b = User(username='user', year=10)
>>> b.save()
True
>>> c = User(username='abc', year=20)
>>> c.save()
True
>>> g1 = Group(name='python')
>>> g1.save()
True
>>> g2 = Group(name='perl')
>>> g2.save()
True
>>> g3 = Group(name='java')
>>> g3.save()
True
>>> g1.users.add(a)
>>> g1.users.add(b)
```

你可以使用 `ManyToMany` 来指明一个多对多的关系. uliorm会象Django一样自动创建
第三张表,上例的第三张表会是: `group_user_usres`, 它是由两个表名(user和group)
和关系名(users)组成. 第三张表的表结构会是:


```
CREATE TABLE group_user_users (
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (group_id, user_id)
)
```

### 手工创建 ManyToMany 表

在 Uliorm 中支持两种创建 ManyToMany 表的机制，一种是最常见的自动创建的方式。只要定义关系，就可以
自动创建。但是这种情况下，ManyToMany 表只会有两个字段。如果我们还希望在这个表上添加其它的字段，就
需要手工创建这张表，然后将其关联到 ManyToMany 中。

例如，先定义两个 User, Group Model:

```
class User(Model):
    username = Field(str)

class Group(model):
    name = Field(str)
```

然后定义第三张表，如： User_Group_Rel:

```
class User_Group_Rel(Model):
    user = Reference('user')
    group = Reference('group')
    role = Field(CHAR)
```

这里第三张表要定义两个 Reference 字段，一个指向 User ，一个指向 Group。然后我们可以把这个关系放
在 User 或 Group 上，修改 User 为：

```
class User(Model):
    username = Field(str)
    groups = ManyToMany('group', through='user_group_rel',
        through_reference_fieldname='user',through_reversed_fieldname='group')
```

通过 `through` 来定义将要引用的表名，通过 `through_reference_fieldname` 定义与 User.id 对应的
关系字段名，通过 `through_reversed_fieldname` 定义与 `Group.id` 对应的关系字段名，相当于要使用
以下的连接条件：

```
user.id==user_group_rel.user and group.id==user_group_rel.group
```

如果你的两个关系字段分别定义为对应的 `<表名>_id` 的形式，如：

```
class User_Group_Rel(Model):
    user_id = Reference('user')
    group_id = Reference('group')
    role = Field(CHAR)
```

那么将不需要设置 `through_reference_fieldname` 和 `through_reversed_fieldname` 。

定义好之后，就可以象一般 ManyToMany 字段一样来使用了。

但是我们定义单独的 ManyToMany 表是为了能够在关系上保存额外的数据，因此为了得到它们，需要在查询时指定
`with_relation(relation

## 操作

ORM的操作可以分为不同的级别: 实例级、Model级和关系级。


实例级 --
    这类操作只会影响实例自身，你可以进行: 创建、获取、删除、更新等操作。

Model级 --
    这类操作所处理的范围是整个Model或表级，它主要进行集合性质的操作。你可以进行：
    查询、计数、排序、删除、分组等操作。

关系级 --
    不同的关系可以执行不同的操作。如：OneToOne可以进行实例级操作。而Reference,
    SelfReference和ManyToMany则可以进行集合操作。在使用关系时，一种我们是使用
    inst.relationship的方式，这样会自动将关系与正在处理的实例进行条件的绑定，
    另一种是通过Model.relationship的方式，这样可以调用关系字段的某些特殊方法，
    比如用来生成条件。



### 实例级


#### 创建实例

假定有一个 User Model，类的定义为:


```
class User(Model):
    username = Field(CHAR, max_length=20)
    year = Field(int)
```

所以，如果你想要创建一个User的实例，只要:


```
user = User(username='limodou', year=36)
```

但这样还不会保存到数据库中，它只是创建了一个实例，你还需要调用 `save` 来保存:


```
user.save()
```


#### 获取实例


```
user = User.get(5)
user = User.get(User.c.id==5)
```

可以通过Model.get()来获取一个实例。在get()中是条件。如果是一个整数，则认为是要
获取id等于这个值的记录。否则你可以使用一个条件。这里条件的写法完全是遵守 SQLAlchemy
的要求。如果条件不止一个，可以使用 `and_, or_, not_` 或 `&, |, ~` 来拼接条件。SQLAlchemy
的相关文档可以查看： [http://www.sqlalchemy.org/docs/core/tutorial.html](http://www.sqlalchemy.org/docs/core/tutorial.html)


{% alert class=info %}
注意，在结果集上，你可以多个使用filter()连接多个 `and` 的条件，而get不支
持这样的用法。比如你可以 User.filter(User.c.id=5).filter(User.c.year>30)。
{% endalert %}


```
user = User.get_or_notfound(5)
```

使用get_or_notfound可以当无满足条件的对象时抛出一个NotFound的异常。


#### 删除实例


```
user = User.get(5)
user.delete()
```

delete在删除对象时，会自动删除相关联的ManyToMany的关系数据。如果不想删除，则可以
传入 `manytomany=False` 。


#### 更新实例


```
user = User.get(5)
user.username = 'user'
user.save()
```

更新实例可以直接向实例的某个字段赋予新值，也可以使用update方法来一次更新多个字
段。如:


```
user.update(username='user')
user.save()
```


{% alert class=info %}
注意，象创建和更新时，在调用相关的方法时，你传入的是key=value的写法，这里
key就是字段的名字。但是在写条件时，你要使用 Model.c.fieldname 这样的写法，
并且不是赋值，而是python的各种运算符。不要搞错了。
{% endalert %}

Uliorm在保存时会根据对象的id值是否为None来判断是否是insert还是update。如果你直接
设置了id值，但是又希望通过insert来插入数据，可以在调用save时传入 `insert=True` 。


{% alert class=warning %}
Model中更新数据库相关的方法，如: save, delete, get, get_or_notfound, count, remove
都可以传入connection参数，它可以是数据库连接名或真正的连接对象。
{% endalert %}


#### 其它的API


to_dict(fields=[], convert=True, manytomany=False) --
    将实例的值转为一个dict对象。如果没有给出fields参数，则所有字段都将转出。
    注意，这里对 `ManyToMany` 属性有特殊的处理。因为 `ManyToMany` 属性并
    不是真正的表中的字段，所以缺省情况下是不会包含这些值的，如果指定manytomany为
    True，则会也把相应的 `ManyToMany` 所对应的对象集的ID取出来，组织为一个list。
    如果convert=True，则在取出字段值的时候，还会调用field_str函数进行值的处理。
    在调用field_str时，strict保持为False不变。
    举例:

    ```
    a = User.get(1)
    a.to_dict() #this will dump all fields
    a.to_dict(['name', 'age'])    #this will only dump 'name' and 'age' fields
    ```


field_str(v, strict=False) --
    将某个字段的值转为字符串表示。如果strict为False，则只会处理日期类型、Decimal
    类型和将Unicode转为字符串。如果strict为True，则：None会转为''，其它的全部转为
    字符串。

get_display_value(field_name) --
    返回指定字段的显示值。特别是对于包含有choices的字段，可以根据相应的值返回对
    应的choices的值。

get_datastore_value(field_name) --
    返回指定字段的数据库的值。特别是对于 `Reference` 字段，如果直接使用inst.reference
    则得到的会是引用的对象，而不是数据库保存的值。而使用 `get_datastore_value()`
    可以得到数据库的值。

    {% alert class=info %}
    uliorm会将 `Reference` 字段保存到 `_field_name_` 的属性中，因此可以
    直接使用它来得到 `Reference` 的值。比如 `User.c.system` 可能是指向 `System`
    表的引用，直接使用 `user.system` 会得到对象的 `System` 的对象。而使用 `user._system_`
    则得到对应的数据库的值。
    {% endalert %}




### Model级

uliorm在Model级上的操作主要有两类，一类是直接通过Model.func来调用的，另一类是通
过Model.func或Model.relationship的方式返回结果集，再在结果集上进行操作。对于与
查询相关的函数，是可以连在一起使用的，比如:


```
User.filter(...).filter(...).count()
```

有些方法会返回结果集，因此你可以在返回值的基础上，再调用查询相关的方法。有些方法会
直接返回结果，不能再调用查询相关的方法。


#### 查询

在查询一个表的时候可能会有两种需求：全部记录和按条件筛选，因此对应着可以使用
`all()` 和 `filter()` 。`all()` 中是没有参数的，它会返回一个 `Result`
对象，这是前面介绍的结果集，你可以在结果集上继续使用其它的方法。 `filter()`
需要传入条件，条件的写法是符合SQLAlchemy要求的。它也返回一个结果集。多个 `filter()`
是可以连接使用的，相当于多个与条件。 `empty()` 返回一个空的结果集.

举例:


```
User.all()
User.empty()
User.filter(User.c.year > 18)
```


#### 删除记录

Model中提供了 `remove(condition)` 来删除满足条件的记录。同时你也可以利用结果
集来删除。例如:


```
User.remove(User.c.year<18)
#等价于
User.filter(User.c.year<18).remove()
```


{% alert class=info %}
注意，结果集的删除是使用 `remove` ，而实例的删除是使用 `delete` 。

{% endalert %}


#### 记录条数统计

Model中提供了 `count(condition)` 来计算满足条件的记录数。同时你也可以利用结果
集来统计，例如:


```
User.count(User.c.year<18)
#等价于
User.filter(User.c.year<18).count()
```

注意在使用count时，uliweb自动根据查询中是否存在：limit, group_by, join来决定是直接使用 `select count(*) from table where condition`
的形式，还是采用 `select count(*) as count_1 from (select * from table where)` 的形式。因为，一旦存在
limit, group_by, join，在计数时统计的是结果集，而第一种只是根据条件来处理的。所以对于 limit 这样的查询要按
结果集来统计。同时要注意，因为是对结果集来统计，所以它是先进行了一个子查询，从总体效果上来看，速度会慢一些。

#### 其它 API


bind(metadata=None, auto_create=False) --
    绑定当前的类到一个metadata对象上。如果 `auto_create` 为 `True`, 则将
    自动建表。

create() --
    建表，并且会自动检查表是否存在。

connect() --
    切換数据库连接，这样后续的执行将在新的数据库连接上进行。

get_engine_name() --
    获得当前表所使用的数据库连接的名字。在多个地方都可以设置数据库连接，uliweb
    将按以下顺序来判断：

    * 是否设置了 `__engine_name__`
    * 是否在 `settings.ini` 中设置了对应的连接名
    * `'default'`

    这样在缺省情况下，数据库连接名为 `default` .



### 关系级


#### 一对一(One to One)

一对一关系没什么特别的，例如:


```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = OneToOne(Test)
...     name = Field(str)
>>> a = Test(username='limodou', year=36).save()
>>> b = Test1(name='user', test=a).save()
>>> b.test
<Test {'username':'limodou', 'year':36}>
```

所以你可以使用 `b.test` 如同 `a` 对象。


{% alert class=info %}
注意，关系的建立是在相关的对象创建之后，而不是会根据关系自动创建对应的对象。

{% endalert %}


#### 多对一(Many to One)


```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = Reference(Test, collection_name='tttt')
...     name = Field(str)
>>> a = Test(username='limodou').save()
>>> b = Test1(name='user', test=a).save()
>>> c = Test1(name='aaaa', test=a).save()
```

根据上面的代码， Test:Test1 是一个 1:n 关系。并且 `b.test` 是对象 `a` 。但是
`a.tttt` 将是反向的结果集，它可能不止一个对象。所以 `a.tttt` 将返回一个 `Result`
对象。并且这个结果集对象将绑定到 Test1 Model，所以结果集的 `all()` 和 `filter()`
方法将只返回 Test1 对象。更多的细节可以查看 `Result` 的描述。


#### 多对多(Many to Many)


```
>>> class User(Model):
...     username = Field(CHAR, max_length=20)
...     year = Field(int)
>>> class Group(Model):
...     name = Field(str, max_length=20)
...     users = ManyToMany(User)
>>> a = User(username='limodou', year=5).save()
>>> b = User(username='user', year=10).save()
>>> c = User(username='abc', year=20).save()
>>> g1 = Group(name='python').save()
>>> g2 = Group(name='perl').save()
>>> g3 = Group(name='java').save()
>>> g1.users.add(a)
>>> g1.users.add(b)
```

当你调用 `a.group_set` (因为你没有在ManyToMany属性中定义collection_name)或
`g1.users` 时，将返回一个 `ManyResult` 对象。


### Result 对象

`Result` 对象的生成有多种方式，一种是执行某个关系查询时生成的，一种是直接在
Model上调用 `all()` 或 `filter()` 生成的。`Result` 对象有多个方法可以调
用，有些方法，如 `filter()` 会返回 `Result` 本身，因此还可以继续调用相应的
方法。有些方法直接返回结果，如： `one()`, `count()` 。因此你可以根据不同的
方法来考虑是不是使用方法的连用形式。

注意， `Result` 对象在调用相应的方法时，如果返回的是结果集本身，此时不会立即
进行数据库的交互，而是当你调用返回非结果集的函数，或要真正获得记录时才会与数据
库进行交互。比如执行 `User.filter(...).count()` 时，在执行到User.filter(...)
并没有与数据库进行交互，但在执行到 count() 时，则生成相应的SQL语句与数据库进行
交互。又如:


```
query = User.all()
for row in query:
```

在执行 `query = User.all()` 时，并不会引发数据库操作，而在执行 `for` 语句时
才会真正引发数据库的操作。

同时， `Result` 在获取数据时，除了 `one()` 和 `values_one()` 会直接返回
一条记录或 None。`all()` , `filter()`, `values()` 会返回一个 generator。
所以如果你想要一个list对象，需要使用 list(result) 来转成 list 结果。

方法说明:


all(): Result --
    返回Result本身. 注意在 Model中也有一个all()方法，它就是创建一个 `Result`
    对象，然后将其返回。如果不带任何条件创建一个结果集，则在处理记录时相当
    于all()的调用。

empty(): Result --
    返回空的结果集.

any(): Boolean --
    根据条件判断是否存在相应的记录.如果存在返回 `True`,不存在返回 `False`.

filter(condition): Result --
    按条件查询。可以多个filter连用。返回结果集本身。
    示例:

    ```
    User.filter(User.c.age > 30).filter(User.c.username.like('Lee' + '%%'))
    ```


connect(engine_name): Result --
    切換到指定的连接名上，engine_name可以是连接名，Engine对象或Connection对象。

count(): int --
    返回满足条件的记录条数。需要与前面的all(), filter()连用。

    {% alert class=info %}
    在Model中也有一个count()方法，但是它是可以带条件的，比如: `User.count(User.c.age > 30)` 。
    它可以等同于 `User.filter(User.c.age > 30).count()`
    {% endalert %}

    示例:

    ```
    User.all().count()
    User.filter(User.c.username == 'a').count()
    ```


remove(): None --
    删除所有满足条件的记录。它其实是调用 Model.remove(condition)。可以和 `all()`
    和 `filter()` 连用。

update(**kwargs): --
    执行一条update语句。例如:

    ```
    User.filter(User.c.id==1).update(username='test')
    ```

    它等同于:

    ```
    do_(User.table.update().where(User.c.id==1).values(username='test'))
    ```


order_by(*field): Result --
    向查询中添加 `ORDER BY` 字句。例如:

    ```
    result.order_by(User.c.year.desc()).order_by(User.c.username.asc())
    #or
    result.order_by(User.c.year.desc(), User.c.username.asc())
    ```

    缺省情况下是按升序排列，所以asc()可以不加。

limit(n): Result --
    向查询中添加 `LIMIT` 子句。`n` 是一个整数。

offset(n): Result --
    向查询中添加 `OFFSET` 子句。 `n` 是一个整数。

distinct(*field): Result --
    向查询中添加 `DISTINCT` 函数，field是字段列表。

values(*fields): 结果 generator --
    它将根据前面设置的条件立即返回一个结果的generator。每行只会列出指定的字段值。
    fields为字段列表，可以直接是字段的名字，也可以是Model.c.fieldname的形式。
    例如:

    ```
    >>> print a1.tttt.all().values(Test1.c.name, Test1.c.year)
    [(u'user', 5), (u'aaaa', 10)]
    >>> print a1.tttt.all().values('name', 'year')
    a1.tttt.all().values(Test1.c.name, Test1.c.year)
    ```


one(): value --
    只返回结果集中的第一条记录。如果没有记录，则返回 `None` 。

values_one(*fields): value --
    相当于执行了 `values()`, 但是只会返回第一条记录。

get(condition): value --
    相当于 `Result.filter(condition).one()` 。

without(flag='default_query') --
    去掉default_query的条件处理。



### ManyResult

`ManyResult` 非常象 `Result`, 只不过它是通过 `ManyToMany` 关系创建的，它
拥有与 `Result` 大部分相同的方法，但是有一些差别:


add(*objects): boolean --
    这个方法可以建立多个对象与当前对象的多对多关系。其实就是向第三张关系表中插入
    相应的记录。它会返回一个boolean值。如果为 Ture 表示有变化。否则无变化。如果
    Model A的实例a已经和Model B的某些实例有多对多的关系，那么当你添加新的关系时
    对于已经存在的关系将不会再添加，只添加不存在的关系。

update(*objects): boolean --
    这个方法与add()有所不同。add会在原来的基础之上添加新的关系。而update会完全
    按照传入的对象来重新修改关系，对于仍然存在的关系将保留，对于不存在的关系将
    删除。它也会返回是否存在修改的状态。

ids(): list --
    它将返回ManyToMany关系中所有记录的 ID 列表。注意，这里的ID是与定义ManyToMany
    属性时所使用的引用字段一致的。缺省情况下是id字段，如果使用了其它的引用字段
    则有可能是别的字段。

has(*objects): boolean --
    判断传入的对象是否存在于关系中。这里对象可以是对象的id值，也可以是对象。如果
    存在则返回 True，如果不存在则返回 False。

## Session管理

当我们需要进行数据库的操作时，我们要建立一个连接对象。在一个engine对象上，可以
建不同的连接对象，一个连接对象可以有不同的事务。因此事务都是放在某个连接对象上的。
为了方便使用这些连接对象，Uliweb对其进行了包装，构造了 Session 类。这个 Session
和SQLalchemy提供的 session 机制是不同的。在Uliweb主要是管理连接的，它还提供了事务
的管理功能。

Session对象会有两种创建方式，一种是自动创建。当我们在某个数据库连接上进行操作时，
如： `do_(sql, engine_name)` ，这里只指明了要操作的连接名。这种情况下，Uliorm会
自动使用对应连接名对象上的session对象（如果在执行SQL时还没有创建，则会自动创建）。
同时，考虑到多线程工作的情况，这个session对象在不同的线程环境是不同的。

所以这种情况下，当只使用连接名来进行SQL操作时，同一个线程使用的 Session 对象是
相同的，因此它们的事务也将是相同的。

第二种情况就是手工创建 Session 对象，只要执行 `session = Session()` 或 `session = Session(engine_name)`
会通过相应的数据库连接对象来创建相应的连接。这种方式是显示地创建 session 对象，
不会复用已经存在的 Session 对象。




## 事务处理

uliorm提供两种控制事务的方式，一种是通过Middleware，一种是手工处理。如果要使用
Middleware方式，你需要在settings.ini中添加:


```
MIDDLEWARE_CLASSES = [
    'uliweb.orm.middle_transaction.TransactionMiddle'
]
```

使用Mideleware，它将在每个view处理时生效。当view成功处理，没有异常时，事务会被
自动提交。当view处理失败，抛出异常时，事务会被回滚。


{% alert class=info %}
一般情况下，只有事务处理Middleware捕获到了异常时，才会自动对事务进行回滚。
因此，如果你自行捕获了异常并进行了处理，一般要自行去处理异常。
{% endalert %}

手工处理事务，uliorm提供了基于线程模式的连接处理。uliorm提供了：Begin(), Commit(),
和Rollback()函数。当执行Begin()时，它会先检查是否当前线程已经存在一个连接，
如果存在，则直接使用，如果不存在则，如果传入了create=True，则自动创建一个连接，
并绑到当前的线程中。如果create=False，则使用engine的连接。同时Commit()和Rollback()
都会使用类似的方式，以保证与Begin()中获得的连接一致。


### Web事务模式

一般你要使用事务中间件，它的处理代码很简单，为:


```
class TransactionMiddle(Middleware):
    ORDER = 80

    def __init__(self, application, settings):
        self.db = None
        self.settings = settings

    def process_request(self, request):
        Begin()

    def process_response(self, request, response):
        try:
            return response
        finally:
            CommitAll(close=True)
            if self.settings.ORM.CONNECTION_TYPE == 'short':
                db = get_connection()
                db.dispose()

    def process_exception(self, request, exception):
        RollbackAll(close=True)
        if self.settings.ORM.CONNECTION_TYPE == 'short':
            db = get_connection()
            db.dispose()
```

当请求进来时，执行 Begin() 以创建线程级别的连接对象。这样，如果在你的
View中要手工处理事务，执行Begin()会自动使用当前线程的连接对象。

应答成功时，执行 `CommitAll(close=True)` ，完成提交并关闭连接。因为有可能存在
多个连接，所以使用CommitAll. 而在View中手动控制一般只要调用 `Commit()` 就可以了，
关闭连接交由中间件完成。

如果中间处理抛出异常，则执行 `RollbackAll(close=True)` ，回滚当前事务，并关闭
所有连接。而在View中手动控制，也只要简单调用 `Rollback()` 就可以了，关闭连接处理由
中间件完成。

在View中的处理，有几点要注意，Begin(), Commit(), Rollback() 都不带参数调用。
在Uliorm中，SQL的执行分两种，一种是直接使用ORM的API处理，还有一种是使用SQLAlchemy
的API进行处理(即非ORM的SQL)。为了保证正确使用线程的连接对象，ORM的API已经都使用
`do_()` 进行了处理。 `do_()` 可以保证执行的SQL语句在当前的合理的连接上执行。几种
常见的SQL的书写样板:


```
#插入
do_(User.table.insert().values(username='limodou'))
#更新
do_(User.table.update().where(User.c.username=='limodou').values(flag=True))
#删除
do_(User.table.delete().where(User.c.username=='limodou'))
#查询
do_(select(User.c, User.c.username=='limodou'))
```


### 命令行事务模式

所谓命令行事务模式一般就是在命令行下运行，比如批处理。它们一般不存在多线程的环境，
所以一个程序就是一个进程，使用一个连接就可以了。这时我们可以还使用engine的连接
对象。使用时，只要简单的不带参数调用Begin(), Commit()和Rollback()就可以了。因为
Begin()在没有参数调用的情况下，会自动先判断有没有线程级的连接对象，这时一定是没有，
如果没有，则使用engine下的连接对象。

这样，SQL语句既可以使用do_()来运行，也可以使用原来的SQLAlchemy的执行方式，如:


```
#插入
User.table.insert().values(username='limodou').execute()
#更新
User.table.update().where(User.c.username=='limodou').values(flag=True).execute()
#删除
User.table.delete().where(User.c.username=='limodou').execute()
#查询
select(User.c, User.c.username=='limodou').execute()
```


## NotFound异常

当你使用get_or_notfound()或在使用instance.refernce_field时，如果对象没找到则会
抛出NotFound异常。


## Model配置化

uliorm在考虑Model的可替换性时，提供了一种配置机制。这种机制主要是由orm app来初
始化的，它对Model的编写有一定的要求。使用配置机制的好处主要有两点：


1. 可以方便使用，不用关心要使用的Model是在哪里定义的。orm提供了 `get_model()`
    方法，可以传入字符串的表名或真正的Model对象。因此在一般情况下，使用字符串
    形式是最方便的。比如我们想获得一个User的Model，可以使用:

    ```
    User = get_model('user')
    ```

    但是使用这种字符串的形式，对于Model的配置有要求。需要在settings.ini中配置:

    ```
    [MODELS]
    user = 'uliweb.contrib.auth.models.User'
    ```

    其中key为引用的别名。它可以是表名（一般为Model类名小写），也可以不是表名。
    value为表所对应的Model类的路径。uliorm将在需要时自动进行导入。

    {% alert class=info %}
    为什么需要表名呢？因为orm提供的命令行工具中，syncdb会自动创建数据库中
    不存在的表，它就是使用的真正的表名。
    {% endalert %}


1. 可以有条件的方便进行替换。
    在某些时候，你可能发现某个app的表结构要扩展几个字段，但是因为已经有许多Model
    和这个表实现了关联，而且这个app提供了其它与些Model相关的一些方法。因此，如果
    简单地替换这个app，有可能会要同时修改其它的app的代码，比如导入处理等。如是你
    在定义关系时使用的是get_model(name)的形式，并且name是字符串，这样你实际上已经
    实现了Model的配置化。因此你就可以定义新的Model类，并且配置到settings.ini中来
    替换原来的Model。如果不是把配置信息写到同一个settings.ini中，那么，你可以把
    新的App定义到原来的App之后(这里指INSTALLED_APPS)，这样后面定义的内容会覆盖前
    面定义的内容。这种做比较适合扩展字段的情况，或表结构的修改不影响其它的功能调
    用的情况。

在定义关系时，象OneToOne, Reference和ManyToMany时既可以接受字符串的Model名，也
可以直接传入Model的类，都可以。


## 如何在其它项目中使用 uliorm

uliorm是可以在非Uliweb项目和非web程序中使用的，因此根据是否有Uliweb项目，决定了
可以使用不同的方式。


### 非Uliweb项目

Uliweb项目中，所有的Model都要配置到settings.ini中去，所以在非Uliweb项目中，你无
法这样做，因此处理上会有所不同。因为没有了Model的配置，所以你需要在使用Model前
先导入它们。然后你要考虑是自动建表还是手工建表。我建议是把自动建表单独处理，只
在需要时执行。简单的一个代码示例:


```
from uliweb.orm import *

class User(Model):
    name = Field(unicode)
class Group(Model):
    name = Field(str)
    users = ManyToMany(User, collection_name = 'groups')

if __name__ == '__main__':
    db = get_connection('sqlite://')
    db.metadata.drop_all()
    db.metadata.create_all()
    u1 = User(name='limodou')
    u1.save()
    g1 = Group(name='python')
    g1.save()
    g1.users.add(u1)

    print g1.users.one().groups.one().users.one().name
    print u1.groups.one().users.one().groups.one().name
```

这里 `db.metadata.create_all()` 用于创建所有的表。


### Uliweb项目

如果我们要在非web程序中使用uliorm时，我们还是希望使用Uliweb的管理机制，使用Uliweb
项目的配置信息，这时我们可以:


```
from uliweb.manage import make_simple_application

app = make_simple_application(project_dir='.')
Begin()
try:
    User = get_model('user')
    print list(User.all())
    Commit()
except:
    Rollback()
```


### 在守护中使用Uliorm的注意事务

其实在守护中使用uliorm就是要注意使用事务。在我自已的开发中发现一个问题:

例如有一个循环，它的工作就是扫描数据库满足某个条件的数据集，如果有，则取出进行
处理，然后修改处理标志。处理完毕或不存在这样的数据，则sleep一定的时间。然后反复
执行。我在循环外创建一个数据库连接，这样可以复用这个连接。但是发现：一旦我在循
环中查到了数据，并执行了更新，则在以后的循环中，如果数据又发生了变化，但是我将
无法得到后来变化的数据。于是我到SQLAlchemy上问了一下，结果发现是由于数据库的连
接如果一直使用的话，当执行了更新，插入之类的操作后，事务隔离级会上升，造成数据
库认为当前连接所得到的数据已经是最新的，再查询时将不会返回新结果。所以，建议是
每次循环创建新的连接。因此，我在ORM中提供了Reset命令，它可以清除当前连接，从而
实现新连接的创建。因此如果你的处理是一个循环，可以在每次循环时执行 `Reset()` 。



## 信号处理

uliorm提供类似django信号的处理机制，它会在一些重要的执行点调用发出信号，以便让
其它的信号处理函数进行后续的工作。注意，uliorm的信号并不是真正的异步，它只是定
义上的异步，调用还是同步的。


### 预定义的几种信号

uliorm已经提供了几种预定义好的信号，下面列举出来。在每个信号名的冒号后面所定义
的是使用dispatch调用时使用的方法，分为call和get。其中call不需要返回值，并且会
将所有订阅此信号的方法依次调用。而get需要一个返回值，一旦某个方法返回非None的值，
则结束调用并将值返回。


pre_save:call --
    保存一个对象 **前** 发出的信号
    参数： instance, created, data, old_data

    instance --
            为保存的对象

    created --
            True为创建，False为修改

    data --
            新的数据

    old_data --
            旧的数据



post_save:call --
    保存一个对象 **后** 发出的信号。参数同 `pre_save`

pre_delete:call --
    删除一个对象 **前** 发出的信号
    参数： instance

    instance --
            为待删除的对象



post_delete:call --
    删除一个对象 **后** 发出的信号
    参数： instance

    instance --
            为待删除的对象



get_object:get --
    通过Model.get()获得一个对象 **前** 发出的信号。get_object和set_object
    相结合可以实现简单的对get()方式的单对象的缓存处理。在uliweb中已经提供了一个
    名为objcache的app，它可以在获取简单条件的对象时自动进行缓存的处理。
    参数: condition

    condition --
            调用get()方法所使用的条件，它是SQLAlchemy的一个表达式对象



set_object:call --
    通过Model.get()获得一个对象 **后** 发出的信号
    参数: condition, instance

    condition --
            调用get()方法所使用的条件，它是SQLAlchemy的一个表达式对象

    instance --
            所获得的对象实例





### 定义接收函数

当使用uliorm时，它会根据执行情况自动发出相应的信号，此时如果有订阅此信号的方法存
在则将被自动调用，如果不存在，则继续后面的处理。在uliweb中，一般将订阅方法写在
settings.ini中，以减少启动时的导入处理。举例如下:


```
[BINDS]
audit.post_save = 'post_save'
audit.pre_delete = 'pre_delete'
```

在settings.ini中定义BINDS节，然后key是方法路径，值是对应的信号。方法路径的形式为:


```
module.function_name
```

为什么要这样定义？因为一个信号可以被多个方法来订阅，因此信号是可以重复的。

Uliweb在启动时会自动读取settings.ini中的信号，然后将其与相应的信号进行绑定。相
关的处理方法此时并不真正导入，而是当发出信号时，再动态导入。

接收函数的定义形式为:


```
def receiver(sender, topic, **kwargs)
```

第一和第二个参数都是固定的，sender是发出信号的对象。在uliorm中都是Model类。
topic是信号的名称。后面的kwargs对应每个信号可以接受的参数。不同的信号所接受的
参数可能是不同的。


## 测试代码

在 uliweb/test/test_orm.py 中有一些测试代码，你可以查看一些例子来了解如何使用
uliorm。


