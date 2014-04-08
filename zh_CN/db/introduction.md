# 数据库使用介绍

## 概述

Uliweb提供了 `uliweb.contrib.orm` 这个APP来实现数据库的基本操作。它是基于
SQLAlchemy库来实现ORM相关的功能。因此，你既可以使用 Uliweb 提供的 ORM 功能，
也可以使用底层的SQLAlchemy功能。

在Uliweb中，可以在web环境与命令行环境（批处理，守护）中使用ORM或数据库。

## 准备

使用 ORM 需要安装依赖的一些模块，如：

* SQLAlchemy (可以使用 0.8+版本)
* 数据库驱动 (Mysqldb, pymysql等)
* 如果考虑使用alembic进行数据库迁移，建议安装我修改过的 alembic，因为它做了与
  uliweb的集成

为了方便安装上面的包，uliweb提供了缺省的命令，如：

```
uliweb install uliweb.contrib.orm
```

这个命令将缺省安装： SQLAlchemy, mysqldb, alembic

然后要向 settings.ini 中添加 `uliweb.contrib.orm` APP，如：

```
[GLOBAL]
INSTALLED_APPS = [
...
    'uliweb.contrib.orm',
...
]
```


## 使用步骤

在项目中使用 Uliorm 要遵守：先定义，后使用的原则（测试代码为了方便可能不采用
这种方式）。因此使用步骤为：

1. 在 models.py 中定义 Model
1. 在 settings.ini 中定义这个Model，如：

    ```
    [MODELS]
    user = 'uliweb.contrib.auth.models.User'
    ```
    
    定义时，前面的名字最好与Model的名字相同，并且使用小写。
    
1. 在使用Model时，使用 `functions.get_model(model_name)` 来获得Model类
1. 在关系定义时，使用settings.ini中定义的名字，而不是直接引用Model类（在0.2.6+
   版本中会抛出警告）。

## 两种事务环境

在web运行态与命令行运行态对事务的处理不同。

* 在web运行态，每个请求会自动创建事务，当请求处理成功，则自动提交，如果存在异常，
则自动回滚事务。
* 在命令行运行态，不会自动创建事务，而是 autocommit 的状态，所以要启动事务，可以
调用 `Begin()`, `Commit()`, `Rollback()` 来手工控制事务。

在应用中，如果需要特别区分是在web运行态还是非web运行态，可以：

```
from uliweb import is_in_web
```

当 `is_in_web()` 返回为 True 时表示在 web 运行态。

## Model 的特殊配置

在定义 Model 时，还有一些配置可以通过 settings.ini 来动态修改，减少直接写在代码
中，这样的配置参数可以定义在：

```
[MODELS_CONFIG]
user = {'__mapping_only__':True}
```

基本上 Model 中可以定义为类属性的都可以在 settings.ini 中进行配置，详细内容参见
ORM 文档中关于表参数的描述。但是对于多数据库配置 `engines`，是需要通过 settings.ini 来配
置的，不能直接在 Model 中设置。

## ORM 与 SQLAlchemy的关系

因为 Uliweb 的 ORM 是基于 SQLAlchemy 实现的，所以一方面它有自已的 ORM 相关的 API，
但同时又与 SQLAlchemy 有密切的关系。主要体现在：

* Model.table 可以得到底层的 Table 实例
* Model.c 和 Model.table.c 的效果一样，就是 Table 实例中字段的字典
* 在Model查询时使用的条件符合 SQLAlchemy 的语法，例如： `Model.c.id==1` 和 `Table.c.id==1` 类似。
* 可以直接使用 SQLAlchemy 的底层函数，如：

    ```
    from uliweb import functions
    from sqlalchemy.sql import select, func
    from uliweb.orm import do_
    
    User = functions.get_model('user')
    sql = select([func.count('*')], User.c.age>40)
    count = do_(sql).scalar()
    ```
    
    