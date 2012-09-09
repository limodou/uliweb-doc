=============
CSRF
=============

CSRF - Cross-site request forgery(跨站请求伪造)，可以去网上搜索一下它的意思。
它是一种比较危险的攻击手段。现在在 Uliweb 中也提供了对这种攻击的保护机制。此
机制是由Damon根据Django和Tornado的实现，再由我进行相应的修改编写而成。

它实现的主要原理是：

首先在后台生成相应的token，将其保存在session中（有效期缺省是30分钟）。然后在返
回前端时，将token保存在cookie中。这样我们就有了系统级别的token(session和cookie中
的都算)。我们可以认为这两个token都是安全的。

然后对于可能修改数据的交互，如Form的POST提交，ajax的POST提交，我们要求上传的数据
都要带上这个token，所以这个就是由应用来完成的。这样我们又得到了一个应用级别的
token。

然后将请求发送到后端时，我们比较系统的token和应用的token是否一致，如果不一致则
报错。

可能你认为，这两个本就就一致，这样比较有什么意思呢？因为根据CSRF的攻击原理，攻
击者是在无法直接操作受害者机器的情况下来引导受害者访问一个正常的URL来进行攻击的。
由于cookie总是会上传到服务器，所以如果只检查cookie，将无法识别是否受到攻击。但
是如果在应用上増加token的信息，而攻击者是无法直接拿到这个token的，所以提交的数据
将无法带有正确的token，从而造成校验失败。

所以本CSRF App的目的就是构造系统和应用级别的token处理，然后在后台进行比较。

保护范围
-----------

根据Django的代码，我们可以看出，一般的CSRF的保护都是对后台数据有修改的请求，如：
POST，DELETE等。但是有些操作是通过GET方式来修改的，因此，如果在URL中带有token的
信息也将进行校验处理。

使用说明
-----------

使用csrf app，首先要在 ``settings.ini`` 中安装 ``uliweb.contrib.csrf`` app.

安装好 csrf app后，相应的Middleware会自动生效。它将会依赖 ``uliweb.contrib.session``
App，不过，在csrf中已经设置好了相关的依赖，所以你不需要显示地安装 session app。

整个csrf的处理过程是比较自动化的，和其它的csrf和实现可能不太一样。

一般的页面流程是：

* GET 一个页面，在页面中显示表格或内容，此时应生成token
* POST 数据，检查token是否正确

以上的处理主要是通过Middleware的机制完成的::

    def process_request(self, request):
        # process each request
        if self.settings.get_var('CSRF/enable', False):
            if request.method in ('POST', 'DELETE') or (request.method == 'GET' and request.GET.get(self.settings.CSRF.form_token_name)):
                functions.check_csrf_token()
    
    def process_response(self, request, response):
        if not self.settings.get_var('CSRF/enable', False):
            return response
        
        token = functions.csrf_token() #创建token
    
        #保存token到cookie中
        response.set_cookie(self.settings.CSRF.cookie_token_name, token, max_age=self.settings.CSRF.timeout)
    
        #如果用户设置了csrf_pass，则跳过csrf的处理
        if getattr(response, 'csrf_pass', False):
            return response
    
        #处理返回的内容中包含有 Form 内容时自动添加token输入
        if response.headers['Content-Type'].split(';')[0] in _HTML_TYPES:
    
            def add_csrf_field(match):
                """Returns the matched <form> tag plus the added <input> element"""
    
                return (match.group() + 
                    '\n<input type="hidden" name="%s" value="%s">' % (self.settings.CSRF.form_token_name, functions.csrf_token()))
    
            # Modify any POST forms
            response.data = _POST_FORM_RE.sub(add_csrf_field, response.data)
    
        return response
    
通过Middleware把相应的页面流进行了处理。有几点要说明：

#. csrf可以通过 ``'CSRF/enable'`` 来设置是否启用，缺省为启用
#. 对于请求方法为POST或DELETE的进行校验，同时对于GET方法，同时上传的数据中包含有
   token信息的也进行校验
#. 在应答时创建token，如果token已经创建，则等到超时时间到达时，创建新的token。缺
   省的token生存期是30分钟
#. 通过设置 ``response.csrf_pass`` 可以跳过对响应报文中token串的自动处理
#. 当返回的内存类型为 ``text/html`` 和 ``application/xhtml+xml`` 的自动扫描是否
   存在 Form 元素，如果有，自动添加 ``<input type="hidden" name="csrf_token" value=token>`` 的信息。
   这样对于存在Form场景是非常自动化的。如果不喜欢这种方式，完成可以写一个新的Middleware
   来进行替換。

让我们对不同的使用场景来进行描述。

Form
~~~~~~~~~

如果你采用Form来交互，其实在安装好 csrf App 之后不需要做特殊的处理，token的生
成，插入到Form中，token的校验都由Middleware完成了。你需要注意的是Form的method
一定要是 POST。

Ajax
~~~~~~~~~

Ajax比较特殊，它一般不用 Form ，直接通过ajax请求向后端发送数据。这里参考了django
针对jquery写的一个javascript片段，你需要在使用时将其 include 到你的模板中。例如::

    {{include "inc_jquery_csrf.html"}}
    
这个片段完全参考了Django的代码，除了cookie的token名是改为配置化的。它的主要作用是
先判断请求的类型，如果是修改类的，如:POST或DELETE则会将token从cookie中取出，然后插
入到http的头中，这一点和Form的方式不同。Form是作为数据提交的。

GET方法
~~~~~~~~~~~

前面主要是针对修改数据的操作，但是有时ajax的操作就是通过GET来完成的。所以我们
可以在相应的URL上包含token信息，这样Middleware一样会进行校验。例如::

    <a href="/remove/{{=object.id}}?csrf_token={{=functions.get_token()}}">remove</a>
    
配置说明
------------

::

    [MIDDLEWARES]
    csrf = 'uliweb.contrib.csrf.middleware.CSRFMiddleware', 150
    
    [CSRF]
    enable = True
    timeout = 30*60 #seconds
    form_token_name = 'csrf_token'
    cookie_token_name = '_csrf_token'
    
    [FUNCTIONS]
    csrf_token = 'uliweb.contrib.csrf.csrf_token'
    check_csrf_token = 'uliweb.contrib.csrf.check_csrf_token'

csrf提供以下配置:

* csrf 中间件
* 基本配置

  * ``enable`` 用来控制csrf机制是否生效
  * ``timeout`` 用来控制session中保存的token的生存期，缺省为30分钟
  * ``form_token_name`` 用来设置定义在Form中的隐藏字段名，缺省为 ``csrf_token``
  * ``cookie_token_name`` 用来设置cookie的token名，缺省为 ``_csrf_token``

* 公共函数

  * ``csrf_token`` 用来生成一个token，并保存到session中
  * ``check_csrf_token`` 用来校验一个token是否正确

其实使用 ``csrf_token`` 和 ``check_csrf_token`` 再结合相应的cookie及应用的集成也可以
实现其它的csrf的处理模式。
