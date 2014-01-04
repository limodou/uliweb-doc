# Deployment Guide


## GAE(Google Application Engine)

GAE is a plaform provided by Google for web applications. To use GAE in combination
with ULiweb for web development, you will need a GAE account. Follow the instructions
on the GAE main site to create one.

You should test your project code under the GAE SDK development environment first
before the final deployment.


1. Using the `export` command, export Uliweb to your project directory. You should name
    your project directory using the application name you created in
    GAE. For example, say your project name is `myproject`, and you installed GAE SDK in
    `C:\Program Files\Google\google_appengine`, you can use the command:

    ```
    python manage.py export "C:\Program Files\Google\google_appengine\myproject"
    ```

    You would notice that the target directory is quoted by double-quotes,
    that's because there is space character in the directory. The deployement is ready after this step.
1. Modify the `app.yaml` file, change the value of `application` to your project name,
    for example: `myproject`.
1. Begin your web development using the Uliweb development server
    first, switch to the GAE development server for further testing.
1. Upload your project with the `appcfg.py` tool:

    ```
    python appcfg.py update myproject
    ```



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

