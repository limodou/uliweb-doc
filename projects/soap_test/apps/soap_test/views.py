#coding=utf-8
from uliweb import decorators
from uliweb.contrib.soap import Date, DateTime, Decimal

@decorators.soap('hello', returns={}, args={'a':str})
def hello(a):
    return

@decorators.soap(returns={'a':str})
def echo(request):
    return request.value

@decorators.soap(returns={'a':int}, args={'a':[int]})
def add(a):
    t = 0
    for x in a:
        t += x['int']
    return t

@decorators.soap(returns={'a':[str]}, args={'a':[str]})
def string(a):
    t = []
    for i, x in enumerate(a):
        t.append(x['string'] + u'中文')
    return t

@decorators.soap('Adder', returns={'AddResult': {'ab': int, 'dd': str, 'dt':Date } }, 
        args={'p': {'a': int,'b': int}, 'dt': Date, 'c': [{'d': Decimal}]}
)
def adder(p,c, dt=None):
    "Add several values"
    import datetime
    dt = dt + datetime.timedelta(365)
    return {'AddResult':{'ab': p['a']+p['b'], 'dd': c[0]['d']+c[1]['d'], 'dt': dt}}

from uliweb.contrib.soap.views import SoapView

class SoapView2(SoapView):
    config = 'SOAP2'

@decorators.soap('hello2', returns={}, args={'a':str}, target='SOAP2')
def hello2(a):
    """
    This function is bound to SOAP2
    """
    return

