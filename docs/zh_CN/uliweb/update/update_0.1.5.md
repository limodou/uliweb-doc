# 0.1.5


更新内容


* 修改cache设置，移除file_dir和lock_dir
* 添加更多的dispatch调用异常输出信息
* 添加uliweb.contrib.form app，添加get_form函数
* 修改auth支持get_form功能
* 改进file_storage过程。
* 修正RedirectException显示bug。
* 添加TablenameConvert到uliweb.orm中，通过orm.set_tablename_converter(converter)传递函数，或者在settings.ini中定义，如：

    > [ORM]
    > TABLENAME_CONVERTER = 'uliweb.utils.common.camel_to_'
当Model名字是CamelCase时，将转化为camel_case
* 添加Reference，OneToOne，ManyToMany关系到Model层级
* 如果collection_name为None，并且tablename_set已存在，将自动创建新的collection_name,因此collection_name将会被会复制，如果传递了collection_name，并且tablename_set已经存在，将抛出异常，请注意其中的差别。
* 修改默认CHAR, str， unicode的max_length为255，之前默认为30.
* 在validator.py添加IS_LENGTH_LESSTHAN和IS_LENGTH_BETWEEN。
* 添加[GLOBAL_OBJECTS]机制，此处的对象配置将被注入到uliweb中。
* 在uliweb中添加validator，使用[VALIDATORS]机制
* 在generic.py中添加IS_LENGTH_LESSTHAN，如果max_length存在。
