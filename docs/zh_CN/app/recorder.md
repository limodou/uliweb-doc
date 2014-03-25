# recorder(请求记录与回放组件)

## 功能介绍

Web测试一直是很麻烦的一件事，因为它涉及到前端、后端，涉及界面，服务。开发 recorder
的目的不是为了测试前端，而是测试后端。它的基本想法是：把用户的操作请求与应答通
过录制的方式记录下来，然后生成脚本，再执行，检查对应的输出结果是否符合预期。

在测试执行时与一般的web测试不同，它并不需要真正启动web服务，象命令一样运行就可以
了。因为，recorder可以创建应用的实例，并调用实例的接口来执行请求。

## 使用说明

### apps/settings.ini中的配置

首先要在settings.ini中配置 recorder, 如：

```
INSTALLED_APPS = [
...
'uliweb.contrib.recorder',
...
]
```

### 初始化数据库

recorder 需要使用数据库来保存录制下来的数据，因此可以使用：

```
uliweb syncdb
#or
uliweb alembic diff -f
uliweb alembic upgrade
```

进行相应表结构的创建

### 打开录制状态

```
uliweb recorder start
```

### 用户操作

用户此时可以在界面进行相应的操作。对于需要权限或用户登录的处理，建议先从登录
页面开始操作。此时，用户操作的请求会记录在数据库中。静态请求将不会记录。

### 生成脚本

```
uliweb recorder print [filename]
```

如果没有给出文件名，则脚本将输出到控制台。 `print` 命令将生成一个 .py 的脚本。
生成的脚本内容如：

```
import os
from datetime import datetime

from uliweb.utils.test import client
c = client('.')
print 'Current directory is %s' % os.getcwd()
print

#log = 'recorder_test_%s.log' % datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
log = True

c.test_url('/login', data={}, method='GET', ok_test=200, log=log)
c.test_url('/login', data={"username":"xxxx","password":"yyyy","next":"/"}, method='POST', ok_test=302, log=log)
c.test_url('/', data={}, method='GET', ok_test=200, log=log)

#total 88 records output, time used 0s
```

上面的 `c = client('.')` 将创建一个测试用的客户端对象。它需要一个启动应用的路
径作为参数。上面 `'.'` 表示当前目录就是应用的目录。如果你生成的文件在其它的目录
下，那么你要手工修改一下，让它可以正确找到你的应用目录。

这个客户端提供 `get`, `post` 等方法，但是，它将返回 Response 对象，所以使用它
们的话，还需要自已去写判断结果的代码。

因此客户端还提供了 `test_url` 的方法，它可以测试相应的 url 并且与 `ok_test` 的值
进行比较，并将结果输出。详情参见下面的具体描述。

log 用来控制结果输出。这里 `log=True` 表示输出到控制台。但是在测试时，会和日志输
出混在一起，所以最好是输出到文件名。上面注释掉的一行就是日志文件的生成。按日期和
时间，如果认为不合适可以进行手工修改。

### 编辑或执行

在文件生成之后，即可以直接运行。但是你还可以再编辑一下，比如删除重复的请求，
对请求数据进行加工。

这是一个可能的输出结果：

```
Current directory is /home/uliweb/project/blog

Testing /login...OK
Testing /login...Failed
    ok_test = 302
    Response code=200
Testing /...OK
```

上面会列出当前执行的目录。然后下面是结果。如果成功，最后是 `OK` ，如果失败，则
为 `Failed` ，同时列出检查条件，上面是 `ok_test=302` 及响应码。因为预期的响应
码和返回的不同，所以出错。正文因为有可能太长，所以没有列出来。你可以自已写一个
log函数将其输出。

## test_url() 说明

### 函数原型

```
def test_url(url, data=None, method='get', 
    ok_test=(200, 304, 302), log=True):
```

url --
    待执行的URL
    
data --
    待上传的数据
    
method --
    请求的方法名
    
ok_test --
    检查是否成功的条件
    
log --
    结果输出

### `ok_test` 比较模式

1. tuple, list 类型

    如果是这些类型，则会认为它们是status_code的集合，只要 Response 对象的状态码
    在这个范围内都认为成功。
    
2. int, long 类型

    如果是上述类型，则认为是status_code值，只要 Response 对象的状态码等于这个值
    则成功。
    
3. str, unicode 类型

    如果是上述类型，则认为如果响应的文本中包含这个字符串则认为成功。
    
4. 可调用类型

    如果是可调用类型，则将执行这个对象，将传递 `(url, data, method, status_code, response_data)`
    供用户自行处理。
    
### 日志输出

`test_url` 支持几种日志输出方式

1. log=True

    将输出结果到控制台
    
2. log='filename'

    结果将以追加方式输出到指定的文件中
    
3. log=可调用对象

    将执行这个对象，需要定义此函数为：
    
    ```
    def log_func(url, data, method, ok_test, result, r):
        """
        url 请求链接
        data 数据
        method 方法
        ok_test 测试条件
        result 测试结果
        r 响应的 Response 对象
        """
    ```

## recorder 命令行

### 查看帮助

运行：

```
uliweb help recorder
```

可以查看 recorder 所带的全部命令

### clear - 删除已录制所有数据

```
uliweb recorder clear
```

### start - 开启录制状态

```
uliweb recorder start
```

### stop - 关闭录制状态

```
uliweb recorder stop
```

### status - 查看当前状态

```
uliweb recorder status
```

### print - 生成脚本

```
uliweb print <output.py>
```

如果不给出文件名，结果将输出到控制台。

详细的帮助信息：

```
Usage: uliweb recorder print [options] [--time begin_time] [--id begin_id] outputfile

Print all records of recorder.

Options:
  --time=BEGIN_TIME     All records which great and equal than this time will
                        be processed.
  --id=ID               All records which great and equal than the id value
                        will be processed.
  --template=TEMPLATE   Output template file. Default is recorder.tpl.
  --template_row=TEMPLATE_ROW
                        Easy rocord fo recorder output template file. Default
                        is recorder_row.tpl.
```

`time` 和 `id` 可以用来控制输出的范围。不过这样要查数据库才知道。

`template` 和 `template_row` 分别对应输出脚本的模板，一个用于整体代码，一个用于
每条记录的生成。你可以自已写模板进行替換。 recorder 已经提供了缺省模板，就在
`uliweb.contrib.recorder` 的 `template_files` 目录下。

## 注意事项

此功能强烈要求在测试环境下使用，因为：

> 这个功能会把用户输入的信息原样保存，所以象登录操作，会把密码录制下来，以
> 明文的形式生成脚本。会存不安全的情况。另外，会占用数据库空间。