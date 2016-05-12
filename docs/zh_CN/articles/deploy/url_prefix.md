# 站点的url前缀配置例子

local_settings.ini例子:

```
[DOMAINS]
default = {'url_prefix': '/myprefix', 'domain': '', 'display': False}
static = {'url_prefix': '/myprefix', 'domain': '', 'display': False}
```

这样就可以对所有views及静态文件的url加上前缀,原来 http://mysite/test 会变成 http://mysite/myprefix/test

同时web服务器的配置也需要加上前缀,以 nginx 为例:

```
server {
    listen 80;
    server_name example.com;
    location /myprefix/ {
        proxy_pass http://localhost:8000/myprefix/;
        ...
    }
}
```

最后还有一个如果需要加 url prefix ,那么代码(python/html/javascript)里不能把 url 写死,应该用 [url_for](http://limodou.github.io/uliweb-doc/zh_CN/url_mapping.html#title_1-3) 或者 [url_for_static](http://limodou.github.io/uliweb-doc/zh_CN/app_staticfiles.html#title_1-1),比如在html里可以这么用url_for:

```
{{=url_for('Test.views.index')}}
```
