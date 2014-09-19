# 0.4

## 问题修复

* 修正 Pickle 缺省值Bug，将不会自动将空值转为 ''
* 修正当存在 group_by, limit, join 时的 count 的实现，将使用 `select count(*) from (select * from table)`
* 修正 uliweb load 在处理cvs格式时的Bug，感谢 taogeT
* 修正 `tmp/templates_temp` 创建Bug
* 修正显示模板块顺序不正确的Bug

## 功能优化

* 使用tornado的模板代码重构uliweb的模板实现，具体变化内容详见 [模板](../template.html)
* 添加 staticize 命令，实现静态化
* 添加 `__debug__` 参数用于跟踪 i18n 语言的变化
* ORM多数据库配置时，增加复制的支持，你可以在 CONNECTIONS 配置项中进行设置
* 向 ORM 中添加 `set_session()` 函数
* 向ORM中的 Property 类添加 `fieldname` 参数
* 向 `load` 和 `loadtable` 添加 `-z` 参数，感谢 linuxr
* 向模板的 `Loader.load()` 方法添加 `layout` 参数，可以用来实现动态模板继承
* 添加 `validatetemplate` 命令，可以用来检查项目，app或单个模板的语法是否正确。可以方便用来检查升级到0.4后的模板问题。 详情参见 [validatetemplate](../manage_guide.html#validatetemplate)