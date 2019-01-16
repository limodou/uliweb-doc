# 0.2.1

* 添加 `uliweb.utils.timeit` 模块，用户可以使用 `with timeit(prompt):` 来计算下面
  代码的执行时间
* 修改 `file_serving()` 处理的 `action` 缺省值为 `None`. 这样缺省的 `/uploads` 文件
  服务不再是默认为下载。
* 修复ORM的Reference的validate问题。它影响Reference的默认缺省值。
