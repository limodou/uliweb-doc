# 常用API

## manage.py

### make_simple_application

用于创建application实例。

```
def make_simple_application(apps_dir='apps', project_dir=None, include_apps=None,
    settings_file='', local_settings_file='',
    default_settings=None, dispatcher_cls=None, dispatcher_kwargs=None, reuse=True,
    pythonpath=None):
```

default_settings --
    用于覆盖缺省的配置信息。格式为 `section/key`, 如 `PARA/test`.