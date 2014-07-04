# 0.3.1 2014-07-04

## 问题修复

* 修复 `include` 在 ini 中的bug
* 修复在 orm.get() 中的condition判断bug
* 修复 recorder bug

## 功能优化

* 增加 qqmail 邮件服务后端支持，感谢 Yubin Wang <harry198344 AT gmail.com>
* 增加 `yes` 命令行选项，删除 makeapp, makeproject 命令的 `--force` 选项
* 删除 `Command` 类中的 `has_options` 属性，改为根据 `option_list` 的长度来动态判断

## ORM相关

* 增加 `sqlshell` 命令
* 向 ORM 结果对象添加 `having` 和 `join` 方法
* 增加整个数据库 dump 和 load 支持 #33
* 向 orm 的 __all__ 添加 `NotFound`
