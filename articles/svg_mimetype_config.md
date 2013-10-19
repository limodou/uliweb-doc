# svg mimetype在uliweb中的设置

发现 [plugs][1] 中的wiki在python 2.6下以img方式显示svg不正确，经检查是content-type不对，正确的应该是 image/svg+xml。但是在2.7下就是正确的。于是发现2.6缺省的mime列表不全。查看了mimetypes模块源码，大概是这样处理的：

1. mimetypes会有自动检查系统中可能存放mimetypes的配置文件，它们可以放在如： /etc, usr/local/etc 等目录下，还可以直接识别象apache的标准安装目录下的mime.types文件。不过nginx的mime.types的格式和标准的不同，所以还无法直接识别。
2. mimetypes模块已经内置了一些mimetypes的类型，存放在 types\_map 变量中。它作为缺省值。可以和mimetypes的配置文件合并。而types\_map中，在2.7版本下其实也不存在svg的配置。不过在windows下，还可以从注册表中获取。
3. 新的类型可以通过 `add_type(type, ext)` 来注册。

在我的环境中，python是2.6，nginx中有svg的配置，标准的 `/etc/mime.types` 下没有。我使用的是nginx作为web server提供静态文件服务。如果只是使用nginx的静态文件，其实这个和python无关了，因为可以不经过python直接提供处理。

但是有些下载要经过python的处理，如 `uliweb.contrib.upload` app提供的文件下载功能。因此还是需要让python能够正确识别mimetypes的。一种方式是在某个mime.types中添加新的类型，不过这种试对于新的环境仍然要修改。于是我在upload app中増加了 `MIME_TYPES` 的配置，如：

    [MIME_TYPES]
    .svg = 'image/svg+xml'

每种后缀对应一个类型。这样就可以将mimetypes配置到应用中了。通用性比较好。

不过，要注意，它只对应用有效。

  [1]: https://github.com/limodou/plugs

update:

其实不是因为python版本的问题，而是环境问题。2.6和2.7中的mimetypes中的types\_map其实都没有对svg的类型定义。我之所以出现这样的问题是2.7是在windows环境下，它可以从注册表中读mimetypes的信息。而2.6是在linux下，的确没有定义。
