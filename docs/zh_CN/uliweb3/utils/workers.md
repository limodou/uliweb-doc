# Workers - 多进程执行

## 背景

在很多时候，需要将一个任务通过异步方式来执行，因此就需要考虑使用象celery这样的软件，它就是一个分布式的任务
执行的框架。也有时候需要实现一个守护，来自动执行一些命令，为了并发，需要启动多个进程来并行处理。在我的应用
场景中，存在这么一种情况：存在许多的队列需要监听处理，它是一个IP和队列的组合，如：

```
('ip1', 'queue1'),
('ip1', 'queue2'),
('ip2', 'queue1'),
('ip2', 'queue2'),
```

整个处理是完全相同的，区别的只是监控的IP和队列不同，因此希望针对这些参数启动不同的守护进程。如果考虑使用
supervisord工具，那么写守护就是一件很简单的事情。

为了实现这个场景，我的设计是实现两个类，一个用来进行调度，一个用来实现队列的处理。其实简单的做法只要实现队列
处理就可以了，这样只要在supervisord中配置不同的入口即可，只是麻烦的地方是：配置上基本上一致，只是启动参数
不同，并且当调整监听队列的数量时，要修改supervisord配置入口。因此我想实现只启动一个主进程，由它来自动启动
子进程的方式，这样supervisord中只需要配置一个入口，修改参数也只是改动主进程的配置文件。

## 功能要求

在实现时，我希望实现以下几个功能：

* 主进程自动维护子进程，当存在子进程退出情况，主进程自动重启
* 对子进程可以进行限制:
    * 执行次数限制。当执行次数达到上限时，重新创建新的子进程
    * 执行超时限制。当执行一个命令的时间超过一定的时间，结束子进程并重新创建新的子进程
    * 执行内存限制，软限制和硬限制。软限制的阀值应小于硬限制。当子进程使用内存超过软限制，将发出SIGTERM
      信号，等待子进程正常结束。当子进程使用内存超过硬限制，将发出SIGKILL信号，强行将子进程终止
* 主进程退出时，自动结束子进程

这个程序只是实现了一个调度的框架，所以真正在使用时，还需要根据需求进行定制方可使用。

## 实现

根据上面的功能要求，我设计了两个类：Worker和Manager，一个是用来进行子进程的处理，一个是用来对子进程进行
管理。最后的代码是写在了 `uliweb/utils/workers.py` 中。

Worker用来实现每个命令的执行，包括命令执行前的初始化以及退出时的一些清理工作。为了通用，Worker本身是以子
进程方式来工作，它自身会不断循环，因此命令的获取是在Worker中实现的。

Manager是用来进行管理，但不进行调度，所以它和Worker进程间除了向它发出信号，目前没有其它的交互。这一点和
Celery是有所区别的。当然，通过数据库或队列之类的工具是可以实现间接的通讯，应该扩展一下就可以。不过这个模
块主要的定位是Worker的执行，扫描处理或调度可以单独写一个守护，然后通过队列之类的方式实现与Worker的通信。

## 运行要求

使用它需要安装：

* psutil

因为使用了 fork 所以这个模块只能在 Linux 相关的系统上使用，windows是不行的。

## 使用

### 基本说明

```
from uliweb.utils.workers import Worker, Manager
import time

class MyWork(Worker):
    def run(self):
        self.log.info('running')
        time.sleep(1)
        return True

workers = [MyWork()]
manager = Manager(workers)
manager.start()
```

上面的例子中，先实现了一个简单的Worker类，将要执行的功能放在了 `run` 方法中，功能是打印 `running` 信息。
要注意:

* `time.sleep(1)` 用于让进程等一秒钟，不要让程序运行太快。
* `return True` 表示成功处理，这样请求的计算可以加1,不然会认为没有命令被执行

`Manager` 接收一个 Worker 的数组，通过执行 `start()` 来启动守护。

{% alert class=info %}
这个程序不是真正的守护，它只是一个死循环，所以可以利用supervisord工具来管理成为一个守护。
{% endalert %}


### Worker 的定制

因为 workers 模块只提供了一个基本的框架，所以通常你需要对它进行定制，对于Worker主要可以定制以下内容：

#### 参数定义

name --
    用于给Worker实例起名字，如果不给由缺省使用 `Process` ，同时按启动的顺序在每个名字后面会添加一个序号。
log --
    日志输出对象，如果不给则缺省为 `logging.getLogger(__name__)`
`*args, **kwargs` --
    额外参数，可以用于Worker的初始化中
max_requests --
    最大处理请求个数，不提供则不限制
soft_memory_limit （单位MB） --
    软内存限制，缺省为 `200MB`。当内存达到这个限制时，会收到 `SIGTERM` 的信号，允许Worker尝试正常退出
hard_memory_limit （单位MB） --
    硬内存限制，缺省为 `300MB`。当内存达到这个限制时，会收到 `SIGKILL` 的信号，Worker将强制结束
timeout （单位秒） --
    运行超时限制。缺不处不限制。当运行时间超过超时时间，将引出超时异常从而退出。
check_point （单位秒） --
    Worker循环间隔时间。缺省为None，表示不等待。因此，Worker的两次执行间的间隔时间可以有两种方式来控制：

    * 在 `run()` 方法中手工添加 `time.sleep(n)` 的代码
    * 在创建Worker时给出 `check_point` 的参数

#### 方法扩展

Worker 还提供了一些预置的方法，供扩展使用。Worker在启动时会按照以下方法执行：

```
self.init()
self._run()
self.after_run()
```

init() --
    用于实现初始化的扩展
_run() --
    内存使用，不用于扩展。它会调用 `run()` 方法，你应该对 `run()` 进行扩展。
run() --
    在 `_run()` 中被调用，用于实际任务的一次执行。如果存在象对表的扫描，可以在这个方法中进行循环。在这个
    方法执行完毕后，如果判断为一次正确的执行，应返回 `True` ，以便Worker进行执行次数的计数处理。
after_run() --
    Worker结束或中止（收到`SIGTERM`信号）时执行，可以用于执行清理动作。对于强制中止则不会触发。

### Manager 的定制

#### 参数定制

log --
    日志输出对象，如果不给则缺省为 `logging.getLogger(__name__)`
check_point （单位秒） --
    对子进程进行检查的间隔时间
wait_time （单位秒） --
    等待子进程结束的时间
title --
    启动主进程时，显示Banner中的标题

### 复杂一点的例子

```
import time
import logging
from uliweb.utils.workers import *

logging.basicConfig(level=logging.INFO)

class NewWorker(Worker):
    def init(self):
        self.log = make_log(self.log, 'new_worker.log')
        super(NewWorker, self).init()

    def run(self):
        s = []
        for i in range(50000):
            s.append(str(i))
        self.log.info ('result= %d ' % len(s))
        time.sleep(1)
        return True

workers = [Worker(max_requests=2),
           NewWorker(max_requests=2, timeout=5, name='NewWorker',
                     soft_memory_limit=5, hard_memory_limit=10)]
manager = Manager(workers, check_point=1)
manager.start()
```

这个例子要复杂一些，它主要实现了以下几点功能：

* 在 `NewWorker.init` 中对 `self.log` 进行了处理。其中 `make_log()` 是在 `workers.py` 中定
  义的函数，你也可以自已写。它的代码如下：

    ```
    FORMAT = "[%(levelname)s - %(asctime)s - %(filename)s:%(lineno)s] - %(message)s"

    def make_log(log, log_filename, format=FORMAT, datafmt=None, max_bytes=1024*1024*50,
                 backup_count=5):
        import logging.handlers

        if isinstance(log, (str, unicode)):
            log = logging.getLogger(log)

        handler = logging.handlers.RotatingFileHandler(
            log_filename, maxBytes=max_bytes, backupCount=backup_count)
        fmt = logging.Formatter(format, datafmt)
        handler.setFormatter(fmt)
        log.addHandler(handler)
        return log
    ```

    它将向log对象添加 `RotatingFileHandler` 这个Handler ，这样日志就可以按大小自动切分，缺省为50M，
    最多5个文件。
* 在 run 中的代码只是为了让内存足够大好测试是否内存的控制可以起作用。
* 在创建 NewWorker时分别指定了一些参数，具体的作用看前面对Worker的说明。
* Worker本身也是可以运行的，只不过它只是输出日志，所以只是用来测试使用，一般都要从 `Worker` 类进行派生。

### Redis的例子

让我们设想基于redis的Worker功能，利用redis的数组的阻塞方法 `brpop`，可以把 redis 当成消息队列。示例
代码如下：

```
import logging
from uliweb.utils.workers import *
import redis

logging.basicConfig(level=logging.INFO)

class NewWorker(Worker):
    def init(self):
        super(NewWorker, self).init()
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def run(self):

        message = self.redis.brpop('redis_queue', 10)
        if message:
            self.log.info(message[1])

            return True

workers = [NewWorker(max_requests=2, name='Redis Worker')]
manager = Manager(workers, check_point=5)
manager.start()
```

启动时可以看到如下的结果：

```
INFO:uliweb.utils.workers:=============================
INFO:uliweb.utils.workers:Workers Daemon Starting
INFO:uliweb.utils.workers:=============================
INFO:uliweb.utils.workers:Daemon process 83307
INFO:uliweb.utils.workers:Check point 5s
INFO:uliweb.utils.workers:Redis Worker-1 83308 created
```

主进程的PID是83307，检查时间是5秒钟。

子进程的名字是使用了传入的 `name` 加上一个序号。后面跟着的是它的PID。

然后我们使用`redis-cli`来进行测试：

```
lpush redis_queue "hello"
```

可以看到:

```
INFO:uliweb.utils.workers:hello
```

再执行一遍时，会是：

```
INFO:uliweb.utils.workers:hello
INFO:uliweb.utils.workers:Redis Worker-1 83308 cancelled by reaching max requests count [2]
INFO:uliweb.utils.workers:Redis Worker-1 83308 is not existed any more.
INFO:uliweb.utils.workers:Redis Worker-1 83309 created
```

说明达到了子进程的最大个数被，因此 `Worker-1 83308` 被取消了，然后后面自动又创建了一个新的子进程。

这里redis有一个小问题，那就是如果取出一条消息，但是在处理时子进程退出了，会造成消息丢失，所以可以将消息
处理的方式修改一下。这里我们将使用 `brpoplpush` 命令具体的参数可以看[它的文档](http://redis.io/commands/brpoplpush).

原理是：为每个子进程创建一个queue，然后通过 `brpoplpush` 将消息从公共的队列中搬到子进程的工作队列中，
这样一旦子进程因为意外退出，下次再启动时先读取工作队列，然后再处理公共队列，从而保证数据不丢失。

示例代码如：

```
import logging
from uliweb.utils.workers import *
import redis

logging.basicConfig(level=logging.INFO)

class NewWorker(Worker):
    def init(self):
        super(NewWorker, self).init()
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.queue = self.kwargs['queue']

    def get_message(self):
        message = self.redis.lindex(self.queue, 0)
        if not message:
            message = self.redis.brpoplpush('redis_queue', self.queue, 10)

        return message

    def run(self):

        message = self.get_message()
        if message:
            self.log.info(message)
            self.redis.lpop(self.queue)

            return True

workers = [NewWorker(max_requests=2, name='Redis Worker', queue='worker')]
manager = Manager(workers, check_point=5)
manager.start()
```

这里主要的变化有：

* NewWorker 中传入了 `queue='worker'` 的参数，用来指定子进程内部的queue。不同的子进程应该
  定义不同的名字。
* 定义了一个 `get_message()` 方法来实现前面说的：先从工作队列中读消息，然后再从公共队列中读消息。

## 与Celery的区别

Celery是一个分布式的任务执行工具，因此它一般是当有需要执行的异步方法时，通过提供异步任务来执行。而workers
只是多进程执行的简单框架，并不限制是否有异步的任务，通过扩展，你可以实现异步的任务，也可以只是单纯的自循环的
守护，比如扫描数据库或监时消息队列。



