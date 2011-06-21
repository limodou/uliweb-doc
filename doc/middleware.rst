====================================
Middleware 开发
====================================

Uliweb中的Middleware是类似于django的Middleware，它可以在交易处理前和处理后，以
及出错时执行Middleware中的方法，起到一种通用的中间件的作用。Middleware是基于请
求的，它和平时的wsgi middleware不同，wsgi middleware是基于应用级的，当然也可以
处理请求，但是比Middleware还要底层，本文就不讨论了。

介绍
------

先以contrib.auth.middle_auth的AuthMiddle为例::

    from uliweb.middleware import Middleware

    class AuthMiddle(Middleware):
        ORDER = 100
        
        def process_request(self, request):
            from uliweb.contrib.auth import get_user
            request.user = get_user(request)

一个Middleware要从``Middleware``类派生。一般只需要定义三个方法::

    process_request(request)
    process_response(request, response)
    process_exception(request, exception)

不同的Middleware可以根据需要分别定义不同的方法。

Middleware基类有一个缺省的``__init__``方法，如::

    def __init__(self, application, settings):
        self.application = application
        self.settings = settings

你也可以自已定义一个，以便进行初始化的处理。

执行顺序
----------

从上面的示例中，可以看到AuthMiddle中定义了一个``ORDER``的属性。Uliweb在调用
middlware时会根据``ORDER``的值先对Middleware进行排序，然后再根据顺序进行依次
调用。这里的顺序只是缺省的顺序，在用户进行配置时还可以进行修改。详见下面的配
置说明。

调用逻辑
----------

下面列出执行的伪代码进行说明::

    #排序
    middlewares.sort()
    
    #执行Middleware，执行process_request
    for m in middlewares:
        if hasattr(m, 'process_request'):
            res = m.process_request(request)
            if res is not None:
                return res
            
    #调用view方法
    try:
        res = call_view()
    except Exception, e:
        for m in reversed(middlewares):
            if hasattr(m, 'process_exception'):
                res = m.process_exception(request, e)
                if res is not None:
                    break
        #继续抛出异常
        raise
    
    #执行Middleware, 执行process_response
    for m in reversed(middlewares):
        if hasattr(m, 'process_response'):
            res = m.process_response(request, res)
            
#. 先是对Middleware进行排序。
#. 对所有的Middleware中的process_request进行处理。如果有返回值不是None，则跳出
   循环。这里会对Middleware中是否有process_reqeust方法进行判断。后面类似。
#. 然后是执行view方法，获得response。在执行中，如果出错，则按倒序对Middleware
   进行处理。如果某个process_exception有返回值，则跳出循环。最后通过raise再次抛
   出异常，让整个应用捕获。
#. 如果没有异常，则按倒序执行Middleware中的process_response方法。这里和process_request
   不同。你需要强制返回response对象，因为它会传递到下一个处理方法中。

配置
==========

有两个地方可以配置：apps/settings.ini和某个应用下的settings.ini。

Uliweb缺省定义了一个::

    GLOBAL
    MIDDLEWARE_CLASSES = []

所以，不管你把MIDDLEWARE_CLASSES定义在哪里，都会由Uliweb自动将所有定义在不同的
settings.ini文件中的MIDDLEWARE_CLASSES汇总到一起。这个功能是由Uliweb中的ini功能
提供的。比如前面的AuthMiddle就是在uliweb/contrib/auth/settings.ini中有定义:

    [GLOBAL]
    MIDDLEWARE_CLASSES = [
        'uliweb.contrib.auth.middle_auth.AuthMiddle',
    ]

因此，你自已的应用如果要配置Middleware，可以自行考虑要放到哪级的settings.ini中。

那么你可能要问，当所有的MIDDLEWARE_CLASSES汇总成一个list时，顺序如何确定？

在前面伪代码中，有一个对Middleware进行排序的处理。它会根据Middleware中的ORDER来
排序，这是缺省的。如果你的settings.ini在定义时加上了顺序值，例如::

    [GLOBAL]
    MIDDLEWARE_CLASSES = [
       (200,  'uliweb.contrib.auth.middle_auth.AuthMiddle'),
    ]

它就会按200的顺序值进行排序。

Uliweb中的app有些已经提供了MIDDLEWARE_CLASSES，它们只要你在INSTALLED_APPS中包含
app即可。因为在它们的settings.ini中已经写好了MIDDLEWARE_CLASSES的配置，因此不再
需要重新定义，并且顺序也考虑好了。

因此当你自已写了Middleware或特殊情况下，才需要重新定义顺序。

在Contrib中定义的Midddleware
------------------------------

下面列出在contrib中定义的一些Middleware供参考:

* 'uliweb.contrib.auth.middle_auth.AuthMiddle' ORDER=100 app='auth'
  用于在请求进来时，向request添加一个user的对象。这样用户就可以直接通过request.user
  来判断用户是否已经登录和得到登录用户对象。
* 'uliweb.i18n.middle_i18n.I18nMiddle' ORDER=500 app='i18n'
  用于i18n的处理，设置语言类型
* 'uliweb.contrib.session.middle_session.SessionMiddle' ORDER=50 app='session'
  请求进来时自动读取session。请求结束时自动保存cookie。

所以，当你使用了上面三个app时，它会自动按::

    'uliweb.contrib.session.middle_session.SessionMiddle'
    'uliweb.contrib.auth.middle_auth.AuthMiddle'
    'uliweb.i18n.middle_i18n.I18nMiddle'
    
的顺序来执行。