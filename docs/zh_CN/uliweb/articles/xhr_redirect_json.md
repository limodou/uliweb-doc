# 重定向在异步请求中的处理实现

## 问题描述

在Web请求某个页面时，我们需要判断当前用户是否有访问权限，如果当前用户尚未登录，
一般会跳转到登录页面，在登录页面登录成功之后，再跳回到原来的页面。如果都是普通
请求，跳转没有什么问题，但是如果请求是以ajax方式发送到后台，后台简单的返回重定
向，前端就有可能在当前的div中显示登录窗口，而不是真正跳转到登录页。这个不是我们
想要的结果。

## 处理办法

主要涉及到前后台的配合。

### 后台处理

后台在遇到ajax请求时，不再返回redirect信息，而是返回一个json信息。为了区别于正
常结果，使用了500的返回码。

目前这块在uliweb 0.2版本中已经自动支持。它会根据请求是否为ajax方式来返回普通的
重定向结果，或json结果。返回的json结果为：

```
{'success':False, 'redirect':'xxxxxxx'}
```

响应码为500。

在缺省情况下，这种处理是自动的。如果你不想使用这种机制，则需要在启动代码时，在
创建application实例时传入 `xhr_redirect_json=False` 的参数。如修改wsgi_handler.py
中的：

```
application = make_application(apps_dir=apps_dir)
```

为：

```
application = make_application(apps_dir=apps_dir, dispatcher_kwargs={'xhr_redirect_json':False})
```

### 前台处理

前台可以考虑每个请求都去判断出错的情况。但是因为我主要是使用jquery，所以给出jquery
中更通用的做法。

一般在uliweb项目中，引用jquery时会使用 `{{use "jquery"}}` ，那么它会在生成页面时
查找settings.ini中的 `[UI_CONFIG]` 中是否有 `jquery_bootstrap` 的定义。如果有，
会把settings.ini中的值写到模板中。所以，这个配置就是在引入jquery后，可以由用户
来进行必要的初始化的一个配置。缺省情况下它是：

```
jquery_bootstrap = "<script>$.ajaxSetup({cache:false, traditional:true});</script>"
```

然后我们可以根据需要修改这个配置。

为了方便，我把处理写在一个js文件中，比如叫jsinit.js。然后你可以放在某个app的static
目录下。它的内容是：

```
function updateURLParameter(url, param, paramVal)
{
    var TheAnchor = null;
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";

    if (additionalURL) 
    {
        var tmpAnchor = additionalURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor = tmpAnchor[1];
        if(TheAnchor)
            additionalURL = TheParams;

        tempArray = additionalURL.split("&");

        for (i=0; i<tempArray.length; i++)
        {
            if(tempArray[i].split('=')[0] != param)
            {
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }        
    }
    else
    {
        var tmpAnchor = baseURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor  = tmpAnchor[1];

        if(TheParams)
            baseURL = TheParams;
    }

    if(TheAnchor)
        paramVal += "#" + TheAnchor;

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}

$.ajaxSetup({
    cache:false, 
    traditional:true,
    error:function(jqXHR, textStatus, errorThrown){
        var m = $.parseJSON(jqXHR.responseText);
        if (!m.success && m.redirect){
            var login = /\/login\b/;
            var url = m.redirect;
            //Test if login, then replace next parameter
            if (login.test(m.redirect)){
                url = updateURLParameter(m.redirect, 'next', window.location.href);
            }
            window.location.href = url;
        }
    }
});
```

其中 `updateURLParameter` 是一个函数，它的作用是替換URL中的某个参数。为什么需要
这个？这个和uliweb的机制有关。如果你使用 `uliweb.contrib.auth` 的 `require_login` 
进行登录检查，那么它会在跳转到登录页面时使用：

```
/login?next=/path/to/origin/path
```

因此，当登录成功，可以根据 `next` 的值再跳回原来的地址上。

但是这里存在一个问题。因为这个next的值 **是ajax请求的URL** 。可能你要说，这有什
么关系？问题就是，登录成功，你返回的页面将只是ajax请求处理后的结果，而不是原始
的操作页面。ajax的URL只是这个页面中的某个操作，它并不是原来的访问页面。所以，我
们要获得原始的可访问的页面URL，然后把next替換成这个地址。这样，我们并不是实现了
在登录后，再次执行原始的ajax请求，而是跳到合适的页面，让用户再操作一遍。

了解这个处理很重要，因为跳转多次后，原来的ajax请求有可能根本不能直接运行的，比如
使用了POST发送数据，跳转之后数据已经丢失，再提交也是错误。更何况，跳转的页面不
是希望的HTML的页面，只是某个处理后的结果。

所以我们先定义了一个 `updateURLParameter` 函数用来替換 next 参数。在jquery中没有
直接可用的函数。这个函数是从stackoverflow上找到的。

那么，我们还假设，你使用的是uliweb的require_login的机制，所以才会去替換next值。
不然，你要根据你的应用去考虑如何处理重定向。

这里我们只对登录重定向作了特殊处理，也很难想象还有哪些其它的情况会是ajax请求，但是
后台会重定向。

为了确保是登录URL，我们还对重向定的URL进行了检查，看是否包含 `/login` 这样的串。
如果有，则替換 next 参数。参数值，我们使用了 `window.location.href` 。这里我们
假设了ajax请求没有修改URL，所以得到的URL应该就是还没有进行ajax处理的URL，正是
我们想要跳回来的地址。

我们把上面的处理放在了 `$.ajaxSetup` 这样做为一个缺省的处理。

我们把jsinit.js的引入加到settings.ini中去：

```
[UI_CONFIG]
jquery_bootstrap = """<script src="/static/jqinit.js"></script>"""
```

经过前后台的处理之后，前后的处理基本上是透明的。

因为有许多的假设，所以上述的处理仅供参考。