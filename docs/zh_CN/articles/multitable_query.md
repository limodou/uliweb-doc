# Uliorm多表关联查询

## 简单例子

models.py:

```
class ModelA(Model):
    info = Field(str)

class ModelB(Model):
    a = Reference('modela')
    deleted = Field(bool)
```

dbinit.py:

```
ModelA = get_model('modela')
ModelB = get_model('modelb')

if ModelA.all().count()==0:
    a = ModelA(info="a")
    a.save()
    b = ModelB(a=a.id,deleted=False)
    b.save()

    a = ModelA(info="a")
    a.save()
    b = ModelB(a=a.id,deleted=True)
    b.save()

    a = ModelA(info="b")
    a.save()
    b = ModelB(a=a.id,deleted=False)
    b.save()

    a = ModelA(info="b")
    a.save()
    b = ModelB(a=a.id,deleted=True)
    b.save()


print "---ModelB filter:"
for i in ModelB.filter(ModelB.c.a==ModelA.c.id,ModelA.c.info=='a',ModelB.c.deleted==True):
    print i.to_dict()

print "---ModelA filter:"
for i in ModelA.filter(ModelB.c.a==ModelA.c.id,ModelA.c.info=='a',ModelB.c.deleted==True):
    print i.to_dict()
```

运行结果:

```
$ uliweb dbinit
---ModelB filter:
{'a': 2, 'deleted': True, 'id': 2}
---ModelA filter:
{'info': 'a', 'id': 2}
```

## 较为复杂的例子

例如有一个部门的表定义如下:

```
#部门
class Department(Model):
    #部门名称
    name = Field(str, nullable=False)
    #对应的usergroup
    usergroups = ManyToMany('usergroup', collection_name='usergroup_department')

```

那么和 uliweb.contrib.auth 里定义的 user 和 usergroup 表一起配合起来判断某个用户属于哪个部门可以这么写:

```
def user_department(user=None):
    if not user:
        user = request.user
    if not user:
        return None
    Department = get_model("department")
    User = get_model("user")
    UserGroup = get_model("usergroup")
    d = Department.filter(Department.c.id == Department.usergroups.table.c.department_id,
        Department.usergroups.table.c.usergroup_id == UserGroup.users.table.c.usergroup_id,
        UserGroup.users.table.c.user_id==user.id
    ).one()
    return d
```
