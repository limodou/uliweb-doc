# 创建项目

请注意，我们很多操作是通过命令行完成的，所以请确认你可以在命令行上执行python和uliweb
命令。如果不行，需要将Python的安装目录，以及它下面的Scripts子目录添加到PATH环境中。

## clone仓库

如果我们已经在github上创建了一个仓库，因此第一步就是将仓库clone到本地。

```
git clone git@github.com:limodou/uliweb-blogs-demo.git
```

这里你应该換成你所创建的仓库地址。这时，仓库还是空的。我们可以向仓库中添加常见
的一些文件，如：LICENSE, README.md等。具体如何使用git进行版本管理，本教程就不涉及
了，请大家自已查看git相关的一些书和教程。

clone完成之后，将会在当前目录下生成一个名为 uliweb-blogs-demo 的子目录（目录名
应该換成你真正的项目名）。

## 创建项目

我们将在项目目录下创建一个uliweb_blogs子目录，作为存放uliweb项目源代码的地方，
这个目录才是真正的uliweb项目的目录，因为可以在这个目录下启动我们的项目。

```
uliweb makeproject uliweb_blogs
```

生成的目录结构如下：

```
|-- .gitignore
|-- apps/
|   |-- __init__.py
|   |-- local_settings.ini
|   `-- settings.ini
|-- setup.py
`-- wsgi_handler.py
```

如果是一个git仓库，它已经自动生成了一个.gitignore，所以你可以修改它，添加你不想放
在git中的文件。如果你打开它你会看到：

```
*.pyc
*.bak
local_settings.ini
```

因此local_settings.ini缺省是不会添加到git中去的，这样保证不同的环境下local_settings.ini
不会被覆盖。

apps是一个标准的Python包结构，所以在引用它下面的模块时，其实可以使用 `apps.xxx`,
不过，Uliweb在启动时，会自动将Uliweb 项目目录以及apps目录添加到 `sys.path` 中，
因此可以在当前项目下直接使用apps下的模块，这一点在后面配置app时我们会看到。

Uliweb的项目是由若干个app组成的，所以它们都将放在apps目录下。

在 apps 下的两个 settings 文件，它们都是全局性的，一个是 local_settings.ini
，由于它不会被添加到 git 仓库中，所以不同的环境上， local_settings.ini 可以
不同，因此可以用来放置与环境相关的参数，比如数据库连接串等。

这里为什么会有setup.py？这是为了实现项目之间想要复用app时，可以把当前项目通过执行
setup.py来安装，这样别的项目就可以方便引用本项目的app了。Uliweb在安装时做了处理，
因为app一般都在apps目录下，但是安装之后，只需要通过 `project.app` 就可以使用了，不
需要添加apps。

wsgi_handler.py 是启动文件，在开发时不需要使用它。它是用在部署上，比如部署到
uwsgi下。

## 目录规划

与uliweb_blogs平级，我们还可以创建如 docs, test等目录，用来存放文档和测试代码。
