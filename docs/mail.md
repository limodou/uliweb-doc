# Mail 处理

Uliweb中内置了邮件处理，目前支持普通的smtp和gmail的发送模式。如果有特殊要求也
可以自定义邮件发送的后端处理。


## 配置

在settings.ini添加 'uliweb.contrib.mail' app。

同时有以下几项缺省设置:


```
[MAIL]
HOST = 'localhost'
PORT = 25
USER = ''
PASSWORD = ''
BACKEND = 'uliweb.mail.backends.smtp'
SENDMAIL_LOCATION = '/usr/sbin/sendmail'
```

前四项不用过多解释，最后一项是指示使用哪个发送后端。Uliweb已经内置了三个后端，分
别为： smtp, gmail, sendfile。缺省为smtp方式。

使用不同的后端，需要修改 `BACKEND` 为不同的类名，分别为： `uliweb.mail.backends.smtp`,
`uliweb.mail.backends.gmail`, `uliweb.mail.backends.sendfile` 。这种方式允许你
编写自已的后端。

### 无验证模式

保持USER, PASSWORD为空，BACKEND为smtp，这种情况下将不进行验证。如:


```
[MAIL]
HOST = 'localhost'
PORT = 25
```


### 用户验证模式

填写USER, PASSWORD内容，BACKEND为smtp，这种情况下将进行用户验证处理。如:


```
[MAIL]
HOST = 'localhost'
PORT = 25
USER = 'user'
PASSWORD = 'password'
```


### Gmail模式

Gmail有自已特殊的方式，并且它的主机和端口都是特殊的，因此，保持HOST为''，PORT为0，
同时填写USER和PASSWORD，BACKEND改为'uliweb.mail.backends.gmail'。如:


```
[MAIL]
HOST = ''
PORT = 0
USER = 'user'
PASSWORD = 'password'
BACKEND = 'uliweb.mail.backends.gmail'
```

### Sendmail模式

sendmail模式将使用机器上自动的sendmail程序来发送。这是通过命令行来执行的。所以
要保证你的机器上安装有 sendmail 服务. 缺省sendmail的路径是 `/usr/sbin/sendmail`。
使用sendmail来发送邮件，将不需要用户名和口令。不过这种方式很有可能会被收信人判
断为垃圾邮件。

## 邮件发送

配置好之后就是邮件发送处理。举例如下:


```
def mail():
    from uliweb.mail import Mail

    Mail().send_mail('limodou@gmail.com', 'limodou@gmail.com',
        u'中文标题', u'中文内容')
    return 'ok'
```

首先是要创建Mail的实例，然后调用send_mail来发送邮件。

其中，如果Mail()没有传入参数时，将自动使用settings中的配置信息。你也可以直接传
入象:host, port, user, password, backend等参数。

send_mail的原型为:


```
send_mail(from_, to_, subject, message, html=False, attachments=None)
```


* `from_` 为发信人
* `to_` 为收信人
* `subject` 为主题
* `message` 为内容
* `html` 标识是否为HTML内容。如果为True，则message应为HTML片段
* `attachments` 为附件，它是一个tuple或list。

如果主题或内容有中文，建议使用unicode或utf-8编码。


{% alert class=info %}
如果同时有多个收信人时，to_可以为以','号分隔的邮件列表，也可以是一个list。如:
mailto:'abc@com,bcd@com'或[mailto:'abc@com', mailto:'bcd@com']。

{% endalert %}

## 本机测试

如果你没有环境怎么办，Python提供了这样的方法，在本机命令行执行:


```
python -m smtpd -n -c DebuggingServer localhost:1025
```

这样就启动了一个测试用的smtp服务器，将settings.ini中的HOST和PORT修改成：
localhost和1025就可以在命令行下看到发送的文本了。不过要看效果的话可能还是要真正
给自已发个邮件才行。

再有就是，如果你可以直接Internet，可以使用上面的gmail的配置来测试。

