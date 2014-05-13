# 0.2.6

* 増加在定义关系字段时，当引用Model不是字符串而是Model类时发出警告的提示。需
  使用字符串名称。
* 修复在 ListView 和 SelectListView 中对 `manual` 和 `total` 处理的Bug。
* 修复 `rawsql` bug。
* 向 Generic ListView 中増加使用 `get_object` 的调用，使用缓存机制来处理引用对象。
* 修复 `get_cached()` Bug。
* 修复在 Generic 中 AddView 和 EditView 中处理 `process_files()` 的Bug。
* 在进入 Shell 环境前増加对调用 `readline` 的支持。
* 将乐观锁相关的参数由 `occ` 改为 `version` 。
* 修复 ManyToMany 缓存值在保存时没有正确使用的Bug（由于没有存入 `_old_values` ）。
* 当在 Model 中定义了主键时，将不再自动创建 `id` 字段，如：

    ```
    user_id = Field(int, primary_key=True, autoincrement=True)
    ```

* 修复 `sqldot` 命令在处理 settings.ini 中定义的 Model 名称与 `__tablename__` 不一致
  时的Bug。
* 优化 `sqlhtml` 文档输出，増加 Model 描述及索引的输出。
* 将 `runserver` 的日志输出改为缺省是彩色输出，可以使用 `--nocolor` 关闭。
