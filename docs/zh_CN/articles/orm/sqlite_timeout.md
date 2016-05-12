# uliweb里sqlite的timeout参数

(整理自[google groups相关讨论](https://groups.google.com/d/topic/uliweb/cv8J3T1_EH8/discussion))

本来uliorm里是支持CONNECTION_ARGS参数的,那么应该要能这么用:
(加timeout参数的原因可以参考[这里](http://stackoverflow.com/questions/15065037/how-to-increase-connection-timeout-using-sqlalchemy-with-sqlite-in-python))

```
[ORM]
CONNECTIONS = {
    'default':{
        'CONNECTION':'sqlite:///database.db',
        'CONNECTION_ARGS':{'timeout': 8.0},
        'CONNECTION_TYPE':'short',
    }
}
```

但是因为sqlalchemy的实现,在数据库引擎为sqlite的时候不支持这么用,而是在数据库url里给出,例子:

```
[ORM]
CONNECTIONS = {
    'default':{
        'CONNECTION':'sqlite:///database.db?timeout=8.0',
        'CONNECTION_TYPE':'short',
    }
}
```
