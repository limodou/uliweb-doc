=============
部署指南
=============

Apache
---------

mod_wsgi
~~~~~~~~~~~

#. 按 `mod_wsgi <http://code.google.com/p/modwsgi/>`_ 的说明安装mod_wsgi到apache下。

   * 拷贝mod_wsgi.so到apache的modules目录下

   Window环境可以看：

    http://code.google.com/p/modwsgi/wiki/InstallationOnWindows

   Linux环境可以看：

    http://code.google.com/p/modwsgi/wiki/InstallationOnLinux


#. 配置 apache 的httpd.conf文件

   * 增加：

     ::
    
        LoadModule wsgi_module modules/mod_wsgi.so
        WSGIScriptAlias / /path/to/uliweb/wsgi_handler.wsgi
        
        <Directory /path/to/youruliwebproject>
        Order deny,allow
        Allow from all
        </Directory>
        
     上面是将起始的URL设为/，你可以根据需要换为其它的起始URL，如/myproj。
    
     如果在windows下，示例为：
    
     ::
     
        WSGIScriptAlias / d:/project/svn/uliweb/wsgi_handler.wsgi
        
        <Directory d:/project/svn/uliweb>
        Order deny,allow
        Allow from all
        </Directory>

#. 重启apache
#. 测试。启动浏览器输入： http://localhost/YOURURL 来检测你的网站可否可以正常访问。 

Lighttpd + SCGI
-----------------
#. 配置lighttpd.conf：
   ::
     
     scgi.server=(
	"/uliweb.scgi"=> (
			 "main" => (
			 	"socket" => "/tmp/uliweb.sock",
				"check-local" => "disable",
				),
			),
	)
	url.rewrite-once = (
			 "^(/.*)$" => "/uliweb.scgi$1",
	)

#. 运行：
   ::
     
     python runcgi.py protocol=scgi socket=/tmp/uliweb.sck method=threaded daemonize=true

.. note::
	runcgi.py需要使用flup,下地址：http://trac.saddi.com/flup


IIS + SCGI
--------------

#. 下载安装pyISAPI_SCGI 地址: http://code.google.com/p/pyisapi-scgi/
#. pyISAPI_SCGI配置方法 http://code.google.com/p/pyisapi-scgi/wiki/PyISAPI_SCGI_0_6_17
#. 编辑scgi.conf:
   ::
     
     port=3033 #设置一个空闲的端口号


#. 运行:
   ::
     
     python runcgi.py protocol=scgi host=127.0.0.1 port=3033 method=threaded

.. note::
	runcgi.py需要使用flup,下地址：http://trac.saddi.com/flup


虚拟主机(DreamHost,BlueHost,HostMonsger等)
--------------------------------------------

FastCGI
~~~~~~~~~

#. 安装python, 参考http://wiki.dreamhost.com/Python
#. 新建dispatch.fcgi,内容：
   ::
   
     #!/home/yourname/bin/python (你安装的python的路径)
     import sys
     from runcgi import run
     run(method='threaded',protocol='fcgi')

#. 编辑.htaccess，内容：
   ::
   
     Options +FollowSymLinks +ExecCGI
     RewriteEngine On
     RewriteBase /
     RewriteRule ^(dispatch\.fcgi/.*)$ - [L]
     RewriteRule ^(.*)$ dispatch.fcgi/$1 [L]
     AddHandler fastcgi-script .fcgi #或者是AddHandler fcgid-script .fcgi

CGI
~~~~
#. 安装python, 参考http://wiki.dreamhost.com/Python
#. 修改runcgi.py,将第一行内容修改为：
   ::
     
     #!/home/yourname/bin/python (你安装的python的路径)


#. 修改.htaccess,内容：
   ::
     
     Options +FollowSymLinks +ExecCGI
     RewriteEngine On
     RewriteBase /
     RewriteRule ^(runcgi\.py/.*)$ - [L]
     RewriteRule ^(.*)$ runcgi.py/$! [L]
     AddHandler cgi-script .py
    
.. note::
	
	以CGI方式运行，需flup 1.0以上版本。