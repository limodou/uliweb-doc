#coding=utf-8
from uliweb import expose
from plugs.generic.views import View
from uliweb.i18n import ugettext as _

@expose('/')
class Todo(View):
    model = 'todo'
    layout = 'base.html'
    key_field = 'title'
    add_button_text = _('New')
    pagination = True
    rows = 10
        
    @expose('/')    
    def list(self):
        return View.list(self)
