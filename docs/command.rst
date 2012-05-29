====================================
如何编写自已的命令
====================================

Uliweb内置了一个命令系统，其中在uliweb/manage.py中已经内置了一些常用命令。同时
你也可以在某个app中，按照命令编写的要求来编写app相关的命令。这样一旦在settings.ini
中的 ``INSTALLED_APPS`` 里引入了这个app，这些命令就可以被 Uliweb 使用。你可以
输入 ``uliweb`` 来查看当前有哪些可用的命令。

下面就来介绍一下如何编写自已的命令。

创建commands.py文件
-----------------------

在你的app下创建一个commands.py的文件，文件结构如下::

    from uliweb.core.commands import Command
    from optparse import make_option
    
    class DemoCommand(Command):
        name = 'demo'
        option_list = (
            make_option('-d', '--demo', dest='demo', default=False, action='store_true',
                help='Demo command demo.'),
        )
        help = ''
        args = ''
        check_apps_dirs = True
        has_options = False
        check_apps = False
        
        def handle(self, options, global_options, *args):
            print 'This is a demo of DemoCommand, you can enter: '
            print
            print '    uliweb help demo'
            print
            print 'to test this command'
            print 
            print 'options=', options
            print 'global_options=', global_options
            print 'args=', args
            
以上是一个命令的示例，仔细解释一下。

.. attention::
    除了手工创建上面的文件和内容，Uliweb还提供了一个命令可以方便生成代码的模板，
    使用方式为::
    
        uliweb makecmd [appname]
        
    如果没有给出 ``appname`` ，则会在当前目录下生成一个 ``commands.py`` 文件。
    如果给出 ``appname`` ，则会在指定的 ``appname`` 下创建 ``commands.py`` 文件。
    
命令类
--------------

类属性
~~~~~~~~~~~~~~

每个命令都应该从Command类派生而来。这个类有几个属性可以覆盖，分别为：

name
    命令的名字。你将使用它来执行，执行方式如::
    
        uliweb demo
        
option_list
    它是参数列表。定义形式为 ``optparse`` 所要求的格式。每个参数都使用 ``make_option`` 
    来定义。它支持短参数和长参数。其中短参数就是类似 ``-d`` ，长参数就是 ``--demo`` 。
    ``dest`` 表示解析后的参数将使用的变量名。 ``default`` 为缺省值。 ``action``
    表示解析后的值如何存储，这里为 ``store_true`` ，表示一旦给出参数，则将保存为
    ``True`` 。所以，这种方式会将参数解析为 ``Boolean`` 值。那么如果要解析为字符
    串怎么做，只要去掉 ``action`` 即可，缺省就是字符串，这样可以在参数后面接收
    参数。 ``help`` 为此参数的帮助信息。
help
    它会额外输出当前命令的帮助信息。用于对当前命令进行解释。
args
    将用在帮助信息的显示上。它与下面的 ``has_options`` 一起用在帮助信息的显示上。
    对命令的执行没有影响。如果定义 ``has_options`` 为 ``True`` ，则命令帮助显示
    为::
    
        uliweb demo [options] <args>
        
    如果为 ``False`` ，则命令显示为::
    
        uliweb demo <args>
        
has_options
    用于帮助信息的显示。
check_apps_dirs
    用来显示是否检查当前目录下存在 ``apps`` 子目录。缺省为 ``True`` 。
check_apps
    用来检查app是否存在。如果设置为 ``True`` ，则假定传入的参数应该是 app 。这里
    的参数是进行过命令行参数解析之后剩下的参数。
    
类方法
~~~~~~~~~~~~~

def get_apps(self, global_options, include_apps=None)
    返回当前项目所有app的清单。类似于uliweb中的get_apps，不过它因为使用了global_options
    所以使用会更为简单
def get_application(self, global_options)
    根据配置信息创建一个application的实例，它会调用 ``make_simple_application`` 。
def handle(self, options, global_options, \*args)
    用于子类继承的方法。用户自定义的命令应该覆盖这个方法。
    
handler方法
----------------

handler方法是命令类的主体，它接三个参数:

options
    为本命令专有的参数，它是与类中的 ``option_list`` 的定义相对应的。
global_options
    为命令全局参数。Uliweb的命令系统提供了缺省的全局参数，如 ``-h`` , ``-v`` 等
    参数。因此用户在定义自已的命令参数时，注意不要与全局的参数重复。
args
    它就是参数解析之后剩下的参数。
    
常用在命令中的uliweb方法
---------------------------

extract_dirs
    从指定的模块的子目录下抽取相应的目录和文件到指定目录下。
    
    ::
    
        from uliweb.utils.common import extract_dirs
        
    函数定义为::
    
        extract_dirs(module, path, dest_path, options)
        
    module
        模块名。
    path
        模块下的目录路径。
    dest_path
        目标目录。
    options
        可使用参数。如::
        
            verbose=global_options.verbose
            
get_apps
    获得当前项目下所有的app名字
    
    ::
    
        from uliweb import get_apps
        
    函数定义为::
    
        get_apps(apps_dir, settings_file, local_settings_file)
        
    apps_dir
        当前项目下的apps目录。使用时如::
        
            global_options.apps_dir
            
    settings_file
        settings.ini文件路径。使用时如::
        
            global_options.settings
            
    local_settings_file
        local_settings.ini文件路径，使用时如::
        
            global_options.local_settings
            
常用global_options属性
------------------------

verbose
    对应于 ``-v`` 参数。表示是否要冗余输出。
apps_dir
    项目下的 ``apps`` 子目录。
project
    项目目录。
settings
    当前项目的settings.ini文件。用户可以使用非settings.ini名字。
local_settings
    当前项目下的local_settings.ini文件。用户可以使用非local_settings.ini名字。
    
Command类
-------------

``Command`` 类是所有命令的基类。大多数方法请参见 ``uliweb/core/commands.py`` 文件。
其中有 ``get_apps`` 方法，功能和uliweb中的一样，不过需要传入的参数不同，如:

get_apps
    ::
    
        get_apps(global_options, include_apps=None)
    
    使用起来比uliweb下的get_apps要简单一些。
    
get_application
    ::
    
        get_application(global_options)
        
    获得当前应用的实例，它将完成整个应用的初始化工作