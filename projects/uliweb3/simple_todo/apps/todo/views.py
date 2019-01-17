#coding=utf-8
from uliweb import expose

@expose('/todo')
class Todo(object):
    def __init__(self):
        from uliweb.orm import get_model
        
        self.model = get_model('todo')
    
    @expose('/')    
    def index(self):
        return {'todos':self.model.all()}
    
    def new(self):
        title = request.POST.get('title')
        if not title:
            error('标题是必须的')
        todo = self.model(title=title)
        todo.save()
        return redirect(url_for(Todo.index))
        
    def _get_todo(self, id):
        todo = self.model.get(int(id))
        if not todo:
            error('没找到这条记录')
        return todo
    
    def edit(self, id):
        todo = self._get_todo(id)
        if request.method == 'GET':
            return {'todo':todo}
        else:
            title = request.POST.get('title')
            if not title:
                error('标题是必须的')
            todo.title = title
            todo.save()
            return redirect(url_for(Todo.index))
            
    def delete(self, id):
        todo = self._get_todo(id)
        todo.delete()
        return redirect(url_for(Todo.index))
        