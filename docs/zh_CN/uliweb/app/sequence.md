# sequence(序号生成)

在许多数据库引擎中存在sequence的字段类型，但这是数据库自身的机制。在Uliweb中提供了一个类似的简单序号生成的机制。它的功能
很简单，就是对某个唯一的key，从1开始不断生成序号，并且将最大值保存在数据库中，这样这次可以从这个值继承生成新的序号。

考虑到并发情况，它使用了乐观锁机制来处理并发。

## 初始化说明

1. 使用sequence，需要向 settings.ini 中的 `INSTALLED_APPS` 添加 `uliweb.contrib.sequence`
2. 因为序号将要保存到数据库中，故需要在命令行执行 `uliweb syncdb` 来创建相关的表

sequence 的实现并没有使用 redis 等 NoSql 数据库，大家有兴趣可以自行实现或供献给 uliweb

## 使用说明

sequnce 提供了两个api: `get_sequence` 和 `set_sequence` ，使用时可以通过 `functions` 来引用，如：

```
from uliweb import functions

key = 'table'
functions.get_sequnce(key)
```

### get_sequence

```
get_sequence(key, default=1, step=1, retry_times=None, retry_waittime=None)
```

key --
    生成序号的对象可能是很多类型，比如按表来生成，一张表的序号不重复，这时key可以使用表名。还有可能有主表和明细表，
    对于主表的某条记录来说，序号是从1开始的，这时key可以使用 `主表表名+记录ID` 。所以key是可以根据需要由用户来
    生成的，只要不重复就可以了。
default --
    当key不存在时返回的缺省值。缺省为 1。
step --
    表示一次生成几个序号。缺省为 1。对于某些批量的操作，比如一次要插入10条记录，那么如果调用10次序号生成效率是比
    较低的，因此可以传入 `step=10` ，然后第一个序号就是 `返回值 - 9` 。
retry_times --
    当出现并发时，重试次数。如果不传入，缺省按 `SEQUENCE/retry_times` 的值来处理，缺省为3.
retry_waittime(毫秒) --
    如果保存时出现并发冲突， 会自动根据retry_times的值来重试。两次保存之间会按 retry_waittime 的值来等待，如
    果没有传入则按 `SEQUENCE/retry_waittime` 来处理，缺省为 0.05 毫秒。

### set_sequence

```
set_sequence(key, value)
```

如果一个key的序号不正确，需要直接设定为某个值时，可以调用 `set_sequence` 来直接设置。此时将不会重试，一旦执行失
败则抛出相应的异常。

## 其它

通过 `get_sequence` 得到的是一个整数，如果你需要的是一个字符串，一般是有一个前缀的规范，如： `XXX_XX_00001`
之类的，前缀可以根据你的需要自行生成，后面数字部分可以使用 `get_sequence` 来生成。