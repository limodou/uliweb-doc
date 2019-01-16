# F&Q


## 如何处理Mysql中的 "MySQL server has gone away" 错误？

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


## MySQL 编码设置

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

## 如何实现update table set field = field + 1类似的更新

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


## 如何实现MySql中区分大小写字段定义和查询

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


## 反向获取ManyToMany关系时，找不到对应属性

在Uliweb中，如果两个表存在ManyToMany关系，则关系一般只会定义在其中一个Model类上
被定义。例如有两个Model: A和B。在A上定义了一个到B的ManyToMany的关系。在导入A类
时(或通过get_model来获取)会自动向B类绑定一个反向获取的对象，用于从B的对象获得A对
象时使用。因此，有时候，你直接导入B类，但是因为B类中没有定义与A的任何关系，所以
对A的反向获取对象将无法生成，因此可能不能直接使用B到A的反向获取。在这种情况下，你
可以再使用get_model或导入A，这样就可以生成反向获取对象了。

## None 条件在0.9.X中的变化

None在0.9以前的版本中，如果进行 & 操作，会自动丢弃。但是在 0.9.X 中却会变成 NULL，
所以以前这样的写法：

```
cond = None
for c in conditions:
    cond = c & cond
```

就不再正确了，要改为：

```
from uliweb.orm import true
cond = true()
for c in conditions:
    cond = c & cond
```

`true` 也可以从 sqlalchemy.sql 中导出。

**0.3+ 变化** --
    在0.3+版本中，增加了对 None 的兼容处理。详情参见 [ORM基本使用/PATCH_NONE](orm.html#patch) 的说明。