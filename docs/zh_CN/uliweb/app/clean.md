# clean

## 说明

Uliweb提供了一个清理命令,目前支持对目录和Model的清理.目录清理可以直接使用,但是Model的清理要有相应的处理代码.

clean 提供了两个子命令:

dir --
    清理目录
    
model --
    清理Model
    
## 命令行说明

### dir

使用格式为:

```
uliweb clean dir [options] directory
```

命令行选项:

```
Options:
  -e EXTENSIONS, --extension=EXTENSIONS
                        Only matches extension. E.g. .txt
  -x EXCLUDE_EXTENSIONS, --exclude_extensions=EXCLUDE_EXTENSIONS
                        Not matches extension.
  -r, --recursion       Recursion the directory.
  -d DAYS, --days=DAYS  Delta days before now.
```

-e EXTENSIONS, --extension=EXTENSIONS --
    表示要处理的扩展名,扩展名为 `.txt` 的形式.如果有多个扩展名可以设置多个,如: `-e .txt -e .bak`.
    
-x EXCLUDE_EXTENSIONS, --exclude_extensions=EXCLUDE_EXTENSIONS --
    表示要排除的扩展名,可以是多个.
    
-r, --recursion --
    表示对子目录进行递归处理.
    
-d DAYS, --days=DAYS --
    表示要清除DAYS天前的文件
    
    
### model

使用格式为:

```
uliweb clean model [options] model_name
```

命令行选项:

```
Options:
  -d DAYS, --days=DAYS  Delta days before now.
  -c COUNT, --count=COUNT
                        Records count of cleaning at one time.
```

-d DAYS, --days=DAYS --
    表示要清除DAYS天前的文件

-c COUNT, --count=COUNT --
    用来控制多少条记录一个事务.缺省是5000条.
    
使用此命令,需要对应的Model要定义 `clear_data` 方法,举例如下:

```
    @classmethod
    def clear_data(cls, days, count=5000):
        from datetime import timedelta

        His = get_model('async_tasks_his')

        now = date.now()

        i = 0
        for row in cls.filter(cls.c.status.in_(['C', '1', 'F']), cls.c.created_time<(now-timedelta(days=days))):
            his = His(**row.to_dict())
            his.save(insert=True)
            row.delete()

            i += 1
            if i == count:
                yield i
                i = 0
        yield i
```

clear_data 是一个 classmethod 方法.它接受两个参数:days, count, 分别对应要清理的天数和每次处理的条数.

返回结果可以是一个generator,也可以是一般函数. 每次返回处理的条数.

在调用 clean model 时会自动处理事务,所以在clear_data中不需要处理事务.