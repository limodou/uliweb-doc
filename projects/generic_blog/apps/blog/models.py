#coding=utf8

from uliweb.orm import *

class Blog(Model):
    __verbose_name__ = 'Blog'
    
    #author = Reference('user', verbose_name='作者', required=True)
    create_date = Field(datetime.datetime, verbose_name='发表时间', auto_now_add=True)
    title = Field(str, max_length=255, verbose_name='标题', required=True)
    content = Field(TEXT, verbose_name='内容', required=True)
    deleted = Field(bool, verbose_name='删除标志')
    
    class Table:
        fields = [
            'title', 'create_date',
        ]
        
    class AddForm:
        fields = ['title', 'content']
        
    class EditForm:
        fields = ['title', 'content']
    
    def __unicode__(self):
        return self.title
    
    def get_url(self):
        return '<a href="/view/%d">%s</a>' % (self.id, unicode(self))