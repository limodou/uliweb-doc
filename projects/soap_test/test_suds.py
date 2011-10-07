#coding=utf8
import logging
logging.basicConfig()
logging.getLogger('suds.client').setLevel(logging.DEBUG)

import decimal
from datetime import date

from suds.client import Client
client = Client('http://localhost:8000/SOAP?wsdl')
#result = hello_client.service.say_hello("Dave", 5)
print client

result = client.service.hello('limodou')
print 'test1:', result
#result = client.service.echo('hello')
#print 'test2:', result
#result = client.service.add({'int':[1,2]})
#print 'test3:', result
#result = client.service.string({'string':[u'中', u'国']})
#print 'test4:', result
#result = client.service.Adder(p={'a':10, 'b':20}, c=[{'d':[decimal.Decimal('1.0'),decimal.Decimal('2.0')]}],
#    dt=date.today())
#print 'test5:', result