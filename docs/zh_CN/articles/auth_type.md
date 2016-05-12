# 使用 auth_type 扩展认证方式

为了让 uliweb.contrib.auth 里定义的 user 和 usergroup 表同时具备多种认证方式的扩展性,目前已经为这两个表加上了相关的字段,详细情况见相关的 [model定义](https://github.com/limodou/uliweb/blob/master/uliweb/contrib/auth/models.py)
这样可以让多种认证方式并存, 如同时支持本站注册,ldap,sns帐号登入等等

### 增加新的 auth_type
大概需要做:

* 在settings里添加相关的 auth_type 定义,看 [这个例子](https://github.com/zhangchunlin/shapps/blob/master/shapps/auth/ipuser/settings.ini)
* 在此种认证方式下新建用户的时候要使用相应的auth_type值,看 [这个例子](https://github.com/zhangchunlin/shapps/blob/master/shapps/auth/ipuser/middle_ipuser.py#L9)
* 最好能加上相关的用户管理界面,如 [这个例子](https://github.com/zhangchunlin/shapps/tree/master/shapps/auth/ipuser_admin)

### 升级支持auth_type以后需要做的数据库迁移操作
假设原来只有一种认证方式为ldap, [其值为"ldap"](https://github.com/zhangchunlin/shapps/blob/master/shapps/auth/ldap/settings.ini), 那么升级到支持多种auth_type以后需要在本地数据库执行如下sql:

```
ALTER TABLE "user"
  ADD COLUMN auth_type VARCHAR(20);
update "user" set auth_type="ldap";
ALTER TABLE "usergroup"
  ADD COLUMN auth_type VARCHAR(20);
update "usergroup" set auth_type="ldap";
```

这样可以加上 auth_type 相关的字段,然后设上值,为之后同时支持多种认证方式做准备
