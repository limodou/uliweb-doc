from suds.client import Client
client = Client('http://localhost:8000/SOAP?wsdl')
print client

result = client.service.hello('limodou')
print 'test1:', result