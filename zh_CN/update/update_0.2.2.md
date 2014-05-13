# 0.2.2

* 向 `SortedDict` 添加 `clear()` 函数
* 向 AddView, EditView 添加提交保护，缺省为不启动。它可以用来防止多次提交。但对于
  前端建议再増加相关的措施，比如在提交时将按钮禁掉。如果想要其生效，需要传入 `protect=True` 参数。
* 向 uliweb find -t 命令添加 `--blocks` 和 `--with-filename` 参数，前者用来显示在
  模板中定义的块信息，后者用来列出定义相应块所在的模板文件名。同时向settings.ini
  中添加 GLOBAL/DEBUG_TEMPLATE 配置项，用来控制模板是否显示调试用的注释，用来区分
  不同的块的开始和结束。但是这种输出具有一定的破坏性，比如非HTML的结果等。所以只
  能用于调试，正式使用一定要关闭。比如，打开之后，在输出的模板中可能有：

    ```
    <!-- BLOCK title (apps/theme/templates/theme/skeleton.html) -->
    <!-- END title -->
    ```

* 増加filedown.py在下载时对 `content-range` 的处理，感谢 zhangchunlin 提供代码。
* 改进 `import_attr()` 的处理，増加对 pkg_resource 入口字符串格式的支持，比如：
  `x.y.z` 原来是根据从左向右逐层导入时，动态来判断后面的是模块还是属性，如果是
  模块，则继续导入，如果是属性则使用 `getattr()` 来处理。现在则可以定义为： `x.y:z.c`,
  这样可以更清晰表示 `:` 号前是模块，后面是属性。
* 向 `uliweb.contrib.orm` 上添加 requirements.txt，可以直接用 uliweb install
  来安装: SQLAlchemy, MySQL-python, alembic(这个是我修改的版本)。注意，要在你的应
  中用先配置 `uliweb.contrib.orm` 才可以。因为这个requirements.txt是在app上定义的。
* 添加　LOGO 文件，可以用这里面的图片来展示 uliweb。
* 向 runserver 命令増加 `--color` 参数，可以输出彩色日志。输省是不输出。同时，你
  可以根据需要，在settings.ini中对颜色进行配置，如缺省的为：

    ```
    [LOG.COLORS]
    DEBUG = 'white'
    INFO = 'green'
    WARNING = 'yellow'
    ERROR = 'red'
    CRITICAL = 'red'
    ```

    支持的颜色为: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE.

* 増加 `config` 命令。它可以用来向控制台输出配置文件的模板。目前可以生成 nginx, supervisor
  相关的配置。你也可以在自已的app中定义这样的输出。只要在app下创建 `template_files/config`
  的目录结构，然后创建 `xxxx.conf` 和 `xxxx.ini` 文件。在 `xxxx.ini` 中用来定义一些
  变量，这些变量将用于 `xxxx.conf` 中。

    ini格式定义示例为：

    ```
    [INPUT]
    port = '', 80
    path =
    ```

    port为变量名，值为一个tuple或者不定义，第一个值为提示用的文本，如果为空则表示没有额外
    说明。第二个表示缺省值。

    xxxx.conf 为uliweb格式的模板，如果存在模板变量，则需要与ini中的一致。同时
    有一些预定义的变量，如: project 表示项目目录名称，project_dir 表示项目目录。

    执行时可以： `uliweb config xxxx`

* 优化 `support` 命令，可以象config命令一样，在你的app下创建 `template_files/support/xxxx`
  这样的目录结构，下面放执行 `uliweb support xxxx` 时将要拷贝的文件及目录即可。
* 修复 tmplate 中normcase的bug，改为 normpath 。
* 重构ORM的关系字段的处理，让关系的处理为延迟执行（待get_model时才执行）。这样
  是为了解决存在循环引用的问题，但是带来可能的不兼容问题，就是反向关系的获取。
  如果A和B都是在一个文件中定义，那么在导入A时，B自然也被引入，如果B上有对A的关
  系定义，则A自动被注入一个反向关系。但是现在则要显示执行 get_model('B')才可以
  创建反向关系。
* `get_model()` 和 `set_model()` 中的Model名不再区分大小写。
* 修复当重名的URL定义存在时，后定义的没有替換前面定义的URL的bug。
* 修复 rbac 中没有使用 `functions.has_role()` 和 `functions.has_permission()` 的bug。
* 修复rules.py在处理View类继承时的bug。添加 `expose(replace=True)` 的支持，用来实
  现View类的替換方式，即不会増加新的一套URL，而是为了修改原来的View方法处理。
  如果replace=False,或不写，则为普通的派生方式.
* 向expose()増加template参数，这样除了可以在view函数中指定 `response.tmplate = 'xxxx.html` 外
  还可以直接在expose上指定。执行优先级，以response.template最高。
* 恢复 ORM 配置中关于 `NULLABLE = False` 的配置。这样字段缺省允许为 null。