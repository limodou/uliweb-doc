#coding=utf-8
from uliweb import expose, functions
from uliweb.form import *
from uliweb.orm import get_model

@expose('/')
def index():
    class F(Form):
        filename = FileField('filename')

    File = get_model('dbuploadfiles')
    form = F()
    result = {'objects':File.all(), 'form':form}
    if request.method == 'GET':
        return result
    else:
        if form.validate(request.files):
            nfile = functions.save_file_field(form.filename)
            return result
        else:
            return result

@expose('/deletefile')
def deletefile():
    filename = request.GET.get('filename')
    if filename:
        functions.delete_filename(filename)
    return redirect(url_for(index))