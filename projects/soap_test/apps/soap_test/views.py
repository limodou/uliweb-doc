from uliweb import decorators
from uliweb.contrib.soap import Date, DateTime, Decimal

@decorators.soap('hello', returns={'a':str}, args={'a':str})
def hello(a):
    return 'Hello:' + a
