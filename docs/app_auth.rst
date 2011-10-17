=====================
auth(用户认证处理)
=====================

在Uliweb中提供了一个auth的app，它是专门用来进行用户认证的。一般来说，用户认证功能可以理解为:登录、注册、注销、用户识别。

登录
    指用户由未登录状态，通过输入用户名、口令进入登录状态。
注册
    指在系统中创建新用户的过程。
注销
    用户取消注册状态的过程。
用户识别
    用户在登录后，在访问页面时，识别用户信息的过程。
    
上面只是一般的用户认证相关的内容，更复杂一些的内容，例如：

记住我
    可以保留用户登录状态一段时间，比如一个月或一年等。
其它认证方式
    如采用open_id认证方式，使用其它网站的认证api等。
    
用户认证的原理说明
--------------------

我们知道HTTP是无状态的处理，所以为了在不同的请求中维护用户会话(session)的状态人们想出了多种办法，比如常见的session的处理。常见的session的处理基本上有两种方式：

#. 基于cookie的session处理方式
   这种方式也是uliweb目前采用的方式。它首先在后台生成一个session对象，每个session对象有唯一的session_id。通过session_id可以找到对应的session对象。然后将用户的id保存到session对象中。而session_id则保存到cookie中。这样，利用session本身的机制，在用户访问页面时，首先识别出session信息，如果有，则再查找有没有用户id信息，然后取出用户对象并绑定到request.user属性上，供后续的处理来使用。如果session对象没找到或没有用户id的信息，则认为用户没有登录过，并绑定request.user为None。所以，这种方式，在前端只保留session_id的信息，利用session对象来处理用户登录的状态。而且用户登录的有效期是与session一致的。

#. 基于页面间传递session_id的值的方式
   这种也有人用，但uliweb没有采用这种方式。它的原理是不使用cookie，而是在页面中保持一个session_id，页面间传递时都带着这个值，比如通过URL则放到QueryString中，通过POST则放到post数据中。这种不依赖cookie，但是使用起来相对麻烦。

整个认证及会话处理过程是这样的：

* 用户输入登录信息
* Uliweb在后台检查用户和口令，如果通过，则在session中保存用户id，如果不通过，则报错
* 在访问非登录页面时，根据session中的用户id信息获取用户对象，并绑定到request.user上
* 其它页面可以根据request.user为None或非None的值来知道当前访问的是登录用户还是匿名用户

用户注销的过程比较简单，只要将session中的用户id删除即可。

auth app的使用
----------------

Uliweb中提供了auth app来进行用户识别、登录、注销甚至注册的功能。它提供了以下功能:

* 一张用户表(User)，其中还提供了：
    * set_password 设置口令
    * check_password 检查口令
    * get_default_image_url 获得用户缺省的头像URL方法
    * get_image_url 获得用户头像URL方法
* check_password方法 检查两个口令是否一样的方法
* 提供了几个Form类：
    * RegisterForm 注册Form
    * LoginForm 登录Form
    * ChangePasswordForm 修改口令Form
* 一个Middleware 用于用户识别
* 若干方法：
    * get_user 根据request对象来获得用户对象
    * create_user 创建用户
    * authenticate 用户认证
    * login 用户登录
    * logout 用户注销
    * require_login decorator，用于检查用户是否登录，如果没登录则跳转到相应的URL上，缺省为 `'/login'` 。而且require_login既是一个decorator也是一个普通函数，主要看第一个参数是否为function对象。
    * has_login 和require_login类似，但不是decorator
* 缺省view方法：
    * login 用来处理用户登录，会显示登录界面和进行用户输入登录信息后的处理
    * register 用来处理用户注册，会显示用户注册界面和进行用户输入注册信息后的处理
    * logout 用户注销处理
* 缺省的templates
    * login.html 用来显示登录界面
    * register.html 用来显示注册界面
* settings.ini配置内容：
    * 提供以下内容::
    
        [EXPOSES]
        login = '/login', 'uliweb.contrib.auth.views.login'
        logout = '/logout', 'uliweb.contrib.auth.views.logout'
        
        [FUNCTIONS]
        require_login = 'uliweb.contrib.auth.require_login'
        
        [DECORATORS]
        require_login = 'uliweb.contrib.auth.require_login'

安装auth
~~~~~~~~~~~~

向apps/settings.ini中的INSTALLED_APPS中添加'uliweb.contrib.auth'。

当安装完毕后，你已经可以使用/login, /logout。但是你需要在首页或某个地方将相应的链接添加进去。同时auth的中间件已经生效，它依赖于session app，用户本身还需要orm的支持。不过这两个app都已经在config.ini中写好了，会自动依赖。

用户创建
~~~~~~~~~~~~~~

有了相应的链接，你需要先创建几个用户。auth本身提供了一个命令，通过::

    uliweb createsuperuser
    
可以创建超级用户。

非超级用户，要么通过添加register相关的功能（如添加/register到页面和在views.py或settings.ini中添加相应的链接）让用户自行创建用户。要么开发相应的用户管理app来管理用户。在plugs中有类似的例子，但是已经超出auth本身的功能了。auth不提供复杂的用户管理的功能，它只是完成基本的用户认证、注销、识别等功能。

判断用户是否登录的方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

auth向settings.ini中注册了require_login的方法和decorator。因此，用户可以通过::

    from uliweb import function
    require_login = function('require_login')
    
    if require_login():
        #do something
        
    #或
    
    from uliweb import functions
    require_login = functions.require_login
    
    if require_login():
        #do something
        
    #或
    
    from uliweb import decorators
    
    @decorators.require_login
    @expose('/user/admin')
    def user_admin():
        #do something
        
来使用require_login，用于判断用户是否已经登录，如果没有登录，在缺省情况下，它会自动使用名为 `login` 的 URL进行跳转，成功后再跳转到原来的URL上。用户可以在settings.ini中覆盖 `login` 的URL定义，也可以直接在require_login上传入 `next=url` 的参数。

auth功能扩展
~~~~~~~~~~~~~~~~~~

auth虽然是一个比较基础的功能，但是在实际使用中可能有非常多的变化形式，比如使用邮箱注册，使用其它的网站进行用户认证等。这些目前还不包含在uliweb中，需要用户自行扩展。但是这里给出扩展的建议：

#. uliweb提供的功能可以作为参考，用户可以基于原auth进行扩展，如：替換template，Forms, Views等
#. auth提供的许多功能都是配置化的，因此用户可以考虑在自已的app中进行部分或全部替換