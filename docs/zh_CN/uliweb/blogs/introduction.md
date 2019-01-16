# 介绍

## 目的

Web开发需要大量知识的汇集，Uliweb框架本身也提供了非常多的实现手段。单纯地看文档
可能未必能够了解某些功能的使用场景，因此我开始写这个教程，希望把一些新的、方便的
用法介绍给大家，并且尽量展示更多框架如何与其它的功能结合的一些示例。

* 常见命令行的使用
* 原始的Form交互处理
* 使用Generic交互处理
* 使用generic命令行自动生成代码框架
* 如何处理文件上传及下载
* Ajax的使用示例
* 如何将常用的一些js,css库封装为app
* 邮件处理、守护及异步调用框架示例
* 如何部署

## 准备uliweb环境

在开始项目前，需要安装: python环境，以及 setuptools, pip, uliweb, plugs, 
sqlalchemy, alembic等模块。

其中python版本目前只支持2.6和2.7。3.3+还在准备中。

[setuptools](http://pypi.python.org/pypi/setuptools) 和 
[pip](http://pypi.python.org/pypi/pip) 可以去 pypi 上下载最新的版本进行安装。

安装Uliweb和Plugs可以：

```
pip install uliweb
pip install plugs
```

因为Uliweb和plugs会经常变化，所以最好的方式是使用源码。你可以使用git将Uliweb和
plugs的仓库clone到本地，然后通过：

```
python setup.py develop
```

来进行安装。这样以后如果要保持代码是最新的，只要执行：

```
git pull
```

就可以了。

至于sqlalchemy, alembic可以在后面再安装。

## 准备git环境

这里假设你将要使用git作为你的版本管理工具，并且会将代码放在github上。所以你需要
安装git环境。git工具有很多，这里我使用的是 [git官网](http://git-scm.com/downloads) 上的命令行工具，github本身还提
供了GUI的工具。在安装好git命令行之后，在windows环境下确认可以进入git bash。在linux
下可以启动git。

本项目的代码已经放在github上，地址是： https://github.com/limodou/uliweb-blogs-demo
所以你可以clone这个仓库来查看源码。

欢迎大家在阅读中提出问题，一起完善这个教程。

这个教程本身是放在 https://github.com/limodou/uliweb-doc 项目中的。

## 功能需求

下面把本教程打算实现的功能列在下面，希望我能够全部完成。也希望大家一起来添加内容，
让这个教程更完善。

简要说明一下：我打算实现一个多人共同编写的博客，所以整体上还是一个博客，但是可以
一起展示，也可以按人来分别展示。评论则采用第三方的功能。页面功能尽量考虑实现静态
化。实现基本的用户管理功能。可以记录用户操作。实现邮件异步发送。博客将采用Markdown
语法来写作，可以支持图片上传。

* blog功能
    * blog首页展示
    * blog分页
    * 单个blog文章展示
    * disqus评论集成
    * blog创建
    * blog编辑
    * 分类创建
    * 分类管理
    * Tag管理
    * RSS生成
    
* 后台管理
    * 用户管理
        * 用户注册
        * 用户审批(超级用户)
    * 操作日志
    
* 守护
    * 邮件发送
    