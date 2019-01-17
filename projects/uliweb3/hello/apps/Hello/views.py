#coding=utf-8
from uliweb import expose, functions

@expose('/')
def index():
    return '<h1>Hello, Uliweb</h1>'

@expose('/template')
def template():
    return {}

@expose('/template1')
def template1():
    return {'content':'Uliweb'}
