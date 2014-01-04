# Extending Uliweb

A web framework might fall short to anticipate all your development needs.
Although Uliweb is no exemption in this respect, it strives to provide the most
possible amount of flexibility and extensibility.


## 1\ \ \ Dispatch System

Uliweb ships with a dispatch module, it's in uliweb/core folder.


### 1.1\ \ \ Dispatch units

Uliweb provides a simple Dispatch system that consists of three units:


* Dispatch point
* Receiver function
* Collection system


### 1.2\ \ \ Dispatch points

An Dispatch point will define the place where the dispatcher want to call
its associated receiver functions, and it'll pass the auguments to those
receiver functions. A dispatch point will looks like:


```
dispatch.call(sender, topic, signal=None, *args, **kwargs)
```

or


```
ret = dispatch.get(sender, topic, signal=None, *args, **kwargs)
```

You can see there are two arguments must be passed:


* `sender`
    It just looks like the name.
* `topic`
    Each dispatch has an topic, so that only the receiver functions which
    associated with this topic will be called. So different dispatch point
    can send the same topic.

And the `signal` is optional. If this argument is not `None`, then only the
receiver functions which the topic and the signal are all matched will be called.
If the value of `signal` argument is `None`, then all receiver functions which
as soon as the topic is matched will be called.

Except for above three arguments, you can also pass other arguments, and you
should ensure the receiver functions must match with them.

When you run a dispatch point(It's just a common function invoding), dispatch
system will find all matched receiver functions according the topic and optional
signal, and call them one by one, according the order specified in definition of
receiver function. Why there are two kinds of invoking functions? Because:


* `call`
    will invoke matched receiver functions one by one, and you can't interrupt it
    inn the middle of the execution, and it won't return a value(or it'll just return
    None).
* `get`
    will invoke just like `call`, but if one receiver function returns a value
    is not None, the execution will not continue, and return this value immediately.

So the execution of a dispatch point just like a chain, and you can use different
methods to affect its execution.


{% alert class=info %}
There are two more functions except for `call` and `get`, they are `call_once`
and `get_onec`. You can guess from their names, they could be called really
only once, and if you call them more than one time, for `call_once` will not
invoke again just returned, and `get_once` will only return the first returned
value.

{% endalert %}


### 1.3\ \ \ Receiver functions

It's a function will be used for processing special topic and optional signal.
The signature of a receiver function will look like:


```
def receiver(sender, topic, *args, **kwargs)
```

So, receiver functions are very common.


### 1.4\ \ \ Collection system

Collection system is used to collect all of avaible receiver functions, so that
when executing a dispatch point, it can find all associated receiver functions.
So there are two things you need to do after defining the receiver functions:


1. Call dispatch.bind to receiver functions, for example:

    ```
    from uliweb.core.dispatch import bind
    
    @bind('test_point')
    def receiver():
        ...
    ```

1. Put the code to the right place, so that uliweb can import them, and calling
    the bind function. When Uliweb startup, it'll try to import all `start.py`
    from every available app, so you can put the code to `__init__.py` or `start.py`
    of each app folder.

The signature of the `bind` function is:


```
def bind(topic, signal=None, kind=MIDDLE, nice=-1)
```


* `topic`
    which you want to bind to
* `signal`
    used to match with the dispatch point signal argument. And if the receiver
    function has no signal argument, this argument will be removed. On the
    contrary, it'll be passed to the receiver function.

    {% alert class=info %}
    Here signal maybe a tuple or a list, so that one receiver function can
    match multiple signals.
    {% endalert %}

* `kind`
    There are two types of indicating the priority of a receiver function. And
    priority is higher(the number is lower), the execution order is in front.
    So 0 will highter than 100. And kind has three levels:HIGH, MIDDLE, LOW, and
    they are mapping to different priority number: HIGH=100, MIDDLE=500, LOW=900.
    And default is MIDDLE.
* `nice`
    You should not use kind and nice at the same time. And `nice` is used for
    accurately setting the priority.

When executing a dispatch point, it'll sort all associated receiver functions
according their priority. So if your receiver functions need to run in certain
order, you'll need to set `kind` or `nice` argument.


### 1.5\ \ \ Predefined dispatch points


#### 1.5.1\ \ \ uliweb.core.SimpleFrame


* **dispatch.call(application, 'startup_installed')**
    Dispatcher class initialization, will only run once for class
* **dispatch.call(application, 'startup')**
    Dispatcher has already startuped, will be executed when creating every Dispatcher
    instance.
* **dispatch.call(application, 'prepare_view_env', Dispatcher.env)**
    Used for prepare global view and template execution environment. All objects in env can
    be used in any view function directly.

