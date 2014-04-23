# objcache(对象缓存)

objcache是为了解决这样一种处理场景：大量的操作是通过id来获取数据，因此它更接近
于key-value的处理模式。因此，objcache是希望把这种常见的操作转为对缓存的处理。所
以这就是objcache产生的原因。

## 配置说明

### apps/settings.ini中的配置

首先要在settings.ini中配置 objcache，如：

```
INSTALLED_APPS = [
...
'uliweb.contrib.objcache',
...
]
```

objcache目前只支持使用redis。所以还需要使用 `uliweb.contrib.redis_cli` ，不过它
已经作为依赖app配置在 objcache 的 config.ini 中了，因此只要配置 objcache 就可以了。

### 全局性配置

有一些全局性的配置项可以在需要的时候进行修改：

```
enable = True
timeout = 24*3600
table_format = 'OC:%(engine)s:%(table_id)s:'
key_format = table_format + '%(id)s'
```

enable
:   用来切換objcache功能是否启动的标志。缺省是启用。

timeout
:   用来设置失效时间。缺省为一天。如果为0表示不失败。这是一个全局性的设置，在
    定义每张表时，还可以单独对某张表进行控制。

table_format
:   用来定义key的前缀生成规则，与下面的key_format联用。

    {% alert class=info %}
    上面table_id将会使用 `uliweb.contrib.tables` 来获得一个表对应的id，如果你不想
    使用它，而是用表名，可以在自已的settings.ini中定义为： 
    
    ```
    table_format = 'OC:%(engine)s:%(tablename)s:'
    ```

    这里engine, tableid, tablename, id都是自动提供的。
    {% endalert %}
    
key_format
:   用来控制缓存时的key的生成规则。
    
    
### Model的配置

哪个Model可以使用缓存的功能还需要再进一步进行配置，可以有几种配置方式，如：

```
[OBJCACHE_TABLES]
tablename = field1, field2, ...
tablename = 
tablename = {'fields':[field1, field2, ...], 'expire':xxx, 
    'key':other_key_name_or_function_path}
```

上面列出了常见的三种配置方式，其中第一种和第二种差不多，唯一的区别就是第一种设置
了具体哪些字段需要缓存，这样没列出来的不会放在缓存中。第二种则表示所有字段都需要
缓存。

第三种为更精确的设置，它的值是一个dict，其中各参数的作用为：

fields
:   如果提供了，应该是一个tuple或list。如果没提供，则是所有字段。

expire
:   用来表示这个实例缓存记录的超时时间。如果没提供，则使用全局的设置。为0表示不超时。

key
:   缺省objcache会使用对象的id进行保存，如果你想使用其它的字段作为键值，可以用
    它来指定别的字段名。如果key的值是计算的结果，那么还可以传入一个函数路径，如：
    `blog.views.key`, 它的定义格式为：
    
    ```
    def key(obj):
        return obj.a1+':'+obj.a2
    ```


## 使用示例

Uliweb 提供了两个API来处理缓存： `functions.get_object()` 和 `functions.get_cached_object()`.
其中 `get_cached_object()` 就是调用的 `get_object()` 中不过自动将 `cache` 和 `use_local` 
两个参数默认设为 `True`。

{% alert class=info %}
**New in 0.3**  目前可以在 Model 中定义 `__cacheable__` 来自动启动cache处理。
{% endalert %}

```
def get_object(table, id, condition=None, cache=False, fields=None, 
    use_local=False, session=None)
```

`get_object()` 有以下几个功能：

1. 从cache中读取某条记录，如果不存在，则直接从数据库中读取。

    {% alert class=info %}
    **New in 0.3** 如果id在redis中不存在，则Uliorm会尝试用id的值从数据库中读取，但是它会缺省认
    为id的值是Model.c.id字段对应的值。这在大多数情况下是有效的，但是对于自定义
    的key值（如使用了非id的字段作为key），这样是取不到数据的。所以在这种情况下，
    你可以传入condition参数，它就是一个条件，当按id找不到对应的值时，使用condition
    从数据库中获取数据。 
    {% endalert %}
    
2. 不使用cache, 直接从数据库中读取记录的功能
3. 在使用缓存的情况下，使用线程缓存作为二级缓存
4. 指定要读出的字段来生成返回的对象，对于未指定的字段，缺省为Lazy状态，则当通过
   实例来访问时会引发底层的完整读取

### 示例1

```
blog = functions.get_object('blog', 1)
```

从blog表中读取ID为1的记录。

### 示例2

```
blog = functions.get_object('blog', 1, cache=True)
```

从redis缓存中读取ID为1的对象，如果缓存中不存在，则自动从数据库中获取。

### 示例3

```
for i in range(5):
    blog = functions.get_object('blog', 1, cache=True, use_local=True)
```

使用缓存读取，同时启用二级缓存。则第一次从redis中读取，但是后面在读取相同的ID
记录时，从二级缓存中读取。

注意，二级缓存在WEB处理环境中，会在请求处理前自动清空，在响应返回前也清空。

### 示例4

`settings.ini`

```
[OBJCACHE_TABLES]
blog = {'key':'subject'}
```

这个配置修改了原来使用id作为key的处理，改为使用 `subject` 字段。

读取时：

```
Blog = functions.get_model('blog')
obj = functions.get_object('blog', 'title1', condition=(Blog.c.subject=='title1'),
    cache=True, use_local=True)
```



## 关于日志

为了方便调试，objcache有很多地方会输出 DEBUG 级别的日志。而Uliweb的缺省日志级
别是 `info` ，所以如果你想要查看，可以在settings.ini中设置：

```
[LOG]
level = 'debug'
```

这样，是把整个应用的日志级别改为了 `debug` 。如果只想设置objcache的日志信息，
可以：

```
[LOG.Loggers]
uliweb.contrib.objcache = {'level':info}
```