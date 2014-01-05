# Architecture

Uliweb is a Python web application framework that utilizes a MVT architecture.


## MVT Framework

The **M** or Model. A model is an object ralationship mapping of database table.
Uliweb ORM is based on SQLAlchemy package(not its ORM layer, but basic SQL
layer). You define your models, place them in the `models.py` file and use ORM APIs or
just underlying SQLAlchemy APIs to interactive with database.


The **V** or View can based functions or classes. All files which begin with `views` 
will be treated view module, so `views.py` or `views_auth.py` will be the right
view module filename. When
view function is run, Uliweb will provide an environment for the the view to run in
Uliweb uses `func_globals` inject(You can inject objects into function's `func_globals` 
property, so you can directly use
these injected objects without importing or declaring them.) So you can use
`request`, `response`, `json`, `redirect`, etc. directly in the view function. And some special
objects such as `request`, `response` will be processed to thread local related. 


The **T** stands for template. Templates don't need to be rendered
explicitly, just return a dict variable from the view function, and Uliweb
will automatically find a matching template to render according the function
name. For example, if your view function is named `show_document()`, the
default template will then be `show_document.html`. If you result other type
data, Uliweb will not automatically render the result with template but convert
the result to a Response object directly and returns to web server. Except template
auto render mechanism, you can also provide template filename in `expose(url, template=template_file)`
function or just assign `response.template = template_file` in views function.


## Project Organization

A web application is defined as a **Project** in Uliweb. An Uliweb web
application Project consists of any number of smaller modules. These
modules can be any fucntionality unit, them called **Apps** in Uliweb.
These modules can include: templates, static files, views, model definitions,
middlewares, configuration, etc. An App can be a normal python package, so
you can make it a standalone package so that it can be installed separately .

The basic directory structure of an Uliweb Project is as follows:


```
project/                        #project directory
    .gitignore                  #gitignore file
    apps/                       #all apps should be placed in it
        settings.ini            #project level configuration file
        local_settings.ini      #local project level configuration file
        app1/                   #app1
            templates/          #template directory
            static/             #static directory
            views.py            #views file
            models.py           #models file
            settings.ini        #app level configuration file
        app2/                   #app2
    wsgi_handler.py             #startup file
    setup.py                    #make your project installable
```


For `local_settings.ini` should not be tracked in version control system, because
it can includes environment-related configure options, so different environments
may have some different configure options. 

When uliweb startup, it'll read all settings.ini defined in apps first, according
to the order of `INSTALLED_APPS`, next will be `apps/settings.ini`, the last will
be `apps/local_settings.ini`. So you can overwrite existed configure options in
`apps/settings.ini` or `apps/local_settings.ini` depending on your needs.


## App Organization


### App Organization Structure

Uliweb applications are placed in the `apps` folder. Uliweb also ships with many
built-in apps, they are stored in the `uliweb/contrib` folder. And user can 
also use third-party uliweb apps. 

There is a global settings file for all apps in the `apps` folder called `settings.ini` .
Each app can have its own `settings.ini` file for initialisation and configuration purposes.

An Uliweb **app** in its basic form is actually Python package, this implies the precense
of an empty `__init__.py` file in its root folder. Further, an **app** may have the following
components:


* `settings.ini` file, the configuration file of the app.
* `config.ini` file, used to define app dependencies.
* `templates/` directory, used to store template files.
* `static/` directory, used to store static files like images, css files, javascript files.
* `views*.py` view function will be written in them.
* `models.py` model class will defined in it.
* Other files used in the app.

A `settings.ini` can be used to carry out some initalization work. For example,
database, i18n configuration etc.


### APPs configuration

You should configure what apps should be used in your project, so you should
add something in `settings.ini` like this:

```
[GLOBAL]
INSTALLED_APPS = [
    'uliweb.contrib.orm',
    'third-party-app',
    'app1',
    'app2',
]
```

So when uliweb startup the project, the apps defined in `settings.ini` will be
automatically loaded.

If you have some testing aimed apps that you don't want to configure them in
`settings.ini` yet, you can config it in `local_settings.ini`, Uliweb will merge
same named options together.

### Apps are logically complete components

Even though you can split a project( complete web application) into
different apps physically, every app should be treated as a logically
complete component. This is however, not a rule or restriction as Uliweb is
flexible enough to allow the components in an **app** , for exmple the
`settings.ini` file, the `static` and `templates` to be made available to
other **apps** to facilitate cross-application communication. For example,
if you create a template `layout.html` in an app **A** , you can directly
use it in an app called **B** .

In a deployed production project, you could, for example, have a main app
that contains all the globally available static and template files. It
could even take care of I18n and database initialisation processes.


### Creating dependencies between apps

If you intend to make an app dependant on another app or more, you can
define the dependancies in a `config.ini` file and then place this file in
the app folder, it content should looks like:


```
[DEFAULT]
REQUIRED_APPS = ['uliweb.contrib.i18n']
```

So when Uliweb import the app, if it find `config.ini` in its app folder, it'll
parse `config.ini`, and import dependent apps automatically. 


## Defined in distributed but used in centralized

As described above, you can define static files, template files, configuration, 
views, models, etc
in apps, but when Uliweb startup, you can treat them as one whole things.

## Startup and initialisation process

When Uliweb startup, it'll do following things:

1. Import and merge all settings.ini
2. Process dispatch bindings
3. Import apps
4. Import views
5. Process exposes
6. Process middlewares

## URL Mapping Process

At present, Uliweb supports two ways to define URLs in views.

One way is to define a URL by using the `expose` decorator. This is the easier method, just like:

```
@expose('/login')
def login():
    return {}
```

The other way is define URL in settings, just like:

```
[EXPOSES]
login = '/login', 'uliweb.contrib.auth.views.login'
logout = '/logout', 'uliweb.contrib.auth.views.logout'
```

To assist in URL management, Uliweb provides an `url_for` function. This function
can be used for reversed URL creation, it'll create URLs according to the correspondingview function
name. For more details, see the [URL Mapping](url_mapping.html) document.


## Extending Uliweb

Uliweb provides many ways to extend it:


* Dispatch extension. This is a dispatch mechanism. Uliweb has already predefined
    some dispatch points, when it runs there, it'll find if there are some
    associated receiver functions existed, and will call them one by one.
* middleware extension. It's similar with Django. You can configure them in
    `settings.ini`, and it can be used for processing before or after the view
    process.
* views module initialization process. If you defined a function named as
    `__begin__`, it'll be invoked before invoke the exact view function. So you can
    put some module level process code there. So I suggest that you can divide
    different views modules via different functionalities.

