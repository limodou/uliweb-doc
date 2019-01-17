#coding=utf-8
from xmlrpclib import ServerProxy

server = ServerProxy("http://localhost:8000/XMLRPC")

print server.hello()
print server.func()
print server.Hello.test('limodou')
