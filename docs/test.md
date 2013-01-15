# 如何测试

根据测试的要求，我们可以将其分为：函数测试，web测试。其中，函数测试大多数情况
下可以使用象doctest的技术来实现，这里不描述了。主要讲web测试。web测试一般需要
一个环境，如web server。然后通过在客户端录制脚本来摸拟页面操作，再比较返回的
内容。因为uliweb底层使用werkzeug模块，它提供了 werkzeug.test 功能，所以你可以
使用它来进行测试。它可以摸拟web server的工作方式，通过程序的方式发出get, post
请求，还可以自动处理cookie和redirect，所以使用很方便。

为了简化在uliweb中的使用，uliweb.utils.test中提供了client的函数，它将返回一个
Client对象。关于如何使用werkzeug进行测试的文档请参见werkzeug的 [文档](http://werkzeug.pocoo.org/docs/test/) 。

示例如下:


```
from uliweb.utils.test import client

c = client('..')
r = c.post('/login', data={'username':'username', 'password':'password'}, follow_redirects=True)
r = c.get('/')
print r.data
```

上面的代码摸拟用户登录的例子。

client接受一个project_path的参数，它是你的uliweb项目的目录，其下应该有apps子目录。
它会自动创建app。c.get()和c.post()分别对应GET和POST的HTTP的请求，返回值为Response
对象。

