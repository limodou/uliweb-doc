# 0.2.5

* 修复 config 的模板，添加 `uwsgi` 的shell方式支持
* 向 `settings.ini` 中添加对环境变量的支持。例如，在环境变量中定义了 `MYSQL_PORT`,
  你可以在 settings.ini 中定义：

    ```
    [DEFAULT]
    port = $MYSQL_PORT
    port_str = '${MYSQL_PORT}'
    ```

    `$MYSQL_PORT` 与 `${MYSQL_PORT}` 是一样的。当变量后面跟着标识符时，使用 `${}`
    可以容易地将它分区分开。
* 添加 `STATIC_COMBINE_CONFIG` 配置项，你可以用它来切換是否启动静态文件合并。缺
  省是 `False`. 配置格式为：

    ```
    [STATIC_COMBINE_CONFIG]
    enabled = False
    ```

* 向 `functions` 中添加 `get_table()` 函数，你可以用它来获得 table 对象。它是
  定义在 `uliweb.contrib.tables` app中的。
* 添加 `local_cache` 的支持，可以用来存储与请求相关的缓存值。它会在每个请求处理
  完毕之后被清除。
* 优化 `get_object()` 函数，添加 `use_local` 参数，所以缓存的值将在 `local_cache`
  中先进行检查，并且将从缓存或数据库中获取的值保存在 local_cache 中。
* 优化 objcache 的配置格式，你可以如下定义：

    ```
    user = {'fields':['username'], 'expire':expire_time,
        'key':callable(instance)|key_field}
    #or
    user = ['username', 'nickname']
    #or
    user =
    ```

    如果没有定义 `fields` ，将使用Model中定义的全部字段。如果 `expire` 为0或没有
    定义，将不会失效。

    `key` 将用来替換 `id`, 缺省为 `id`, 当你需要其它的key值时才需要定义。它也可以
    是一个 callable 对象，可以接受一个 Model 的实例参数。所以你可以创建任何想要的
    key值。
* 向ORM中添加乐观并发控制支持，使用它，需要先在 Model 中定义一个 `version` 字段，
  然后当你在保存对象时，需要乐观锁的处理时，需要使用：

    ```
    obj.save(occ=True)
    ```

    如果在保存时有其它的操作已经保存了记录，它将缺省引发一个 `SaveError` 的异常，
    因为 version 已经被改变了。你还可以传入其它的参数：

    * `occ_fieldname` 用于定义 version 字段名，缺省是 `version`
    * `occ_exception` 用来控制是否允许引发异常，缺省为 `True`.