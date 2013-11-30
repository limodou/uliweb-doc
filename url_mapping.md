# URL映射

Uliweb使用Werkzeug的Routing来进行URL的处理。当你使用manage.py的makeapp命令生成一个新
的App时，它会自动生成views.py文件，其中会自动从uliweb.core.SimpleFrame中导出expose
函数，它是一个decorator函数，用于修饰view函数。

通过expose可以将一个URL与一个view函数进行绑定，然后通过url_for(这是SimpleFrame提供的用
于反向生成URL的方法)来生成反向的URL。


## expose说明

目前，Uliweb取消了集中的URL配置，因此你需要在每个view方法前加上expose()来定义URL。
但同时，Uliweb还允许你将URL定义在settings.ini，以方便实现URL的替換。

Uliweb目前提供两种View函数的写法，一种是简单的函数方式，另一种是类方式的定义，下
面分别进行描述。


### 普通View函数的处理

基本用法为：


1. 缺省映射

    ```
    @expose()
    def index(arg1, arg2):
        return {}
    
    @expose
    def index(arg1, arg2):
        return {}
    ```

    当expose()不带任何参数(也可以不带括号)时，将进行缺省的映射。即URL将为:

    ```
    /appname/view_function_name/<arg1>/<arg2>
    ```

    如果view函数没有参数，则为：

    ```
    /appname/view_function_name
    ```

1. 固定映射

    ```
    @expose('/index')
    def index():
        return {}
    ```
    
1. 参数处理

    当URL只有可变内容，可以配置为参数。一个参数的基本形式为：

    ```
    <convertor(arguments):name>
    ```

    其中convertor和arguments是可以缺省的。convertor类型目前可以设置为：int, float,
    any, string, unicode, path等。不同的convertor需要不同的参数。详情请参见
    下面的converter说明。最简单的形式就是 `<name>` 了，它将匹配/到/间的内容。
    name为匹配后参数的名字，它需要与绑定的view方法中的参数名相匹配。
    
1. 其它参数

    expose函数允许在义时除了给出URL字符串以外再提供其它的参数，比如：
    
    defaults --
        它用来定义针对view函数中的参数的缺省值，例如你可以定义:
    
        ```
        @expose('/all', defaults={'page': 1})
        @expose('/all/<int:page>')
        def show(page):
            return {}
        ```
    
        这样两个URL都指向相同的view函数，但由于show方法需要一个page参数，所以对于第一
        个/all来说，需要定义一个缺省值。
    
    build_only --
        如果设置为True，将只用来生成URL，不用于匹配。目前Uliweb提供了静态文件的处理，
        但一旦你想通过象Apache这样的web server来提供服务的话，就不再需要Uliweb的静态
        文件服务了。但是有些文件的链接却是依赖于这个定义来反向生成的，因此为了不进行匹配，
        可以加上这个参数，这样在访问时不会进行匹配，但是在反向生成URL时还可以使用。
    
    methods --
        HTTP请求可以分为GET, POST等方法，使用methods可以用来指定要匹配的方法。比
        如:
    
        ```
        @expose('/all', methods=['GET'])
        ```
    
    关于参数更多的说明请参见werkzeug下的routing.py程序。
    

### 类View函数的处理

详细的文档参见 [视图(View)](views.html)


### 在settings.ini中定义URL

Uliweb也支持将URL定义到settings.ini，其主要目的是为了允许别人替換。比如已经开
发了一个app，有一些常用的URL的定义。但是希望别人可以替換已经定义好的URL，如果
直接写到views中，则不会进行替換，只会添加。所以放到settings.ini中就可以方便替
換了。定义示例如下:


```
[EXPOSES]
login = '/login', 'plugs.user.views.login'
logout = '/logout', 'uliweb.contrib.auth.views.logout'
register = '/register', 'uliweb.contrib.auth.views.register'
```

Key是URL的名字，值一般是二元或三元的tuple。形式为:


```
(url_pattern, view_function_path[, kwargs])
```

第一个为url模式，第二个为url对应的view函数的路径，第三个是可选的，应该是一个字典，
它是将传入expose中的参数。


### GET和POST

为了方便处理expose(methods=['GET', 'POST'])这样的URL，uliweb还定义了GET和POST，
分别用于处理GET和POST方法，其它的象DELETE要象上面这样定义。


### 与decorator联用时的注意事项

有时我们希望通过使用decorator来修饰view方法，包括类的view方法。那么由于expose
本身也是一个decorator，并且当函数有参数时，在expose不传入参数时，将自动对函数
的参数进行解析，而decorator的处理方式，有可能会造成新生成的方法与原始的方法参
数不同，会使得生成的URL出现问题。因此对于普通的view函数，建议将expose放在最下
面，以保证expose先执行。而在使用类view方法时，对于只有self参数的简单方法，可以
只加decorator，并且使用自动URL的处理。但对于带有除self之外的其它的参数，使用自
动URL处理可能会出现问题，因此建议添加expose的修饰，并且放在其它的decorator之上，
如:


```
@expose('/myview')
class MyView(object):
    @_other
    def test1(self):
        #这个可以

    @_other
    def test2(self, id):
        #这样可能有问题，因为_other有可能创建新的函数，造成与test2的
        #参数不同

    @expose('test3/<id>')
    @_other
    def test3(self, id):
        #正确，添加显示的expose调用，并且使用相对URL的定义，以便和
        #缺省URL的处理一致

    @_other
    @expose('test3/<id>')
    def test3(self, id):
        #可能不正确
```


## App URL 前缀定义

当我们写好一个APP时我们可能预先假定了它应该使用的URL前缀，如 `/app` ，但是当
别人在使用时，可能并不希望使用 `/app` 的前缀，而是想使用其它的。因此 Uliweb
提供了一种App前缀的配置机制，可以在 `settings.ini` 中定义如下内容:


```
[URL]
appname = '/app_prefix'
```

`[URL]` 用来存放所有需要重定义 appname 前缀的section。每项的内容：key是App的名字，
value是App的前缀。

一旦我们定义了这个前缀，那么在这个App下的所有URL都将加上对应的前缀。


{% alert class=info %}
如果某些链接的确不想添加这个前缀该如何处理，那么只要在 `@expose('/url')` 中添
加一个 `!` 号即可取消前缀的处理，如:  `@expose('!/url')`

{% endalert %}

## url_for说明

url_for可以根据view方法的名字来反向生成URL。要注意，它需要一个字符串形式的view方法名，
格式为:


```
url_for('appname.views_module_name.function_name', **kwargs)
```

其中kwargs是与view方法中的参数相对应的。例如你在Hello中定义了如下URL:


```
@expose('/index')
def index():
    pass
```

然后在反向生成URL时可以使用:


```
url_for('Hello.views.index') #结果为'/index'
```

如果你在运行时希望可以动态适应App名字的变化，可以使用:


```
url_for('%s.views.index' % request.appname)
```

其中request是请求对象，它有一个appname的属性表示访问的App的名字。


{% alert class=info %}
目前在views方法和template中都是可以直接使用这个函数的，不需要导入。

{% endalert %}

## convertor说明


int --
    基本形式为：

    ```
    <int:name>                      #简单形式
    <int(fixed_digits=4):name>      #带参数形式
    ```

    支持参数有：

    * fixed_digits 固定长度
    * min 最小值
    * max 最大值

float --
    基本形式为：

    ```
    <float:name>                    #简单形式
    <float(min=0.01):name>          #带参数形式
    ```

    支持参数有：

    * min 最小值
    * max 最大值

string 和 unicode --
    这两个其实是一样的。
    基本形式为：

    ```
    <string:name>
    <unicode(length=2):name>
    ```

    支持的参数有：

    * minlength 最小长度
    * maxlength 最大长度
    * length 定长

path --
    与string和unicode类型，但是没有任何参数。就是匹配从第一个不是 `/` 的字符到跟着的字
    符串或末尾之间的内容。基本形式为：

    ```
    <path:name>
    ```

    举例：

    ```
    '/static/<path:filename>'
    ```

    可以匹配：

    ```
    '/static/a.css'         -> filename='a.css'
    '/static/css/a.css'     -> filename='css/a.css'
    '/static/image/a.gif'   -> filename='image/a.gif'
    ```

any --
    基本形式为：

    ```
    <any(about, help, imprint, u"class"):name>
    ```

    将匹配任何一个字符串。

