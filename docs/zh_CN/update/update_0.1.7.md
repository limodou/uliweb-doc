# 0.1.7

更新内容

* 増加 pretty_dict 函数，可以以缩近的形式打印dict数据结构，主要是为了输出。
* 向functions中添加 encrypt 和 decrypt 函数，需要安装 uliweb.contrib.secretkey APP。这个app是一个des算法的加解密功能模块。缺省使用pyDes模块（它是纯Python的DES算法模块），通过配置可以改为其它的DES算法模块。
* 在命令行find中添加 --tree 参数，可以以缩近形式显示模板的继承和include的调用。
* 优化了alembic的功能，増加了对索引变动的支持。同时向ORM中添加只用于映射的 __mapping_only__ 配置属性，它的作用是将不会和数据库进行同步，只是用来映射数据库中已经存在的表。因为这个特性，所以你可以定义少于数据库中字段的Model。一旦在Model中定义了 __mapping_only__=True，则对于reset, syncdb之类的操作都将无效，在命令行上会看到相应的提示。在alembic中会显示有变化，但是不会真正去处理。同时对于数据库中多，而Model中不存在的情况，缺省的比较会自动忽略，除非在执行alembic时指定了--remove参数，才会生成drop table的语句。它可以用来防止某个项目是对现有数据库的一个不完全映射时的数据库更新，以避免将还在使用的表删除。
* 增加 funtcions.request_url() 函数，可以用来替換request.url，主要是可以正确处理多级反向代理生成URL的处理。
* 向ORM相关的命令行输出提示中添加Model的计数，可以让用户清楚了解执行的进度。
* 向 functions 中添加 authenticate 函数，方便用户实现自已的用户认证机制。
* uliweb shell 命令行可以传入文件名，则执行效果为启动uliweb项目环境后，执行这个文件，然后停在交互式环境中。
* 向ORM中添加 Lazy 和 Cache 的功能，这样可以实现在获得一个Model对象时，只装入指定的字段，其它的字段如果访问会自动再从数据库中获取。同时提供了 get_object Signal ，可以使用它实现ORM的cache功能。
* 向 uliweb.contrib 中添加redis_cli的APP，使用functions.get_redis()就可以方便获得redis的连接对象。
* 向ORM中添加post_do和rawsql, set_echo, SQLMonitor等功能。rawsql可以用于输出一条sqlalchemy风格的SQL的语句，并且是将相应的参数替換后的结果。set_echo是用于在线程环境下，打开sql输出，可以看到在执行过程中调用的sql语句。直到使用set_echo(False)来关闭这个功能，同时在输出时可以显示执行时间。SQLMonitor也是用来监控SQL执行的，但是它会将类似的SQL统一进行计数，最后显示一个统计结果，如每条SQL的执行次数，时间等。
* 在导出静态文件时，提供对静态文件的合并功能。前提是要在settings.ini中将要合并的css或js进行配置。这样会在导出静态文件时自动将一组的静态文件合并成一个文件。同时在使用use时，可以自动对这种合并后的文件进行处理。
* 在邮件处理中，増加了对sendmail后端的支持。
* 向session的key増加了独立于整个session的失效期的，以key为单位的失效期参数。
* 向ORM中的ManyToMany的ids()函数添加cache参数，用来指示是否将ids()得到的结果进行缓存。
* 升级werkzeug的版本到0.9.1
* 増加一个colorloged.py模块，可以用它来输出带颜色的日志信息。
