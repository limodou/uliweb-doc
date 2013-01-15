# rbac(权限控制)

RBAC是基于角色控制的英文简写。在Uliweb中，提供了一个rbac的模块，它将提供一个基本的Role(角色表)和Permission(权限表)，以及它们之间的关系。Role和Permission之间是多对多的关系。同时Role有指向User表的引用。


## 原理

为了保证操作的安全性，我们通常会在某些重要的操作上设置权限来控制，比如重要的链接或按钮，重要的 URL 上，前者相当于在界面上进行控制，后者相当于在服务上进行控制。在通常情况下，我们需要在展示和后台处理上都添加权限控制，以便防止用户通过程序的方式来进行攻击。

这里权限说得还是有些笼统，细分起来，我们可以通过角色或权限来控制。比如某个菜单，我们允许某个角色的用户可以访问，也可以设计成具有某种权限的角色可以访问。到底用哪个，这个取决于你的需求和设计。

在Uliweb中，角色、权限和用户之间的关系如下:


```
Permission m:n Role m:n User
```

可以看出， Permission 和 User 之间没有直接的关系。在简单情况下可以只使用角色来判断，如只区分超级用户、登录用户和匿名用户可能就足够了。因此 Permission 可能就不需要使用。在复杂情况下，使用 Permission 可能更方便，配置起来也灵活。


## 只使用auth app来判断基本用户角色

这里基本用户角色我定义为：超级用户、登录用户和匿名用户。

如果我们不使用 rbac app ，只是使用 auth app 的话，在它所提供的 User 表中已经有一些信息可以用来进行基本判断，同时结合 middle_auth ，将可以直接区分：超级用户、登录用户和匿名用户。主要分两种情况：


1. 判断当前用户，使用request.user对象，可以区分：超级用户、登录用户和匿名用户

    超级用户 --
    if request.user and request.user.is_superuser

    普通用户 --
    if request.user and not request.user.is_superuser

    匿名用户 --
    if not request.user


1. 判断指定用户，需要从 User 表中动态获取，然后利用是否存在和 is_superuser 字段来判断是否为普通用户或超级用户，这里无法判断匿名用户

    超级用户 --
    user = User.get(User.c.username == username)
        if user and user.is_superuser

    普通用户 --
    user = User.get(User.c.username == username)
        if user and not user.is_superuser



在最简单情况下，你可能只使用auth就足够了，那么我们看看rbac会带给我们什么呢？


## rbac app的安装

首先是在settings.ini中安装app，如:


```
INSTALLED_APPS = [
#...
'uliweb.contrib.rbac',
#...
]
```

然后需要在命令行执行:


```
uliweb syncdb #用来创建相关的表
uliweb dbinit uliweb.contrib.rbac #初始化相应的权限数据
```

rbac 允许将初始的 Role, Permission 和相应的关系等写在 settings.ini 中，然后通过 dbinit 命令来进行数据装入。并且角色和权限的装入可以多次执行，它只会覆盖，不删除。


## rbac的配置

用户可以把 rbac 相关的信息配置在 settings.ini 中，然后通过 dbinituliweb.contrib.rbac 将相关的数据导入进数据库中，主要可以使用的配置如下：


### ROLES

ROLES用来配置角色信息，如:


```
[ROLES]
superuser = _('Super User'), 'uliweb.contrib.rbac.superuser', True
anonymous = _('Anonymous User'), 'uliweb.contrib.rbac.anonymous', True
trusted = _('Trusted User'), 'uliweb.contrib.rbac.trusted', True
```

上述是示例是由rbac/settings.ini缺省提供的，分别对应三种不同的角色:


superuser --
    超级用户

anonymous --
    匿名用户

trusted --
    登录用户


ROLES每项的定义格式如:


```
role_name = display_name [, 'role_function_path' [, reserved_flag]]
```


role_name --
    是角色的名字，应该为英文标识符。

display_name --
    是角色对应的显示名，可以是中文

role_function_path --
    是角色对应的判断函数路径，写法是模块路径 + 方法名。 rbac 会自动导入相关的函数进行角色的判断。这是一个可选项，也可以置为空。

reserved_flag --
    是否保留的标志。缺省为 False ，这也是一个可选项。它的主要做用是用户可以根据它来区分当前的角色是否是保留的，从而可以进行不同的处理。 rbac 本身不对它做处理，而是将处理留给用户来使用。比如，对于保留的权限不允许删除。至于是否使用，可由用户自行决定。


关于如何判断一个用户是否某个角色，下面会详细解释，这里先不细说。


### PERMISSIONS

PERMISSIONS用来定义权限信息，在rbac/settings.ini中没有缺省权限，示例如下:


```
[PERMISSIONS]
write = _('Write Permission')
```

它的定义很简单，就是权限名和权限名的显示文本。


### ROLES_PERMISSIONS

ROLES_PERMISSIONS用来定义角色和权限之间的关系，如:


```
[ROLES_PERMISSIONS]
permission_name = role
permission_name = role1, role2, ...
permission_name = (role1, role_prop1),(role2, role_prop2)
```

上面是一个示例，有几种定义形式， key 为权限名， value 为角色的列表，可以是单个角色名，也可以是多个角色名，值为 tuple 或 list 。也可以是 tuple 形式的列表。如果是最后一种，则第一个元素是角色名，第二个是这个角色对应权限的附加属性。


{% alert class=info %}
什么是附加属性？通常的权限与角色关系，我们可能只关心一个角色有什么样的权限就够了。但是对于特殊的场合，如审批处理，不同的角色可能审批的额度不同，但是对于只使用角色与权限关系的定位方式就无法定义不同的额度值来，因此在 uliweb 设计 rbac 时，在关系表中还添加了一个附加的 props 字段，利用它可以定义一些特殊的值。不过，目前没有更多对它的处理， rbac 只是把它定义成为了 PICKLE 字段，用户可以存储任意的简单数据类型，如： int, str, dict, list 等。这只是留作以后扩展使用的。

{% endalert %}

{% alert class=info %}
在 settings.ini 中定义的上述内容，应该只是做为初始化数据时使用，在运行时不应直接使用 settings.ini 中的数据，而是通过 rbac 提供的方法或 Model 来处理。

{% endalert %}

## rbac使用的表结构说明


### Permission

权限表


```
class Permission(Model):
    name = Field(str, max_length=80, required=True)
    description = Field(str, max_length=255)
    props = Field(PICKLE)
```

权限表的字段有:


name --
    权限名称，取值应是英文标识符

description --
    权限描述

props --
    和前面讲的附加属性有关系。在 rbac 的设计中， Permission 中的 props 可以视为附加属性的模板和缺省值。即这个权限在关联到角色的时候，应该有哪些属性，它们的缺省值是什么。而在角色与权限的关系表中定义的是某个角色的真正取值。



### Role

角色表


```
class Role(Model):
    name = Field(str, max_length=80, required=True)
    description = Field(str, max_length=255)
    reserve = Field(bool)
    users = ManyToMany('user', collection_name='user_roles')
    permissions = ManyToMany('permission', through='role_perm_rel',
        collection_name='perm_roles')
```

角色表的字段有:


name --
    角色的名字，取值应是英文标识符

description --
    角色的说明

reserve --
    是否保留，留给用户使用，比如在删除时，对于保留的角色要不要有特殊处理

users --
    当前角色所绑定的用户

permissions --
    当前角色所绑定的权限



### Role_Perm_Rel

角色和权限的关系表


```
class Role_Perm_Rel(Model):
    role = Reference('role')
    permission = Reference('permission')
    props = Field(PICKLE)
```

角色和权限的关系表的字段有:


role --
    角色id

permission --
    权限id

props --
    某个角色对应某个权限的附加属性



## role的判断

对于某一个角色，rbac支持不同的判断方式，主要有:


1. 通过role对应的用户来判断。即通过Role表的users字段来判断。
1. 通过 role 判断方法来判断。即你可以提供一个方法，并将其按前面 ROLES 配置的说明中描述所讲的那样进行配置，这样在判断一个角色时，会使用这个方法对传入的用户进行判断。

对于 rbac 提供的缺省的 superuser, trusted, anonymous 就是采用这种方式来判断的。如果对于一个角色，两种方法都提供了，则会先使用方法进行判断，如果不满足，再按用户进行判断，直到都不满足条件。其中只要有一个满足条件，就认为用户拥有某个用户的身份。


## 动态角色和静态角色

在判断一个用户是否具有某种角色时，可能有两种情况：

一种是只根据用户信息本身就可以判断出用户是否且有某种角色，如 superuser 角色的判断，就可以根据 user 对象的 is_superuser 来判断，它不需要再依赖其它的信息。uliweb 称之为 **静态角色** 。

另一种情况就是，除了有用户信息外，还需要知道当前所访问的对象和用户之间的关系，如论坛的某个版块的版主，必须是和某个版块关联时才知道，只有用户信息是不够的，象这种只能在运行时，根据用户与访问对象的关系才能判断出来的角色， uliweb 称之为**动态角色**.


## role判断函数的编写

写法如下:


```
def superuser(user):
    return user and user.is_superuser

#or

def manager(user, id):
    obj = Model.get(id)
    return obj.user.has(user)
```

上面是两种写法，分别对应于静态角色和动态角色的判断。

写好之后，要按ROLES的配置要求写入settings.ini中。


## 通用角色、权限判断的方法

rbac提供两类角色和权限判断的方法，一种是通过function或functions进行函数调用的方式:


has_role(user, *role_names, **kwargs) --
    用户要传入 user 对象和角色的名字，角色名可以是多个。同时如果存在动态角色，还要根据需要传入动态角色判断方法所需要的其它的参数。

has_permission(user, *permission_names, **kwargs) --
    用户要传入 user 对象和权限的名字，权限名可以是多个。同时如果有动态角色，还要传入动态角色判断方法所需要的其它的参数。

    {% alert class=info %}
    为什么判断权限有可能还需要传入动态角色所需要的参数呢？因为，在has_permission 中是根据遍历权限所对应的所有角色，检查用户是否拥有其中某个角色来处理的。
    {% endalert %}


以上两个方法可以在view或模块中进行使用。简单的方法通过:


```
from uliweb import functions

def index():
    if functions.has_role(request.user, 'superuser'):
        pass

#or

from uliweb import function

def index():
    if function('has_role')(request.user, 'superuser'):
        pass
```

同时为了方便使用，rbac还提供了decorator方法，分别为:


check_role(*roles, **args_map) --
    它需要传入角色名，可以是多个。其中 args_map 是一个将 view 函数中的参数映射为动态角色所需要的参数。当然它只是在有动态角色参数的时候才需要使用。并且它有一个限制就是：所要映射的参数需要在 view 函数的参数中存在。例如

    ```
    def topic_manager(user, tid):
        """
        topic_manager是用来判断一个用户是否是某个主题的管理员，它需要一个tid
        的参数
        """
        pass
    
    
    from uliweb import decorators
    
    @decorators.check_role('topic_manager', tid=topic_id)
    @expose('/forum/topic/<topic_id>')
    def topic_view(topic_id):
        pass
    ```

    上面的例子定义了一个主题管理者 (topic_manager) 的角色，它需要一个动态的角色参数 tid 。然后在 topic_view 的定义中，我们想要判断某个用户是否是某个topic 的管理员，但是 topic_view 的参数是 topic_id ，所以我们通过映射的方法将 :tipic_id 映射为 tid 。
    使用 decorator 的形式，并不需要传入 user 对象，因为它会使用 request.user 。因此，它主要是用来处理 view 函数。在其它复杂的场合下，可能使用 has_role 或 has_permission 会更方便。

check_permission(*permissions, **args_map) --
    它这decorator和check_role类似，它是用来判断当前用户是否拥有某种权限。


当使用 decorator 方法时，如果验证失败，将会自动调用 error 函数显示一个出错页面。 error 会缺省调用 error.html 模板，内容为


```
{{extend "layout.html"}}

{{block content}}
<div class="content">
    <div class="box center col_10">
        <h2>出错啦!</h2>
        <div class="box-body">
            <p>{{=message}}</p>
            <p><a href="javascript:history.back();">点击这里回退</a></p>
        </div>
    </div>
</div>
{{end}}
```

这里主要是要有一个{{=message}}的标签。


## 如何将角色与用户关联

经过上面的学习，你可能已经了解到了如何写一个角色判断函数，并且将其配置到某个角色上。但是，如何实现用户与角色的关联呢？这个工作是由用户自已来完成的，在 plugs项目中已经有一个简单的实现，它主要是提供一个角色和权限的管理界面，并且可以关联用户和角色，角色和权限。而 rbac 只提供基本功能框架，不提供相应的管理界面。


## 小结

上面的内容有些多，下面小结一下简单的使用流程:


1. 安装uliweb.contrib.rbac
1. 执行uliweb syncdb创建相关的表
1. 如果有自定义的角色，权限，并且希望通过命令行导入；或者角色的判断是通过函数实现的，则要在 settings.ini 中进行配置
1. 执行uliweb dbinit uliweb.contrib.rbac来装入数据
1. 在程序中调用 has_role, has_permission, check_role, check_permission 等方法检查用户权限
1. 使用plugs/rbac_main或用户自行开发的角色、权限管理模块来管理角色或权限

