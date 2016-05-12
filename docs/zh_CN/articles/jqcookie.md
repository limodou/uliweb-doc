# jqcookie使用说明

因为jqcookie属于jqutils,所以要在相关的settings里加上

<code>
'plugs.ui.jquery.jqutils'
</code>

然后在template里加上

<code>
{{use "jqcookie"}}
</code>

这样就能在生成的html里加上相关的js文件

使用方面请参考 https://github.com/carhartl/jquery-cookie#usage
