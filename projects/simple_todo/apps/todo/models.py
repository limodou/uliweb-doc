#coding=utf-8
from uliweb.orm import *

class Todo(Model):    
    title = Field(str, verbose_name="标题", max_length=255, required=True)
    post_date = Field(datetime.datetime, verbose_name='提交时间', auto_now_add=True)
    finished = Field(bool, verbose_name='是否完成')
