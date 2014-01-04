# Database and ORM

Uliweb don't bind any ORM, but you can use dispatch, app tech to encapsulate
your own usage of database or ORM. Of cause Uliweb indeed has its own ORM, I
call it **uliorm**, and also provide an orm App, so you can easily use it. But
please remember, uliorm is not forced, and if you don't like it, you don't
need to use it at all. But I want to make it suit for many simple tasks. And
uliorm is based on SQLAlchemy, so you can also use many features from
SQLAlchemy.


## Installation

Because uliorm is built on SQLAlchemy, and it also needs pytz when you want
to process timezone, so you should install them first before you want to use
uliorm. Of cause, Uliweb has also provided such install command for you:


```
uliweb call -a uliweb.contrib.orm install
```

After executing it, it'll automatically install SQLAlchemy and pytz for you.


## ORM Configuration

First, you should add `uliweb.contrib.orm` to `INSTALLED_APPS` in `apps/settings.ini`.
Then, there are several parameters you can set to control the behavior of the ORM.


```
[ORM]
DEBUG_LOG = False
AUTO_CREATE = True
CONNECTION = 'sqlite://'
```

The `DEBUG_LOG` is used to toggle SQLAlchemy log, if set to `True`, when executing
SQL, the SQL statements will be output in log.

The `AUTO_CREATE` is used to enable ORM create tables automatically. If set it to
False, you should create table yourself.

The `CONNECTION` is used to set the connection string. Just follow the SQLAlchemy
format. (You can see [http://www.sqlalchemy.org/docs/05/dbengine.html#create-engine-url-arguments](http://www.sqlalchemy.org/docs/05/dbengine.html#create-engine-url-arguments))

The common format is:


```
driver://username:password@host:port/database
```

There are some examples:


```
#sqlite
sqlite_db = create_engine('sqlite:////absolute/path/to/database.txt')
sqlite_db = create_engine('sqlite:///d:/absolute/path/to/database.txt')
sqlite_db = create_engine('sqlite:///relative/path/to/database.txt')
sqlite_db = create_engine('sqlite://')  # in-memory database
sqlite_db = create_engine('sqlite://:memory:')  # the same

# postgresql
pg_db = create_engine('postgres://scott:tiger@localhost/mydatabase')

# mysql
mysql_db = create_engine('mysql://scott:tiger@localhost/mydatabase')

# oracle
oracle_db = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')

# oracle via TNS name
oracle_db = create_engine('oracle://scott:tiger@tnsname')

# mssql using ODBC datasource names.  PyODBC is the default driver.
mssql_db = create_engine('mssql://mydsn')
mssql_db = create_engine('mssql://scott:tiger@mydsn')

# firebird
firebird_db = create_engine('firebird://scott:tiger@localhost/sometest.gdm')
```

And if you don't like to modify the apps/settings.ini manually, you can
also start development sever via:


```
uliweb runadmin
```

Then in Build page of [http://localhost:8000/admin](http://localhost:8000/admin) to set the settings of ORM App.


## Model Definition

In common, you may create your model in models.py. First you should import from
uliweb.orm, then create your own model and it should inherit from `Model` class.
Then add any fields you want to define. For example:


```
from uliweb.orm import *
import datetime

class Note(Model):
    username = Field(CHAR)
    message = Field(TEXT)
    homepage = Field(str, max_length=128)
    email = Field(str, max_length=128)
    datetime = Field(datetime.datetime, auto_now_add=True)
```


### Table Name

By default, the table name will be the lower string of model class name, so Note
model's table name should be `note`.

And if you want to set it to other table name, you can define a `__tablename__` in
model class. For example:


```
class Note(Model):

    __tableame__ = 't_note'
```


### Tabel Arguments

In SQLAlchemy, when you creating a Table, you may pass some extra arguments, just
like: mysql_engine, etc. So you could define `__table_args__` in Model, for example:


```
class Todo(Model):
    __table_args__ = dict(mysql_charset='utf8')
```


### 3.3\ \ \ OnInit Method

uliorm also enable you do some initialization works before doing the creation
of the table. Just write a class method OnInit, for example:

```
class Todo(Model):
    @classmethod
    def OnInit(cls):
        Index('my_indx', cls.c.title, cls.c.owner, unique=True)
```

For now, I only test `Index`, and you can also import it from `uliweb.orm`.


### Property Definition

uliorm define a model field as Property, but you can also use field concept,
it's no problem.

uliorm can define property of a model in two ways. One is very like GAE data
store, just `*Property` class. The other is just using Field() function.

Below are real properties defined in Uliewb ORM:


```
'BlobProperty', 'BooleanProperty', 'DateProperty', 'DateTimeProperty',
'TimeProperty', 'DecimalProperty', 'FloatProperty',
'IntegerProperty', 'Property', 'StringProperty', 'CharProperty',
'TextProperty', 'UnicodeProperty', 'FileProperty'
```

But you may think they are not easy to remember, so you can use the second way
to define a property. Just using `Field()`.

For Field() function, it'll receive a Python date type or some special SQLAlchemy
type, and convert it to a real Property class and then create an instance of it.

The mapping of Python data type and Property are:


```
str:StringProperty,
CHAR:CharProperty,
unicode: UnicodeProperty,
TEXT:TextProperty,
BLOB:BlobProperty,
FILE:FileProperty
int:IntegerProperty,
float:FloatProperty,
bool:BooleanProperty,
datetime.datetime:DateTimeProperty,
datetime.date:DateProperty,
datetime.time:TimeProperty,
decimal.Decimal:DecimalProperty,
DECIMAL:DecimalProperty,
```

So define a property to a model just like define a class attribute to a class.
The name of property will be the attribute name of the model class, and you
can use it to get and set relative table field. Every property will be an
instance of `*Peroperty` class.


### ID Property

By default, uliorm will automatically create an `ID` property for you, and you
don't need to define it in model.


### Property Constuctor

Property is the Base class of all other properties. So many of its attributes and
methods will be used in dirived class:


```
Property(verbose_name=None, name=None, default=None, required=False, validators=None, choices=None, max_length=None)
```


verbose_name --
    can be used as prompt message of a property

name --
    name will be the field name of the relative table, if not provided it'll
    the save as property name.

default --
    default value of this property.

required --
    if this property is needed.

validators --
    when you set a value to this property, uliorm will validate the value
    according this parameter. It should be a function list, the function should
    be:

    ```
    def validator(data):
        xxx
        if error:
            raise BadValueError, message
    ```

    If the validation is failed, the function should raise an Exception. If
    it's successful, you don't need to anything.

choices --
    Used for validation, and testing if the value is in the choices.

max_length --
    Maxmize length of a property, this parameter is only useful for `StringProperty`,
    `CharProperty`. Default value is `30`.

index --
    If this property will be index column. Default is False.

unique --
    If this property will be unique. Default is False.

nullable --
    If this property value can be `NULL`. Default is True.



### CharProperty

This property will be mapped to `CHAR` type. You should pass a `max_length` to it.
If you pass a unicode to it, it'll be converted to default encoding(utf-8).


### StringProperty

This property will be mapped to `VARCHAR` type. You should pass a `max_length` to it.
If you pass a unicode to it, it'll be converted to default encoding(utf-8).


### TextProperty

This property will be mapped to `TEXT` type.


### UnicodeProperty

This property will be mapped to `VARCHAR` type.


### BlobProperty

This property will be mapped to `BLOB` type.


### DateProperty DateTimeProperty TimeProperty

These properties are used for data and time type. They have three more parameters:


auto_now --
    When you saving the object, this property will be automatically updated
    by current time.

auto_add_now --
    Only used when create new object, and this property will be the current
    time.

format --
    If you pass a string value to this property, and this parameter will
    be used to convert string value to datetime.



### BooleanProperty

This property will be mapped to `Boolean` type.


### DecimalProperty

This property will be mapped to `Numric` type. It have two more parameters:


precision --
    Default is 10.

scale --
    Default is 2.



### FloatProperty

This property will be mapped to `Float` type. It have one special parameter:


precision --
    Default is 10.


If you are passing `max_length` but no `precision`, the `precision` will be the same
value of `max_length`.


### IntegerProperty

This property will be mapped to `Integer` type.


### Common Attributes of the Model


table --
    An uliorm model will be mapped to an Table object of SQLAlchemy, and `table`
    will be the underlying Table instance of the model. So you can use this
    attribute do table level operation.

c --
    A model columns set. It's the same as table.c attribute.

properties --
    All properties defined in model.

metadata --
    metadata instance bound.



## Relation Definition

uliorm also supports relation definition: OneToOne, ManyToOne, ManyToMany.


### One to One

"System Message: WARNING/2 (D:\project\mywork\uliweb-doc\docs\en\orm.rst:, line 351)"
Cannot analyze code. No Pygments lexer found for "python+console".


```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = OneToOne(Test)
...     name = Field(str)
```

You can use OneToOne to reference other model. For example:

"System Message: WARNING/2 (D:\project\mywork\uliweb-doc\docs\en\orm.rst:, line 362)"
Cannot analyze code. No Pygments lexer found for "python+console".


```
>>> a1 = Test(username='limodou')
>>> a1.save()
True
>>> b1 = Test1(name='user', test=a1)
>>> b1.save()
True
>>> a1
<Test {'username':'limodou','year':0,'id':1}>
>>> a1.test1
<Test1 {'test':<Test {'username':'limodou','year':0,'id':1}>,'name':'user','id':1}>
>>> b1.test
<Test {'username':'limodou','year':0,'id':1}>
```


### Many to One

"System Message: WARNING/2 (D:\project\mywork\uliweb-doc\docs\en\orm.rst:, line 380)"
Cannot analyze code. No Pygments lexer found for "python+console".


```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = Reference(Test, collection_name='tttt')
...     name = Field(str)
>>> a1 = Test(username='limodou1')
>>> a1.save()
True
>>> b1 = Test1(name='user', test=a1)
>>> b1.save()
True
>>> b2 = Test1(name='aaaa', test=a1)
>>> b2.save()
True
>>> a1
<Test {'username':'limodou1','year':0,'id':1}>
>>> list(a1.tttt.all())[0]   #here we use tttt but not test1_set
<Test1 {'test':<Test {'username':'limodou1','year':0,'id':1}>,'name':'user','id':1}>
>>> a1.tttt.count()
2
```

You should use `Reference` to reference a many to one relation. And `Reference` has
a `collection_name` parameter, if you don't give it, the referenced model will use
object_test.test1_set to get reversed data set. And if there are two and above
relation on same model, you need to define different `collection_name` for each
relation. So `a1` could use `a1.tttt` to get the reversed data set relation to it.
For now, uliorm will not create Foreign Key constrain, because when creating
a table, if there is a foreign key constrain, the foreign table should be created
first, then this table. And it has some difficult for distributed apps.

How to think about many to one relation? Think about Test:Test1 is 1:n relation,
that means one Test object could have one or more Test1 objects. So you should
define `Reference` in Test1 model.

And if you want to reference one model to itself, you can use: SelfReference, for
example:


```
>>> class User(Model):
...     username = Field(unicode)
...     parent = SelfReference(collection_name='children')
```


### Many to Many

"System Message: WARNING/2 (D:\project\mywork\uliweb-doc\docs\en\orm.rst:, line 428)"
Cannot analyze code. No Pygments lexer found for "python+console".


```
>>> class User(Model):
...     username = Field(CHAR, max_length=20)
...     year = Field(int)
>>> class Group(Model):
...     name = Field(str, max_length=20)
...     users = ManyToMany(User)
>>> a = User(username='limodou', year=5)
>>> a.save()
True
>>> b = User(username='user', year=10)
>>> b.save()
True
>>> c = User(username='abc', year=20)
>>> c.save()
True
>>> g1 = Group(name='python')
>>> g1.save()
True
>>> g2 = Group(name='perl')
>>> g2.save()
True
>>> g3 = Group(name='java')
>>> g3.save()
True
>>> g1.users.add(a)
>>> g1.users.add(b)
```

You can use `ManyToMany` to reference a many to many relation. uliorm will
work like Django, it'll create the third table automatically, for example, the
third table of above example will be: group_user_users, it's the two table names
(user and group) and ManyToMany property name (users). The table structure of
the third table will be:


```
CREATE TABLE group_user_users (
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (group_id, user_id)
)
```


## Operation

There are different levels of ORM operations: instance level, model level,
relation level.


Instance Level --
    It'll only affect the instance itself, you can: create, get, delete, update,
    save it.

Model Level --
    It'll affect the model or table level, so you can operate a table instead of
    one instance. You can: query(all, filter), count, order_by, delete, distinct,
    limit, offset, etc.

Relation Level --
    Some relation property will return an `Result` sets, and these result sets
    work just like table level operations but with some different. The relations
    inludes: `_ReverseReferenceProperty`, `_ManyToManyReverseReferenceProperty`.
    You should not need to use these properties directly, they will be created
    automatically when you reference ManyToOne and ManyToMany result reversed.
    You'll see more details later.



### Instance Level


#### Create an Instance

Say there is a User model, the class definition is:

```
class User(Model):
    username = Field(CHAR, max_length=20)
    year = Field(int)
```

So if you want to create an instance of User model, just do like this:

```
user = User(username='limodou', year=36)
```

But it'll not be saved in database, it just creates an instance, you need call
`put` or `save` to save it:

```
user.save()
#or
user.put()
```

#### Get an Instance


```
user = User.get(5)
user = User.get(User.c.id==5)
```

If you want to get an instance from a model, you should call `get` method of a model.
You can pass a integer or a query condition. So `User.get(5)` will be exact:

```
User.get(User.c.id==5)
```

The query condition syntax is exact SQLAlchemy query syntax, so you can see more
detail at: [http://www.sqlalchemy.org/docs/05/sqlexpression.html](http://www.sqlalchemy.org/docs/05/sqlexpression.html)


#### Delete an instance


```
user = User.get(5)
user.delete()
```


#### Update an instance


```
user = User.get(5)
user.uesrname = 'user'
user.save()
```


#### Other APIs


to_dict([*fields]) --
    Dumps instance to a dict object. If there is no `fields` parameter, it'll dump
    all fields of the instance. And you can pass fields which you want to dumps,
    for example:

    ```
    a = User.get(1)
    a.to_dict() #this will dump all fields
    a.to_dict('name', 'age')    #this will only dump 'name' and 'age' fields
    ```


### Model Level


#### Query

There are two query methods: all() and filter(). all() and filter() will both
return an `Result` object, and all() will return all records of a model, but filter()
will only return records of a model which match the condition passed to filter().

For example:

```
User.all()
User.filter(User.c.year > 18)
```

#### Result Object

When you executing all() or filter(), it'll return a Result object, and you can
use it for further opration, just like: filter, count, delete, order_by, limit,
offset, etc. And other operation will also return Result object, for example, when
you access the reversed relation property. Result has many methods, and you can
combine them one by one, for example:

```
User.all().filter(User.c.year>18).count()
```

all() --
    It'll return Result object itself.

filter(condition) --
    It'll add more condition to the result set.

count() --
    It'll return the count number of current condition.

delete() --
    It'll delete all the records which matched the condition.

order_by(*field) --
    It'll add an ORDER_BY clause to the select. For example:

    ```
    result.order_by(User.c.year.desc()).order_by(User.c.username.asc())
    #or
    result.order_by(User.c.year.desc(), User.c.username.asc())
    ```


limit(n) --
    It'll add an LIMIT clause to the select. n should be an integer.

offset(n) --
    It'll add an OFFSET clause to the select. n should be an integer.

values(*fields) --
    It'll return an iteration of records list, and each row will only contain
    the values of the listed fields. It's different from the common query result(
    common query result will be the model objects interation):

    ```
    >>> print a1.tttt.all().values(Test1.c.name, Test1.c.year)
    [(u'user', 5), (u'aaaa', 10)]
    ```


values_one(*fields) --
    Just like values() but only return one record. If no record, then return None.

one() --
    Only return the lastest one record, if no records, then return None.



#### Delete objects

For common usage, you should use all() or filter() first, then use the returned
Result object to delete objects. But you can still use `remove()` to delete objects
without calling all() or filter() first.


```
User.delete(User.c.year<18)
```


#### Count objects

Just like `remove()`, you can still use `count()` to count the objects without
calling all() or filter() first.


```
User.count(User.c.year<18)
```


#### Other APIs


bind(metadata=None, auto_create=False) --
    Binds current class to a metadata. If `auto_create` if `True`, then it'll automatically
    create the table.

create() --
    Create table, and will check if the table is existed first.



### Relation Level


#### One to One

There is no magic for one to one relation, for example:


```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = OneToOne(Test)
...     name = Field(str)
>>> a = Test(username='limodou', year=36).save()
>>> b = Test1(name='user', test=a).save()
>>> b.test
<Test {'username':'limodou', 'year':36}>
```

So you can use `b.test` just like `a` object.


#### Many to One

```
>>> class Test(Model):
...     username = Field(str)
...     year = Field(int)
>>> class Test1(Model):
...     test = Reference(Test, collection_name='tttt')
...     name = Field(str)
>>> a = Test(username='limodou').save()
>>> b = Test1(name='user', test=a).save()
>>> c = Test1(name='aaaa', test=a).save()
```

According above code, Test:Test1 is a 1:n relation. And `b.test` will be the object
`a`. But `a.tttt` will be the reversed query set, it may not be only one objects.
So `a.tttt` will return a Result object. And this Result object will be bound to
Test1 model, so the all() and filter() of the Result will return only Test1 objects.
More details you should see `Result` description previous.


#### Many to Many

```
>>> class User(Model):
...     username = Field(CHAR, max_length=20)
...     year = Field(int)
>>> class Group(Model):
...     name = Field(str, max_length=20)
...     users = ManyToMany(User)
>>> a = User(username='limodou', year=5).save()
>>> b = User(username='user', year=10).save()
>>> c = User(username='abc', year=20).save()
>>> g1 = Group(name='python').save()
>>> g2 = Group(name='perl').save()
>>> g3 = Group(name='java').save()
>>> g1.users.add(a)
>>> g1.users.add(b)
```

So when you access `a.group_set``(because you didn't define collection_name in ManyToMany
property) or ``g1.users` it'll return a ManyResult object.


#### ManyResult

ManyResult is very like Result. But it has other methods:


add(*objects) --
    This method will add new relations to the third table.

clear() --
    Clearing all relations from the third table.

delete(*objects) --
    Delete the relations according to objects.



## Transacation

If you are using uliorm, you can install `middle_transaction.TransactionMiddle`
to `MIDDLEWARE_CLASSES` in `settings.ini`. So when the request is coming, the
transaction is began, and when the response is returned, the transaction will be committed.
And if there are exceptions, the transaction will be rollbacked.

If you want to control the transacation manually, you could get the connection
object first:


```
db = get_connection()
```

Then there are many functions you can use:


```
db.begin()      #start a transacation
db.commit()     #commit
db.rollback()   #rollback
```


## Model Register & Reference

Uliweb also provides a new way to deal with model usage.


1. When you import a model class, it'll be automatically register to a global
    variable, and you can get back the model later according the tablename.
1. You can also register a model in string format, more details see set_model
    explanation.
1. Call get_model(tablename) to get a real model class instance.
1. Reference, ManyToMany can also accept a string(tablename) parameter instead
    of a model class.
1. Models can be configured in settings.ini, for examle:

    ```
    [MODELS]
    user = 'uliweb.contrib.auth.models.User'
    ```

    For the key is the tablename, and the value is the string format of the
    model also with its module name which belongs.

What's the use of it? Think about you have several apps, and each app has its
own models.py, and one app may need to reference some models from others. So
the common situation, you may import the models from other models.py. This is
no problem at all. But what will happen when you want to change the referenced
models, you may think out that "I can change them directly". But if these models
are not maintained by you, so change them may not be a good appoach. With
referencing models by string format tablename, you can easily replace one app
with a new app, and implement new models in new app. Just define MODELS mapping
in new app's settings.ini, then use string tablename in Reference, ManyToMany or
get the model via calling get_model(tablename).

Of cause this appoach is optional, just when you want to make your app is more
easy to be replaced.


## How to use ORM in your program


## Mysql Issues


### Encoding Setting

uliorm will default use utf8 encoding when creating the table in Mysql even
if the default charset of mysql is not utf8. So that if you are using Mysql
you should check if the default charset of your sechma is utf8 encoding, if not
you should add charset in connection string, just like:


```
[ORM]
CONNECTION = 'mysql://root:limodou@localhost/new?charset=utf8'
```

The charset=utf8 is needed when the default charset of server is not utf8,
otherwise you don't need to set it.


## Module Level API


set_auto_create(flag) --
    Set auto create table flag. The flag default is True.

set_debug_query(flag) --
    Set debug mode. If set, the SQL statements will be ouputed in logs.
    If you've gotten a db instance from get_connection(), you can also
    simply set `db.echo = True` to enable the debug mode.

set_encoding(encoding) --
    Set default encoding. Default is 'utf-8'.

get_connection(connection='', metadata=_default_metadata, default=True, debug=None, **args) --
    Establish a connection to database, and return the connection object.

set_model(model, tablename=None, created=None) --
    Register a model or model string. For example:

    ```
    set_model(User)
    set_model('uliweb.contrib.models.User', 'users')
    ```

    If you pass a model instance to set_model, you don't need to pass it a
    tablename parameter. But if you pass a string as model parameter to it,
    you should also need to pass a tablename. And created parameter used for
    indicate that if the table has been created already. So for common usage,
    you don't need to care about this parameter.

get_model(model) --
    Get the real model object according to the model parameter. And the model
    parameter could be a real model instance, in this case, the model will be
    directly returned. And the model parameter could be tablename, so uliorm
    will use it to find the registered value, and if the value is also a model
    instance, then just return it. But if the value is a string, then import it
    according the value.



## Testing Code

There are some testing code in uliweb/test/test_orm.py, so you can see some examples
of how to use uliorm.

