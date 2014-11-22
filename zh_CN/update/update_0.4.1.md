# 0.4.1 2014-11-22

## 问题修复

* 修正 generic 中的 AddView 和 EditView 对 version的处理。当version为真时才会将version值
  传入obj.save()中。而不是False时也自动传入。以避免表中无version字段时的出错。
* 修正对同一个view函数同时使用 expose('/') 和 expose('') 时不正确的bug。
* 修正在一个Model中多次使用 ManyToMany 使用 through 时
* 恢复 count() 的处理使用旧的方式，即使用条件来计算，而不是根所结果集，对于结果集情况需要自行处理，因为
  有可能对性能影响很大。
* 修正模板中使用 try: 的bug

## 功能优化

* 增加 sequence app，可以用来它生成序列值。详情参见 [sequence](app/sequence.html)
* 优化 nginx 和 supervisor 配置内容的生成
* 向URL匹配规则缺省添加 strict_slashes=False 的参数，这样URL结尾有无 '/' 都是正确的
* 优化 Reference() ，如果 reference_class 为 None，则自动处理为 SelfReference
* 优化 ManyToMany()，如果 reference_class 为 None，则自动实现对自身的多对多的关系
* 在app下的settings.ini中添加 #{appname} 的支持，会自动替换为当前app的名字。
* 在模板中添加对 head.js 的支持，可以使用 {{head "xxx"}} 和 {{head_link "xxx.js"}}标签，类似于
  {{use}}和{{link}}。不过uliweb本身没有包含 head.js，将放在plugs中，并且是我修改过的。

