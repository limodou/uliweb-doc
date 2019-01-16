# APIs

Uliweb-UI 提供了常用的一些js的API,分别描述如下:

## load

```
load('module', callback)
load(['module', ...], callback)

function callback () {...}
```

load 用来实现动态装入某个ui的组件,其中第一个参数可以是一个组件名或组件数组,它也可以是一个真正的URL.为了方便
使用,Uliweb-UI将常用的组件定义在了 settings.ini 中, 采用 `TEMPLATE_USE` 的定义方式.这种定义方式可以在
模板中使用 `{{use "name"}}`, 但是不能直接用在 `load` 中,因此需要使用 `uliweb jsmodule -a uliweb_ui`
来生成一个叫 `jsmodules.js` 的文件,并且放在 `uliweb_ui/static/jsmodules.js` 下. 使用 `jsmodule` 
命令时,需要在某个项目目录下运行,不能直接运行.

通常在 Uliweb-UI 中定义的 module 命令都是以 `ui.` 开始,具体有哪些可以使用的组件,可以查看