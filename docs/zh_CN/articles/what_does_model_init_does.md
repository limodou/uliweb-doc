导入一个Model时都做了些什么？
===============================

当使用get_model(model_name, engine_name=None)时，都做了哪些事呢？

1. 从engine中的models属性里，查找model_name，找到后，如果model_path为字符串，则
   开始导入对应的模块
2. 导入模块，则开始对Model类进行初始化
    1. 创建Property对象，对于Reference等会对引用的Model执行get_model，所以这里可能循环
    2. 执行Model元类初始化，执行 `__property_config__` 方法
3. 对类执行bind操作，关联metadata
    1. 根据所有Property来创建Column,执行Property的create方法
    2. 创建Table对象
    3. 处理Model的OnInit方法，如进行索引的处理