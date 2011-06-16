====================================
XMLRPC 使用说明
====================================

Uliweb通过uliweb.contrib.xmlrpc这个app来提供XMLRPC的访问需求。通过此文来讲解XMLRPC
在Uliweb中如何使用。

    
配置
----------

向$project/apps/settings.ini中的INSTALLED_APPS中添加'uliweb.contrib.xmlrpc'。

配置完毕后，你的应用就已经有一个/XMLRPC的url可以使用了。比如可以通过:: 

    http://localhost:8000/XMLRPC

来访问XMLRPC服务。如果你想要修改这个URL，可以在settings.ini中添加::

    [EXPOSES]
    /XMLRPC = 'uliweb.contrib.xmlrpc.views.xmlrpc'
    
在uliweb.contrib.xmlrpc的settings.ini中已经定义上述内容。

使用
---------

下面我使用一个示例的方式来展示如何使用xmlrpc。

先让我们创建一个xmlrpc_test的项目和一个Hello的app，操作如下::

    uliweb makeproject xmlrpc_test
    cd xmlrpc_test
    uliweb makeapp Hello
    
修改settings.ini添加uliweb.contrib.xmlrpc::

    [GLOBAL]
    DEBUG = True
    
    INSTALLED_APPS = [
    #    'uliweb.contrib.staticfiles',
        'uliweb.contrib.xmlrpc',
        'Hello',
        ]
    
然后修改Hello/views.py，修改的内容如下::

    #coding=utf-8
    from uliweb import function
    xmlrpc = function('xmlrpc')
    
    @xmlrpc
    def hello():
        return 'hello'
        
    @xmlrpc('func')
    def new_func():
        return 'new_func'
        
    @xmlrpc
    class Hello(object):
        def test(self, name):
            return {'user':name}
            
        @xmlrpc('name')
        def new_name(self):
            return 'new_name' 

说明如下:

#. xmlrpc提供了一个同名的decorator函数，可以用来修饰普通的函数和类，以便将其转
   为XMLRPC的服务。而这个decorator是定义在xmlrpc的settings.ini中的，例如::

        [FUNCTIONS]
        xmlrpc = 'uliweb.contrib.xmlrpc.xmlrpc'

   为了获取真正的函数对象，uliweb提供了一个内部函数叫function。使用它就可以从
   settings.ini的FUNCTIONS中获取一个形如'module.function'的函数对象。
#. xmlrpc可以支持函数和类。函数和类本身没有特别要求。对于类，一般不定义__init__
   方法，如果有，也需要可以支持不带参数的调用。因为在调用类方法时，xmlrpc会自
   动创建类。
#. xmlrpc可以支持带参数或不带参数。不带参数则会直接使用函数名作为将来调用的函数
   名。如果是类，则形式为ClassName.MethodName的形式。如果带参数，则这个参数将作
   为被调用的函数名，而不是原来的函数名了。所以上面的@xmlrpc('func')就是给所修        
   饰的函数重新起了一个名字，客户端应该使用func来访问，而不是new_func。
#. 如果类函数是以'_'开头的，将不会被调用。
#. 在类方法上仍然可以使用xmlrpc，这样相当于创建了一个xmlrpc函数的别名。
#. Uliweb提供的xmlrpc调用还支持与views相类似的__begin__和__end__的处理。同时可
   以在类上使用。有兴趣的可以自行测试。

测试
----------

下面创建一个测试程序，如test_xmlrpc.py::

    #coding=utf-8
    from xmlrpclib import ServerProxy
    
    server = ServerProxy("http://localhost:8000/XMLRPC")
    
    print server.hello()
    print server.func()
    print server.Hello.test('limodou')

可以看到，如果是类的方式，可以使用 ``server.Hello.test('limodou')`` 很方便。

如果执行正确，运行结果为::

    hello
    new_func
    {'user': 'limodou'}

    