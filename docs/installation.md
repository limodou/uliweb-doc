# 安装说明


## 要求


* Python 2.6+ 目前不支持3.X
* setuptools 0.6c11+


## 额外要求


* SQLAlchemy 0.6+ (如果使用Uliweb ORM需要安装它)

最简单的方法是使用easy_install或pip，如:


```
easy_install Uliweb
pip install Uliweb
```

另外如果你想跟踪最新的代码，可以使用git来下载代码，

```
git clone git://github.com/limodou/uliweb.git
cd uliweb
python setup.py develop
```

使用develop安装只会在Python/site-packages下建一个链接，并不会真正安装，好处就是更新方便。
不过，当Uliweb的版本升级了，还是要再执行一下安装过程的。

当然你也可以直接通过 install 来安装。


```
python setup.py install
```

