# 数据库和ORM

Uliweb内置了一个ORM，不过它是通过orm这个app来安装的，所以缺省情况下，ORM不是自
动生效的。因此，你可以自已使用其它的ORM或数据相关的模块。当然，Uliweb的orm(以下
简称uliorm)也提供了不错的功能，欢迎使用和提改进意见。uliorm是基于sqlalchemy开
发的，并且目前没有使用session机制，而且你可以直接使用一些sqlalchemy底层的功能，如:
select, update, join等。


## 使用要求

需要安装sqlalchemy 0.6+以上的版本。如果你使用sqlite，则python 2.5+就自带了。如果
使用其它的数据库，则还需要安装相应的包。sqlalchemy本身是不带的。

建议使用0.7+以上的版本。


## 配置

首先将 `uliweb.contrib.orm` 添加到 `apps/settings.ini` 的 `INSTALLED_APPS` 中去。
`uliweb.contrib.orm` 的settings.ini中已经提供了几个缺省的配置项，用来控制ORM
的行为:


```
[ORM]
DEBUG_LOG = False
AUTO_CREATE = True
AUTO_DOTRANSACTION = True
CONNECTION = 'sqlite:///database.db'
CONNECTION_TYPE = 'long'
CONNECTION_ARGS = {}
STRATEGY = 'threadlocal'
CONNECTIONS = {}

[MIDDLEWARES]
transaction = 'uliweb.orm.middle_transaction.TransactionMiddle'
```

你可以在apps/settings.ini中覆盖它们。

`DEBUG_LOG` 用来切换是否显示SQLAlchemy的日志。如果设置为True，则SQL语句会输出
到日志中。缺省为False。

`AUTO_CREATE` 用于切换是否可以自动建表。在开发的时候，最简单的情况就是当你定
义完一个Model，那么就可以直接使用它了。Uliorm会自动在数据库中创建表。如果设置为
False，则需要手工建表。要么，你可以直接手工写Create语句，然后到数据库中去创建表，
但是我们一般不会使用这种方法。要么，你可以通过uliweb sql <appname>来生成建表的
SQL语句，然后再到数据库中执行这些语句。但是这种做法，不会将Model中定义的索引也
自动创建（因为SQLAlchemy目前显示建表的SQL功能不能简单地显示索引创建的SQL代码）。
所以还不是完全的。而采用uliweb syncdb就可以自动将没有创建过的表进行创建。注意：
它只会创建没有创建过的表。对于已经创建，但是修改过的表应该如何重建呢？答案是使用
uliweb reset命令。


{% alert class=info %}
自动建表对于sqlite有一个问题。如果在你执行一个事务时，非查询和更新类的语句
会引发事务的自动提交。而自动建表就是会先查找表是否存在，因此会破坏事务的处理。
所以建议对于sqlite禁止自动建表，而是手工建表。其它的暂时还没有发现。

{% endalert %}

`AUTO_DOTRANSACTION` 用于指示是否在执行 `do_` 时自动根据环境来创建新的共享
的线程连接并启动事务，详情参见下面关于多数据库连接的说明。


`CONNECTION` 用于设置数据库连接串。它是遵循SQLAlchemy的要求的。（详情可以参考 --
    [http://www.sqlalchemy.org/docs/05/dbengine.html#create-engine-url-arguments](http://www.sqlalchemy.org/docs/05/dbengine.html#create-engine-url-arguments)）


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

`CONNECTION_TYPE` 用于指明连接模式： `'long'` 为长连接，会在启动时建立。
`'short'` 为短连接，只会在每个请求时建立。使用短连接需要配置 `middle_transaction` 。
使用长连接并不需要配置这个middleware。缺省值为 `'long'` 即长连接。

`CONNECTION_ARGS` 用于除连接串之外的一些参数。SQLAlchemy中，创建引擎时要使用:


```
create_engine(connection, **kwargs)
```

而CONNECTION_ARGS将传入到kwargs中。在某些connection中其实还可以带一些类QUREY_STRING
的东西，如在对mysql的连接中，可以在连接串后面添加 `'?charset=utf8`` 。而这个参
数是会直接传给更底层的mysql的驱动。而CONNECTION_ARGS是传给create_engine的，所以
还是有所不同。

`STRATEGY` 连接策略。此为sqlalchemy的连接参数，可以选择的值为 `plain` 和 `threadlocal`.
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

`CONNECTIONS` 数据库多连接设置。uliweb是支持多个数据库连接，自然也支持多个数据库。
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


MIDDLEWARES --
    安装 uliweb.contrib.orm app会自动添加 TransactionMiddle ，这样将自动启动事务。 **0.1.1修改**



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


### 表别名

在后面我们会了解 Model 在使用时都需要配置，每个Model会有一个名字，因此我们可以
使用 `get_model(name)` 来获得一个Model对象。通常情况下Model的配置名和表名是
相同的（即Model的类名小写），但有时可能也需要有所不同。所以在0.1版本以后就可以
和表名不相同了。设置别名有两种方式， 一种是通过框架来使用Model，所以只要在settings
中配置就可以了。另一种是不通过框架来使用Model，如直接import，那么可以在Model类上
设置 `__alias__` 。


### 表参数

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

### 表的映射

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

### 连接引擎设置

uliweb支持多种数据库连接的设置，其中可以在Model中设置 `__engine_name__` 为指定
的某个连接名，如:


```
class Todo(Model):
    __engine_name__ = 'test'
```


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


### 属性定义

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


### Property 构造函数

Property 其它所有字段类的基类。所以它的一些属性和方法将会被派生类使用到，它的定
义为:


```
Property(verbose_name=None, name=None, default=None, required=False,
    validators=None, choices=None, max_length=None, type_class=None,
    type_attrs=None)
```


verbose_name --
    用于显示字段的描述信息。一般是用在显示界面上。

name --
    字段名，用在所创建的表中。它一般是和Property的实例名相同。例如:

    ```
    class User(Model):
        username = StringProperty(name='user_name')
    ```

    username就是Property的实例名，而name缺省不给出的话就是 `username`, 上面的
    示例是指定了一个不同的值。因此你通过orm引用属性时要使用 `username`，但是
    直接对数据库查询或操作时，即要使用 `user_name`, 因此为了避免造成理解和使用
    上的混乱，建议不要指定 `name` 参数。

default --
    字段的缺省值。注意，default可以是一个函数。在创建一个Model的实例时，对于未
    给出值的属性，uliorm会自动使用default给字段赋值。因此，如果default没有赋值，
    则这个值一般为None。但是对于象IntegerProperty之类的特殊字段来说，缺省值不是None，如
    0。同时，在调用时要注意default函数执行是否可以成功。因为有的时候需要
    在某个环境下，而你在执行时可能不具备所要求的环境，比如default函数要处理request.user，
    但是你有可能在批处理中去创建实例，这样request.user是不会存在的，因此会报错。
    简单的处理就是把Model.field.default置为None。

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

choices --
    当属性值的取值范围是有限时可以使用。它是一个list，每个元素是一个二元tuple，
    格式为(value, display)，value为取值，display为显示信息。目前，uliorm并不用
    它来校验传入数据的正确性，用户可以根据需要自定义校验函数，传入validators中
    进行校验处理。

max_length --
    字段的最大长度，仅用在 `StringProperty`, `CharProperty` 中。如果没
    有指定缺省为30。

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



{% alert class=info %}
Uliweb中Model对应的表名一方面可以通过 `__tablename__` 来指定。另一方面，它
可以将Model的类名小写作为表名。

{% endalert %}


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
是可以连接使用的，相当于多个与条件。

举例:


```
User.all()
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


    {% alert class=info %}
    在使用多数据库连接时，可以在上面的MODELS中的每张表的路径后面添加数据库
    连接名，如:

    ```
    [MODELS]
    user = 'uliweb.contrib.auth.models.User', 'test'
    user = 'uliweb.contrib.auth.models.User', ['default', 'test']
    ```

    第一种是说只在 `test` 中使用User表。而第二种则表示可以在 `default`
    或 `test` 中使用User表，决定的顺序一是根据 Model 的 `__engine_name`
    的设置或执行时使用 `connect(engine_name)` 进行设定。否则将使用第一个。
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


## 模块级 API

uliweb.orm 提供了一些模块级别的方法，用于控制整个uliorm的工作模式。不过，如果
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

get_connection(connection='', default=True, debug=None, engine_name=None, connection_type='long', **args) --
    建立一个数据库连接，并返回连接对象。
    connection需要按SQLAlchemy的要求来编写。
    get_connection既可以支持原来的单数据库连接模式，也可以支持多数据库连接模式，
    还可以支持缺省连接模式，既上次创建过，然后复用原来的连接。那么它按以下策略
    来处理:

    ```
    if connection 不为空:
        则缺建新的连接
        if default is True:
            则将连接设置到线程中进行共享
        else:
            不共享
    else:
        按engine_name来返回连接。如果engine_name为None，则使用 default
    ```


get_model(model, engine_name=None) --
    返回指定连接的 `model` 对应的Class。如果是字符串值，则需要根据Model配置的要求在settings.ini
    中定义Model的信息才有效果。也可以传入Model的类。
    如果engine_name不为None，则根据给定的engine_name来查找Model。如果不存在，则
    抛出异常。
    如果engine_name为空时，将会智能搜索。如果某个Model只设置了一个数据库连接，
    则自动使用这个连接，如果存在多个则会抛出异常。

local_connection(engine_name=None, auto_transaction=False): conn --
    返回缓存的数据库连接。如果不存在，则创建。 `auto_transaction` 是用来控制
    是否自动创建事务。

Connect(engine_name=None): None --
    清除缓存的线程连接，保证下次再访问时可以重建连接。

Begin(ec=None): transaction object --
    开始一个事务。如果存在线程连接对象同时如果不存在当前线程内的连接对象，则自动从连接池中取一个连接
    并绑定到当前线程环境中。ec为数据库引擎对象名，如果没提供，则缺省为 'default'.
    ec也可以为连接对象。

Commit(close=False, ec=None, trans=None) --
    提交一个事务。使用当前线程的连接对象。

CommitAll(close=False) --
    提交所有线程事务。

Rollback(close=False, ec=None, trans=None) --
    回滚一个事务。使用当前线程的连接对象。

RollbackAll(close=False) --
    回滚所有线程事务。

do_(sql, ec=None) --
    执行一条SQL语句。使用当前的线程连接。只有当使用非ORM的API时才需要使用它
    来处理，比如直接使用SQLAlchemy提供的：select, update, delete, insert时，可
    以这样:

    ```
    from uliweb.orm import do_
    
    result = do_(select(User.c, User.c.username=='limodou'))
    ```




## 多数据库连接

从 0.1 版本开始，uliorm 就开始支持多数据库连接了，多数据库连接在这里有两种涵义:


* 同类数据库的不同连接
* 不同类的数据库的不同连接

所以这里没有简单地使用多数据库的说法，而是采用多数据库连接的说法。

在uliorm中多数据库连接的支持分为以下几方面的内容:


* 数据库连接的定义，涉及到settings.ini的配置
* Model如何指定数据库连接，涉及到settings.ini的配置和Model的定义以及执行
* 语句执行以及事务的多数据库连接的支持，包括中间件的支持，线程连接的处理等
* 命令行多数据库的支持


### 数据库连接的定义

首先为了区分不同的数据库连接，并且方便地引用它们，每个连接都需要定义一个名字。
在没有特殊定义的情况下，总是会有一个 `default` 的连接存在。它就是使用原来的
数据库连接的定义。当需要定义其它的数据库连接时，可以在 ORM 下定义 CONNECTIONS
如:


```
CONNECTIONS = {
    'test': {
        'CONNECTION':'mysql://root:limodou@localhost/test2?charset=utf8',
        'CONNECTION_TYPE':'short',
    }
}
```

上面定义了一个名为 `test` 的连接。

定义好连接，在启动 Uliweb 项目时，系统会自动根据配置创建相应的引擎对象。并且在
`orm` 中会自动创建一个管理对象，名为: `engine_manager` ，它可以象一个dict一样
使用，是用来管理连接的。我们可以通过它得到每个连接的信息，包括配置信息和创建的
相关对象的信息，主要包含:


```
options         连接参数：
                    connection_string:  连接串
                    connection_args:    连接参数
                    debug_log:          是否调试
                    connection_type:    连接类型， long or short
engine          引擎实例。对应实际的数据库引擎对象，比如通过
                sqlalchemy的 ``create_engine()`` 创建的对象
metadata        对应的MetaData对象，可以通过它获得对应的表信息
models          与之相关的所有的Model对象信息
```

比如想要获得 default 的连接对象:


```
engine = engine_manager['default'].engine
```

或者直接使用 `get_connection`


```
engine = get_connection(engine_name='default')
```

如果只是访问缺省的连接，可以将 default 使用None来代替，如:


```
engine = engine_manager[None].engine
engine = get_connection()
```

因此我们可以了解，一旦项目启动，定义的数据库的引擎对象将直接被创建。但是此时真
正用来与数据库通讯的连接对象还没有创建，它们将随着请求被自动创建和管理。


### Model的连接设置

在设计uliorm的多数据库连接时我一直在想：多数据库连接在什么情况下会被使用呢？
它们又是如何被使用呢？如果设计时考虑过多，会使得开发变得困难，因此我假设了以下
使用的场景:


* 数据库表本身直接与不同的数据库连接相对应，它们不会混用。这可能是最简单的一种
    情况了。在这种情况下，我们只要能定义出表与将要使用的引擎之间的关系就可以了。
* 数据库表本身可能在多个不同的数据库连接中使用。这样，我们不仅要定义一张表与
    不同的数据库连接关系，还要在运行时指定当前使用哪个连接。

根据以上的假设，uliorm提供了静态配置和动态切換两种方式。

静态配置又分为：settings.ini配置和Model属性配置。

在Uliweb中，每张表如果要使用首先要在settings.ini中进行配置，原来的写法是:


```
[MODELS]
user = 'uliweb.contrib.auth.models.User'
```

现在的写法是:


```
[MODELS]
user = 'uliweb.contrib.auth.models.User', 'test'
user = 'uliweb.contrib.auth.models.User', ['default', 'test']
```

比原来多了一项，就是数据库连接名。如果可以同时在多个连接中使用，后面的连接将是
一个list值。原来的写法依然是有效的，如果不提供，则会认为使用Model属性的定义，如
果Model属性定义也没有，则认为使用 default 连接。

在Model属性中也可以配置，就是添加 `__engine_name__` 属性，比如:


```
class User(Model):
    __engine_name__ = 'test'
```

如果存在多种定义，那么uliweb将按以下顺序来处理:


1. 是否设置了 `__engine_name__`
1. 是否在 `settings.ini` 中设置了对应的连接名
1. `'default'`

所以缺省情况下是使用 `default` 。

当一个Model设置了多个连接名，要么在运行时动态指定，要么uliweb会抛出异常。
所以为了动态指定，uliorm的许多函数和方法都添加了 `engine_name` 参数，比如:


```
Model.connect(engine_name)
Result.connect(engine_name)
```

其中Model类上可以直接调用 `connect()` 来切換连接，它会直接影响后面的结果处理，包括
结果集的处理。这里 `engine_name` 还可以是 `Engine` 对象或 `Connection` 对象。
同时，当返回一个结果集时，在没有获得数据之前，也可以使用结果集的 `connect()` 来切換连接。
这种做法只会影响执行结果。


{% alert class=info %}
原来想实现隐式的连接切換功能，即不要显示地使用象 `connect()` 这样的方法。但是
发现很难做到。

{% endalert %}


### 多数据库下的语句执行与事务处理

在数据库处理中，所有的语句都需要在连接上被执行，事务也是在连接上被处理。不同的
连接意味着不同的处理。考虑到web处理和批处理的方式不同，我们可以考虑以下的场景:


* web处理一般是按请求来执行的，因此一个请求过来，创建一个连接，处理完毕后释放。
    连接可以是长连接或短连接。长连接意味着将使用连接池，因此所谓的释放就是放回池
    子里供下一次使用。而短连接就没有池子，释放就是真正的关闭，下次请求将再次创建。
    而不管长连接还是短连接，处理模式都基本相同。
    为了简化处理，我们可以每次当请求进入时自动创建一个连接，然后启动事务，并且把
    这个连接放到线程环境中，这样所有使用 `do_` 就可以直接利用这个共享的连接和事务
    了。这样的处理只是为了简化。因为有可能一个请求并没有事务处理，甚至不涉及到数据
    操作，这样做有些过头了，不过目前为了简化，uliweb就是这样设计的。
    当支持多数据库连接时，情况有了一些变化。原来可以只自动建一个连接，但是现
    在有可能是有多个连接。那么我们要为所有的连接创建实例，并启动事务吗？因此，
    现在的策略就是只为缺省的连接创建连接实例，并启动事务。对于其它的连接，
    Uliorm 増加了一个名为 `AUTO_DOTRANSACTION` 的配置项，缺省为 `True`.
    它的作用就是当你执行 `do_` 时自动创建连接并启动事务。另一种做法就是使用
    `Begin(ec=engine_name)` 来手工创建连接和事务。目前只要是基本的 SQL 语句
    ，包括： select, update, insert, delete 都是封装到了 `do_` 中了。而象
    `create` 之类的是直接绑定到某个 engine 上，无法直接使用 `do_` , 所以
    自动创建连接和事务一般还是可行的。象建表目前不建议自动创建，所以都是在命
    令行上来执行的，它们都有特殊的处理。
    同时在处理完毕后，也不能只关闭和提交缺省的连接了，需要对所有创建的连接（包括
    自动创建的连接）执行事务提交和关闭。
    不过这些已经通过修改middle_transaction完成了。所以在简单情况下用户不用过份关心
    这些细节。并且这种做法是兼容只有一个数据库连接的情况。
* 命令行和批处理情况有简单的也有复杂的。简单的情况和web请求的处理类似，也可以在
    开始创建相应的连接和事务，在处理完毕后关闭。复杂情况下也可以自已手工创建连接和
    启动事务。目前在命令行处理时有几个关键点：连接获取，Model的获取。Uliorm是完全
    支持脱离WEB环境来使用的。因此我们可以象test_orm.py中那样，自已去创建连接，
    创建Model，然后创建表。在这种情况下，Uliweb启动时做的自动化处理全部无效了，比
    如缺省的 `AUTO_DOTRANSACTION` 的设置, 缺置的 `Begin` 启动事务等。所以我们要自已去
    启动事务。缺省情况下是自动提交的，所以每执行完一条SQL语句就会生效。
    同时uliweb还支持通过调用 make_application 或 make_simple_application 来启动
    应用的实例。后者是专门为命令行准备了，除了个别的参数不能设外，如：debug，其它的
    都一样。一旦启动，你的开发就和WEB区别不大了。所以缺省情况下 `AUTO_DOTRANSACTION`
    是为 `True` 的。因此你执行 `do_` 时会自动启动事务。但是因为它没有 middleware_transaction
    的封装，所以无法在处理完成后自动提交或回滚。这样如果你自已不处理，结果将无法
    保存。对于这种情况，要么我们直接手工启动事务，以明确的事务方式来工作。要么执行
    `set_auto_dotransaction(False)` 来关闭自动生成事务，从而进入 autocommit 状态。
    所以这点要比较注意。建议在命令行处理时，都主动使用事务。

    {% alert class=info %}
    现在在 `make_simplae_application` 中増加了启动时自动将 `AUTO_DOTRANSACTION`
    关闭的设置。所以使用它来启动应用环境直接就是 `autocommit` 的状态。
    {% endalert %}


前面说了，在使用 `do_` 和 `Begin` 时可以自动在创建线程共享的连接。在Uliorm
中维护着一个Local的对象，它上面有 `conn` 和 `trans` 对象，它们各是一个dict
分别保存着线程相关的连接和事务对象。在调用 `do_` 和 `Begin` 时会先检查是否
存在相应的连接和事务对象，如果存在，则直接使用，如果不存在，则创建。这里，还可以
分别传入 engine_name 参数，用来指明检查某个连接名相关的对象是否存在。线程相关的
连接和事务对象存在的目的是为了编程方便。如果所有的SQL都使用 `do_` 会比较简单。
但是因为 Model 把底层SQL的执行封装到了不同的方法中，所以要么它会自动使用 Model
配置的连接名来获得线程连接对象，要么你通过 connect(engine_name) 切換到其它的连接
名上，以便可以获得其它的线程连接对象，目前也可以传入一个真正的连接对象或Engine对象。


### 命令行对多数据库的支持

为了支持多数据库，在所有数据库相关的命令上都増加了 `--engine` 参数，可以用来
切換连接名。缺省是使用 `default` 。影响较大的是 `dump*` 和 `load*` 系列的函数.
原来数据库的数据文件是缺省放在 `./data` 目录下的。现在为了支持多数据库，将会在
它的下面按连接分别创建子目录， 如： `default` 等。所以一旦使用了多数据库支持的
版本，原来的备份和数据装入的路径就发生了变化。


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


## F&Q


### 如何处理Mysql中的 "MySQL server has gone away" 错误？

出现这个问题是因为Mysql有关于非活动连接超时断开的设置，缺省为8小时。当8小时以后
现有的连接没有活动，则MySql会自动断开。因此再次访问时会抛出这个错误。uliorm
使用SQLAlchemy的缺省的连接方式，会自动使用连接池。默认是5个连接。它有一个pool_recycle
的参数，用于设置回收连接的时间。这样，只要你设置一个小于MySql断开的超时时间就
可以了。示例如下:


```
[ORM]
CONNECTION_ARGS = {'pool_recycle':7200, 'echo_pool':True}
```

上述配置表示：连接池回收时间为7200秒(2小时)。echo_pool为True表示在日志中显示
回收信息。这样是通过自动回收重建连接池避免了这个问题。


### MySQL 编码设置

在MySql中创建表时，uliorm将缺省使用utf8编码来创建，即使MySql的缺省编码不是utf8。
所以如果你使用的是MySql，你应该检查schema的缺省编码是不是utf8，如果不是则应该在
connection连接串上添加charset信息，如:


```
[ORM]
CONNECTION = 'mysql://root:limodou@localhost/new?charset=utf8'
```

当服务器的缺省编码不是utf8时， `charset=utf8` 是必须的，其它情况下可以不设置。

### 如果使用sock文件来连接MySQL

可以在settings中如下配置：

```
[ORM]
CONNECTION_ARGS = {'connect_args':{'unix_socket':'/tmp/mysql.sock'}}
```

其中 `/tmp/mysql.sock` 只是一个示例，你可以改为你需要的sock文件路径。

### 如何实现update table set field = field + 1类似的更新

举例如下:


```
User.filter(User.c.id==1).update(score=User.c.score+1)

或

User.filter(User.c.id==1).update(User.c.score=User.c.score+1)
```

或者使用底层的SQLAlchemy的写法:


```
do_(User.table.update().where(User.c.id==1).values(score=User.c.score+1))
```


### 如何实现MySql中区分大小写字段定义和查询

MySql在定义字段和查询字段时，缺省是使用非大小写敏感方式进行处理的。有时我们需要
进行大小写敏感方式的查询，因此这里涉及两种处理，一种是查询时的大小写区分，如:


```
from sqlalchemy.sql import func

User.filter(User.c.username == func.binary('limodou'))
```

上述代码将按大小写对'limodou'进行查询。

但是如果你把CHAR或VARCHAR设置为不重复的索引，在插入类似： `Limodou` 或 `limodou`
有可能会报重复。这就不是靠查询来解决的了。要通过将字段定义为区分大小写的形式。在
MySql中一般是在VARCHAR之后添加Binary，如:


```
username VARCHAR(40) binary
```

那么在Uliorm或SQLAlchemy中如何做呢？代码如下:


```
from sqlalchemy.dialects.mysql import VARCHAR

class Human(Model):
    name = Field(str, verbose_name='姓名', max_length=40, required=True)
    login_name = Field(str, verbose_name='登录名', required=True,
        max_length=40, unique=True, type_class=VARCHAR,
        type_attrs=dict(binary=True))
```

可以看到它使用了mysql的dialect的字段定义，并将其传入uliorm的字段定义中，其中参
数 `type_class` 为字段类型， `type_attrs` 为字段相应的参数，这里设置 `binary`
为 `True` 。在SQLAlchemy中的定义示例如:


```
from sqlalchemy.dialects.mysql import VARCHAR

Column('username', VARCHAR(40, binary=True))
```

这样在数据库中，就是区分大小写的，在查询时不再需要使用func.binary()来处理了。

不过这种方式兼容性不好，所以还有一种变通的方式就是写一个sql文件，在命令行下对
字段进行修改，这样Model就不需要修改了。比如:


```
use <database>;
ALTER TABLE human MODIFY COLUMN `login_name` VARCHAR(40)
    BINARY CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL;
```


### RuntimeError: dictionary changed size during iteration

在Uliweb下使用uliorm，要求将所有的Model都定义在settings.ini中，一旦出现某个Model
没有在settings.ini中定义，就有可能出现上面的问题。


### 反向获取ManyToMany关系时，找不到对应属性

在Uliweb中，如果两个表存在ManyToMany关系，则关系一般只会定义在其中一个Model类上
被定义。例如有两个Model: A和B。在A上定义了一个到B的ManyToMany的关系。在导入A类
时(或通过get_model来获取)会自动向B类绑定一个反向获取的对象，用于从B的对象获得A对
象时使用。因此，有时候，你直接导入B类，但是因为B类中没有定义与A的任何关系，所以
对A的反向获取对象将无法生成，因此可能不能直接使用B到A的反向获取。在这种情况下，你
可以再使用get_model或导入A，这样就可以生成反向获取对象了。

