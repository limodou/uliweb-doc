# 0.2.3

* 更新nginx配置文件的输出模板，添加 proxy_set_header 指令
* 向 ORM 添加 save_file() 方法，你可以用它保存select之后的结果集到一个csv文件中
* 修复 SortedDict 类中丢失的 clear() 方法
* 修改i18n处理，对于项目和apps方式的抽取，它将首先启动应用，这样是为了让自定义tag可以起作用。但是建议用户尽量不用自定义tag，因为模板中可以直接写python代码。
* 向utils/common.py中添加walk_dirs()方法，这个函数可以用来遍历目录，同时可以支持对文件名和后缀的过滤功能。

