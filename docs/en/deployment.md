# Deployment


## Apache


### mod_wsgi


1. You should refer to the [mod_wsgi](http://code.google.com/p/modwsgi/) document, and
    install the mod_wsgi.so module for Apache.

    * Copy mod_wsgi.so to apache/modules directory.

    For Windows instructions, see:

    > http://code.google.com/p/modwsgi/wiki/InstallationOnWindows
    
    If you are using Linux, see:

    > http://code.google.com/p/modwsgi/wiki/InstallationOnLinux
    
1. Modify Apache's httpd.conf file

    * Add the code below

        ```
        LoadModule wsgi_module modules/mod_wsgi.so
        WSGIScriptAlias / /path/to/uliweb/wsgi_handler.wsgi
        
        <Directory /path/to/youruliwebproject>
        Order deny,allow
        Allow from all
        </Directory>
        ```

        The code above assumes that the root URL is `/`, you can change this to
        suite your project, for example `/myproj`.
        Here is an example of a configuration on the Windows platform:

        ```
        WSGIScriptAlias / d:/project/svn/uliweb/wsgi_handler.wsgi
        
        <Directory d:/project/svn/uliweb>
        Order deny,allow
        Allow from all
        </Directory>
        ```


1. Restart apache
1. Test it. Startup a web browser, and enter the URL [http://localhost/YOURURL](http://localhost/YOURURL)
    to test if eveerything went well.


## Static files

Uliweb can serve static files, but you may want to use Apache or any other
webserver instead because they are much faster at doing it. If you decide to
let a web server serve your static files, use the exportstatic command to
collect all static files from all available apps to target directory, then
configure target static directory in your web servers configuration file.

