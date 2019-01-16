# celery

## 初始化

启用celery，需要在 `settings.ini` 中的 `INSTALLED_APPS` 中添加 `'uliweb.contrib.celery'` ，同时要
安装celery包

## 配置
`uliweb.contrib.celery` 本身提供了一些配置项

```
[CELERY]
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {}

[BINDS]
celery.after_init_apps = 'after_init_apps', 'uliweb.contrib.celery.after_init_apps'

[FUNCTIONS]
async_task = 'uliweb.contrib.celery:app.task'
async_run = 'uliweb.contrib.celery.tasks.common_celery_task'
```

其中 `BROKER_URL` 和 `CELERY_RESULT_BACKEND` 分别使用了redis，所以如果你继续使用redis，要自已安装redis，
然后启动它。也可以按celery的文档换成其它的后端。 `CELERYBEAT_SCHEDULE` 目前主要是想用来实现一些调度的功能，
但是这块还没有真正完成，可能要修改。

`FUNCTIONS` 中定义了两个函数，一个是用于将某个函数声明为celery的任务，而另一个则是不用声明直接以celery的
方式来调用一个函数。

## 命令行
`uliweb.contrib.celery` 提供了命令行工具，可以通过 `uliweb celery` 看到它的帮助。不过具体的celery
的命令，还是要参考celery的文档，如启动celery服务为 :  `uliweb celery worker` 。好象-A app 不指定也可以。

## 定义任务
celery的任务函数编写提供了两种方法，一种是和celery一样，要声明。那么
这样的任务可以写在每个app下的 `tasks.py` 中，例如：

```
from uliweb import functions

@functions.async_task
def add(x, y):
    return x+y
```

然后在调用的view中可以：

```
@expose('/celery')
def celery():
    from tasks import add

    result = add.delay(4,4)
    return result.get()
```

另一种写法是不用事先定义task，而是使用uliweb.celery定义好的一个方法来直接调用，如：

```
def p(name):
    return name

@expose('/celery_common')
def celery_common():
    result = functions.async_run.delay('test1.views:p', 'hello')
    return result.get()
```

上面代码p是一个普通函数，如果想要异步调用它，可以直接通过functions.async_run.delay()来调用，第一个
参数是p这个函数的路径，采用 module:function_name的方式。后面是对应的参数。

不过这两种方法，async_task可以接受原celery可以接受的参数，这样就更灵活。而async_run则相当于预先写好
了一个task，所以它的参数相对固定，不太灵活，可能对于简单使用足够了。你也可以仿照async_run的作法预定义一
些固定的场景。