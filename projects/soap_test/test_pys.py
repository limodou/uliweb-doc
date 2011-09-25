from datetime import date
from uliweb.lib.pysimplesoap.client import SoapClient
client = SoapClient(
    location = "",
    action = "", # SOAPAction
    namespace = "", 
    soap_ns='soap',
    wsdl="http://localhost:8000/SOAP?wsdl",
    trace = False,
    ns = False)
#response = client.Adder(p={'a':1,'b':2},dt=date.today(),c=[{'d':'1.20'},{'d':'2.01'}])
#print response
#result = response.AddResult
#print int(result.ab)
#print str(result.dd)
#print result.dt

result = client.hello(a='limodou')
print result
print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', client
result = client.echo(request='hello')
print result
#result = client.add([{'int':1}, {'int':2}])
#result = client.add({'int':[1,2]})
#print result
#result = client.Adder(p={'a':10, 'b':20}, c=[{'d':[decimal.Decimal('1.0'),decimal.Decimal('2.0')]}],
#    dt=date.today())
#print result
