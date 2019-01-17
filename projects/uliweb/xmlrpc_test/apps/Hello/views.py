#coding=utf-8
from uliweb import function
xmlrpc = function('xmlrpc')

@xmlrpc
def hello():
    return 'hello'
    
@xmlrpc('func')
def new_func():
    return 'new_func'
    
@xmlrpc
class Hello(object):
    def test(self, name):
        return {'user':name}
        
    @xmlrpc('name')
    def new_name(self):
        return 'new_name' 