# 0.2

更新内容

* 修复 auth.models `get_href` 错误
* 修改 ORM `save()` 处理，它将保存manytomany数据
* 向 `save()` 中添加 `changed`, `saved` 和 `send_dispatch` 参数。其中 `changed`
  是一个回调函数，当有更新时（不是新増)时被调用。 `saved` 也是一个回调，当保存
  了数据时被回调，它包括更新和新増两种情况。 `send_dispatch` 表示是否发送pre_save和
  post_save信号。
* 改进 `set_echo()`, 添加 `time`, `explain`, `caller` 等参数。
* 向 utils.common 模块添加 `get_caller()` 函数。
* 向 form 模块添加 `CheckboxSelectField` 字段类。
* 添加 `jsonp` 函数，使用方式如json。
* 修复rule合并错误。
* 优化 `get_redis(**options)` 允许传入参数。
* 优化 `jsonp()` 限制 `callback` 参数只能传入字母和数字。
* 优化 pyini, 支持跨section变量引用和延迟处理。
* 优化 `load` 命令，添加总条数和花费时间显示，同时在插入时采用批量插入。
* 向 uliweb/utils/image.py 添加 `test_image` 函数。
* 添加 `xhr_redirect_json` 支持. 在启动uliewb应用时，可以传入 `xhr_redirect_json` (布尔值) 参数，
  缺省值是 `True` 。它的作用是，如果请求是ajax，重定向将返回为一个json结果，错
  误码是 500。所以前端可以使用它来根据需要进行重定向。
* ORM `remove/clear` 函数在传入空条件时将删除全部记录。
* 向 uliweb.utils.common 中添加 `classonlymethod()` 方法, 它和classmethod类似，
  但是它可以限制类属性只能通过类来调用，而不是实例。主要用来控制ORM的Model delete 方法 。
* 重构上传App，添加 `download` 到 functions 配置。
* 优化 secretkey app, 添加 `-o` 来指定输出文件名。向大部分加解密函数添加 `keyfile` 参数。
* 向upload App添加 `MIME_TYPES` section，但是它只会对uliweb应用有效，而不是对web server。
* 优化 `call` 命令，允许调用在apps目录之外的模块，添加project目录到 `sys.path` 中。
* 修复 ORM PICKLE 更新错误, 使用 `deepcopy` 来保存 old_value。
* 添加 tornado 服务器支持。
* 添加 gevent 和 gevent-socketio 服务器支持。
* 添加 `install` 命令支持，你可以在项目目录或app目录下写 `requirements.txt`。
* 在执行 `makeproject` 时添加 `setup.py` 文件。
* `make_application()` 可以重入。
* 添加 `ORM/MODELS_CONFIG` 配置支持。