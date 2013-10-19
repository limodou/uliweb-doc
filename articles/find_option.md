# 查找配置项的定义

在uliweb中，我们会把配置写在各种settings.ini中，因为uliweb可以实现配置项的合并处理，所以我们最终拿到的配置值可能无法知道都是从哪些配置文件中来的，因此我新加了一个 `uliweb find -o option` 的命令。示例如下：

    D:\project\cc\ctasks-master>uliweb find -o ASYNC_EXEC_CONFIG
    ------ Combined value of [ASYNC_EXEC_CONFIG] ------

    [ASYNC_EXEC_CONFIG]
    channels = ['default', 'manual']
    error_sendmail = 'print'

    ------ Detail   value of [ASYNC_EXEC_CONFIG] ------

    ...nc_exec_daemon\settings.ini:0004 [ASYNC_EXEC_CONFIG]


    .\apps\settings.ini           :0212 [ASYNC_EXEC_CONFIG]
    .\apps\settings.ini           :0213 channels = ['default','manual']


    .\apps\local_settings.ini     :0159 [ASYNC_EXEC_CONFIG]
    .\apps\local_settings.ini     :0160 error_sendmail = 'print'

可以看到，首先显示合并后的值，然后再显示都是从哪些settings.ini文件，哪行代码得到的配置。option的值可以是section的值，或section/key的值。再如：

    D:\project\cc\ctasks-master>uliweb find -o GLOBAL/DEBUG
    ------ Combined value of [GLOBAL/DEBUG] ------
    True
    ------ Detail   value of [GLOBAL/DEBUG] ------
    ...b\core\default_settings.ini:0002 DEBUG = False
    .\apps\settings.ini           :0004 DEBUG = True
    .\apps\local_settings.ini     :0095 DEBUG = True
