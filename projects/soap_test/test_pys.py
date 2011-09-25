#coding=utf8
from datetime import date
import decimal
from uliweb.lib.pysimplesoap.client import SoapClient
client = SoapClient(
    location = "",
    action = "", # SOAPAction
    namespace = "", 
    soap_ns='soap',
    wsdl="http://localhost:8000/SOAP?wsdl",
    trace = False,
    ns = False)

result = client.hello(a='limodou')
print 'test1:', result
#result = client.echo(value='hello')
#print 'test2:', result
result = client.add([1,2])
print 'test3:', result
result = client.service.string({'string':[u'中', u'国']})
print 'test4:', result
result = client.Adder(p={'a':10, 'b':20}, c=[{'d':[decimal.Decimal('1.0'),decimal.Decimal('2.0')]}],
    dt=date.today())
print result
