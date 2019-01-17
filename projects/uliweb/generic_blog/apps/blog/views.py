#coding=utf-8
from uliweb import expose
from uliweb.orm import get_model

@expose('/')
class BlogView(object):
    def __init__(self):
        self.model = get_model('blog')
        
    @expose('')
    def list(self):
        from uliweb.utils.generic import ListView
        
        def title(value, obj):
            return obj.get_url()
        
        view = ListView(self.model, condition=(self.model.c.deleted==False),
            fields_convert_map={'title':title}, 
            pagination=False)
        return view.run()
    
    def add(self):
        from uliweb.utils.generic import AddView
        
        def get_url(id):
            return url_for(BlogView.view, id=id)
        
        view = AddView(self.model, ok_url=get_url)
        return view.run()
    
    def view(self, id):
        from uliweb.utils.generic import DetailView
        
        obj = self.model.get_or_notfound(int(id))
        view = DetailView(self.model, obj=obj)
        return view.run()
    
    def edit(self, id):
        from uliweb.utils.generic import EditView
        
        obj = self.model.get_or_notfound(int(id))
        view = EditView(self.model, 
            ok_url=url_for(BlogView.view, id=int(id)), 
            obj=obj)
        return view.run()
    
    def delete(self, id):
        from uliweb.utils.generic import DeleteView
        
        obj = self.model.get_or_notfound(int(id))
        view = DeleteView(self.model, obj=obj, 
            ok_url=url_for(BlogView.view, id=int(id)),
            use_delete_fieldname='deleted')
        return view.run()