# timezone(时区支持)
## 依赖的Python包
经过比较采用Pendulum,理由: 

* [比Arrow接口更合理](https://github.com/sdispater/pendulum#why-not-arrow)
* [比pytz性能更好](https://pendulum.eustace.io/blog/a-faster-alternative-to-pyz.html)
* [更活跃](https://python.libhunt.com/compare-pytz-vs-pendulum)
## settings
settings.GLOBAL.TIME_ZONE

* 意义: 服务端时区配置
* 值:
    1. 默认为None,**None表示不开启时区功能**
    2. 时区可取值可用pendulum.timezones,具体可见pytzdata里的 [这个列表](https://github.com/sdispater/pytzdata/blob/master/pytzdata/_timezones.py)

settings.GLOBAL.LOCAL_TIME_ZONE

* 意义: 客户端的默认时区配置
* 可取值为pendulum.timezones
## contrib.timezone.startup_installed
这里新增一个改变环境变量的步骤,类似于 [django里的做法](https://juejin.im/post/5848b301128fe1006907d5ed),例如: os.environ['TZ'] = 'UTC', 目的是直接影响 datetime/time这些标准库的返回值,会返回和settings.GLOBAL.TIME_ZONE符合的时间

## user表
增加 timezone 字段,可取值为pendulum.timezones,可以参考 [django-easytz里的实现](https://github.com/jamesmfriedman/django-easytz/blob/master/easytz/models.py#L30)

## TimezoneMiddleware
参考[django里有人采用的做法](https://www.calazan.com/adding-a-time-zone-setting-to-your-django-app/)或者[django-easytz里的实现](https://github.com/jamesmfriedman/django-easytz/blob/master/easytz/middleware.py),使用一个middleware,如果TIME_ZONE开启,那么通过处理user.timezone(或者匿名用户可以从cookie获取,cookie key为'timezone',可以通过settings更改)获取时区设置,然后(这里做法和django不一样)将时区保存在 **request.tz **里,供其他地方使用

| request.tz   | 时区(字符串)   | 
|:----|:----|
| request.tzinfo   | 时区信息(tzinfo object),使用 pendulum.timezone(request.tz) 得到   | 

##  获取客户端时区的逻辑
* 优先从request.tzinfo里读取
* 否则尝试从cookie里读取 ( key 为 settings.TIMEZONE.cookie_key )
* 否则使用 settings.GLOBAL.LOCAL_TIME_ZONE
* 如果settings.GLOBAL.TIME_ZONE!=None,但是settings.GLOBAL.LOCAL_TIME_ZONE=None,那么会把默认的local timezone值当成和TIME_ZONE一致
## 时区打开与否的差别
| 模块   | settings.GLOBAL.TIME_ZONE = None  (即关闭时区功能情况下)   | settings.GLOBAL.TIME_ZONE != None  (即开启时区功能情况下)   | 
|:----|:----|:----|:----:|
| uliorm   | DateTime: 只接受naive datetime,如果传递了一个带时区信息的datetime会报错(参考[django做法](https://juejin.im/post/5848b301128fe1006907d5ed))   | DateTime: 保存datetime的时候会将所有的时间都转为UTC时间,如果是不带时区的naive datetime,那么会打印一个warning,并视为TIME_ZONE 这个时区的时间来转换  增加functions.**to_ltimezone**()提供根据request.tzinfo转换成客户端本地时间 | 
|    | DateTimeProperty存取的时候不会处理时区   | 在形成object的时候会将时间数据转成用户本地时区( DateTimeProperty._convert_func() )  在保存到数据库之前会将时间数据转成UTC时间( Model.save() )   | 

## 相关链接
1. [Django time zone文档](https://docs.djangoproject.com/en/2.1/topics/i18n/timezones/)
2. [django-easytz](https://github.com/jamesmfriedman/django-easytz)
