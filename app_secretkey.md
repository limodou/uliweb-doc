# secretkey(DES加解密处理)

secretkey是用来进行加解密处理的App。

## 配置说明

使用secretkey需要安装一个DES处理的库，缺省的支持是使用 [pyDes](http://twhiteman.netfirms.com/des.html),
它是纯Python源码的包，所以移植性好。

在你的settings.ini或local_settings.ini中配置 `uliweb.contrib.secretkey` 。

然后需要创建一个key文件，用来存放密钥。secretkey App已经提供了这样的一个命令，
因此你可以在命令行下运行：

```
uliweb makekey
```

执行这条命令，就可以在当前目录下创建一个名为 `secret.key` 的文件。如果想保存到
其它的目录，可以添加 `-o output_file` 参数。

## 使用说明

在secretkey的 `__init__.py` 中定义了可用的方法。并且为了方便，这些函数都定义为
FUNCTIONS函数（即可以使用functions.xxxx来调用）。

完成配置说明的要求，我们已经可以使用DES算法相关的处理了。

```
text = functions.encrypt(string)    #用来对文本加密
functions.decrypt(text)             #用来对文本解密
```

通常情况下，这样使用就可以了。但有时，我们要更精细的处理，比如读取key，生成密钥
等处理。可以使用 `get_key(keyfile=None)` 来读取key内容。 `get_cipher()` 得到加解
密处理对象等。详情参见API介绍。

为了方便使用，secretkey 提供了一些配置，在settings.ini中可以看到：

```
[SECRETKEY]
SECRET_FILE = 'secret.key'
KEY_LENGTH = 50
CIPHER_CLS = 'pyDes.des'
CIPHER_ARGS = {'mode':1, 'IV':"\0\0\0\0\0\0\0\0", 'pad':None, 'padmode':2}
```

其中：

SECRET_FILE --
    用来定义key文件。如果是相对路径，则以project作为起始目录。也可以是绝对路径。
KEY_LENGTH --
    使用 `makekey` 命令生成的key内容的长度。
CIPHER_CLS, CIPHER_ARGS --
    创建加解密对象所要使用的类及其参数。缺省是使用 `pyDes` 下的 `des` 类。理论上
    可以換成其它类。
    
## API介绍

get_cipher(key=None, keyfile=None) --
    获取加解密对象。key表示原始的key文本。keyfile表示密钥文件。
    
    如果key为None，则使用keyfile参数。如果keyfile参数为None，则使用settings.ini
    中配置的key文件。
    
    真正的加解密都是使用这个函数返回的对象来处理的。
    
encrypt(v, key=None, keyfile=None) --
    对文本 `v` 进行加密处理。key和keyfile都会传给get_cipher函数，利用返回的对象
    调用它的encrypt方法来返回密文。因为是二进制的，所以如果为了方便保存，你可能
    还需要使用 `x.encode('hex')` 来将二进制串转为16进制字符串。
    
decrypt(v, key=None, keyfile=None)
    对密文 `v` 进行解密处理。key和keyfile和encrypt的使用一样。如果你得到的是16
    进制文本，可以先 `x.decode('hex')` 转为二进制串然后再调用decrypt函数。

get_key(keyfile=None) --
    读取secret密钥文件内容。如果keyfile为None，则使用settings.ini中的配置。注意
    读取的文本并不是真正的密钥，它还要转为8字节的字符串，所以还要经过处理。
    
get_cipher_key(keyfile=None) --
    读取secret密钥文件内容，并转为8字节的密钥。这个函数将调用get_key()函数。
    
注意 get_cipher中的key参数使用的是未处理过的密钥文本，它会调用get_ciphyer_key来
对key进行转換处理。
