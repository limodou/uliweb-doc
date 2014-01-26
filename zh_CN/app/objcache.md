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
key_format = 'OC:%(engine)s:%(tablename)s:%(id)s'
```

enable
:   用来切換objcache功能是否启动的标志。缺省是启用。

timeout
:   用来设置失效时间。缺省为一天。如果为0表示不失败。这是一个全局性的设置，在
    定义每张表时，还可以单独对某张表进行控制。
    
key_format
:   用来控制缓存时的key的生成规则。这里engine, tablename, id都是自动提供的。你
    只能修改除它们之外的内容。engine是给多数据库使用。
    
### Model的配置

哪个Model可以使用缓存的功能还需要再进一步进行配置，可以有几种配置方式，如：

```
[OBJCACHE_TABLES]
tablename = field1, field2, ...
tablename = 
tablename = {'fields':[field1, field2, ...], 'expire':xxx, 
    'key':other_key_name, 'fetch_obj':'xxx.xxx.func'}
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

fetch_obj
:   当key不是使用缺省的ID，并且也不是Model中存在的字段时，那么它是计算出来的，因
    此在需要缓存对象时，需要手工来获取对象并返回，此时可以定义这个回调函数，定义
    格式及示例为：
    
    ```
    def fetch_obj(model, id):
        return model.get(model.c.field==id)
    ```
    
    将上面函数的字符串路径配置到 `fetch_obj` 对应的值即可。

## 使用示例

目前uliweb还没有提供自动cache的功能，所以需要显示地使用API来进行处理。

```
    def get_object(table, id, cache=False, fields=None, use_local=False, engine_name=None)
```

`get_object()` 有几下几个功能：

1. 从cache中读取某条记录，如果不存在，则直接从数据库中读取
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