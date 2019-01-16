# 0.3

## 问题修复

* 修正 pyini 中 `"key="` 的值为 `r""` 字符串时的Bug
* 修正 `objcache` APP 中处理 Lazy 字段的Bug。改为：如果第一次发现有 Lazy 字段，将自动从数据库中刷新
* 修正在执行 ORM APP命令时，当出现异常但未抛出的Bug
* 修正 `sync` 命令在执行时，在 `Model.__tablename__` 和 `settings.ini` 中配置名不一致的处理Bug


## 功能优化

* 优化 objcache APP 的实现，添加 `exclude` 的配置项
* 移动 `uliweb/orm/middle*.py` 到 `uliweb/contrib/orm` 目录下
* 移动 `uliweb/i18n/middle_i18n.py` 到 `uliweb/contrib/i18n` 目录下
* 移动 `storgae.py` 从 `core` 目录到 `utils` 目录
* 增加 `SimpleFrame.is_in_web()` 函数，可以用来判断当前运行环境是否在web环境中
* 对 `call` 命令添加 `--gevent` 参数支持
* 在 `redis_cli` APP 中添加 `clear_prefix()` 方法，可以用来清除某个前缀开始的所有key，需要 redis 在 2.6 版本以上
* 当 session 在使用数据库存储时，如果没有给出数据库连接串，则自动使用ORM的配置
* `settings.ini` 和 `local_settings.ini` 的配置可以通过环境变量来指定，分别为： `SETTINGS` 和 `LOCAL_SETTINGS`
* `generic` APP 的自动代码框架中，添加对 avalon 和 mmgrid 的支持。
* generic.py 在保存时添加对乐观锁的支持，可以传入 `(version=True, version_fieldname='version')` ，如果版本字段
  为 `version` 则，`version_fieldname` 可以省略
* generic.py 在 AddView 和 EditView 中添加 `save` 回调参数

## ORM 相关优化

* 重构多数据库支持，包括对数据库相关文档的结构调整
* 优化 ORM 的 count
* 删除 `get_cached()` 方法，在 `Model.get()` 中添加 `cache` 参数
* ORM 中，对于 CHAR 和 VARCHAR 类型， `Property.to_str()` 将只返回 string 类型，而不是 unicode
* 简化 server_default 的处理，对于整数缺省值，将自动转换为 `text(n)`
* `ManyResult.all()` 增加 `cache` 参数用来缓存结果
* 优化 `dump()` 和 `load()` 的处理，添加对 PickleType, ManyToMany 类型的支持，主要用在 objcache 中
* 删除当存在其它主键字段时，不再创建 ID 字段的判断，主要是为了可以支持多主键的处理。
* 添加对 MySQL 分区定义的支持，如：

    ```
    __table_args__ = {
        'mysql_partition_by':'HASH(YEAR(create_time))',
        'mysql_partitions': '6'
    }
    ```

* 添加对 None 因为 SQLAlchemy 0.9 版本变化的兼容性处理，可以配置为 `'empty` 或 `'exception'`
* 向 Result, ManyResult 添加 `any()` ，用来判断是否至少存在一条满足条件的记录
* 向 `get()` 、 `get_object()` 和 `get_cached_object()` 函数中添加 `id` 参数，所以如果指定的
  `id` 如果不能在 cache 中找到时，可以使用 `condition` 参数来进行查询。如果两个参数全部给出，只有当 `id`
  不是一个整数或不是一个有效的表达式时 `condition` 才会被使用。所以通常情况下你不需要传入 `condition`
* 修改 ORM APP 的 requirement.txt 文件，将 alembic 改为 uliweb-alembic
* `Model.put()` 方法被设为 Deprecated ，将在下一个版本中删除，要统一使用 `save()`