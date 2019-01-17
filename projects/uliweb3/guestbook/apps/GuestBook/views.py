#coding=utf-8
from uliweb import expose, functions
from uliweb.utils.textconvert import text2html

@expose('/')
def index():
    Note = functions.get_model('note')
    notes = Note.all().order_by(Note.c.datetime.desc())
    return {'notes':notes,'text2html':text2html}

@expose('/new')
def new_comment():
    from .forms import NoteForm
    import datetime
    
    Note = functions.get_model('note')
    form = NoteForm()
    if request.method == 'GET':
        return {'form':form, 'message':''}
    elif request.method == 'POST':
        flag = form.validate(request.values)
        if flag:
            n = Note(**form.data)
            n.save()
            return redirect(url_for(index))
        else:
            message = "There is something wrong! Please fix them."
            return {'form':form, 'message':message}

@expose('/delete/<id>')
def del_comment(id):
    Note = functions.get_model('note')
    n = Note.get(int(id))
    if n:
        n.delete()
        return redirect(url_for(index))
    else:
        error("No such record [%s] existed" % id)
