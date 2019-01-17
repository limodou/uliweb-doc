#coding=utf-8
from uliweb.orm import *
from sqlalchemy import text

class Todo(Model):    
    title = Field(str, verbose_name="标题", max_length=200, required=True, index=True, server_default="hello")
    post_date = Field(datetime.datetime, verbose_name='提交时间', auto_now_add=True)
    post_time = Field(datetime.datetime, verbose_name='提交时间', auto_now_add=True)
    finished = Field(bool, verbose_name='是否完成')
    date_type = Field(datetime.date)
    time_type = Field(datetime.time)
    float_type = Field(float)
    decimal_type = Field(DECIMAL, scale=3, server_default=text('0.000'))
    text = Field(TEXT)
    blob = Field(BLOB)
    pickle = Field(PICKLE)
    
    @classmethod
    def OnInit(cls):
        Index('todo_idx', cls.c.title)
        
class Test(Model):
    name = Field(str)
    todos = ManyToMany('todo')

class Test1(Model):
    name = Field(str)
    name2 = Field(int, server_default=text('3'))
    t = Reference('todo')
