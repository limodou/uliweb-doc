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

@expose('/list')
def list():
    File = get_model('file')
    return {'objects':File.all()}

@expose('/upload')
def upload():
    File = get_model('file')
    view = functions.AddView(File, ok_url='/list', upload_to='aaa', upload_to_sub='bbb', fileserving_config='UPLOAD_TEST')
    return view.run()

@expose('/edit/<id>')
def edit(id):
    File = get_model('file')
    obj = File.get(int(id))
    view = functions.EditView(File, obj=obj, ok_url='/list', upload_to='aaa', upload_to_sub='bbb', fileserving_config='UPLOAD_TEST')
    return view.run()

@expose('/delete/<id>')
def delete(id):
    File = get_model('file')
    obj = File.get(int(id))

    def pre_delete(obj):
        fileserving = functions.get_fileserving('UPLOAD_TEST')
        fileserving.delete_filename(obj.filename)

    view = functions.DeleteView(File, obj=obj, ok_url='/list', pre_delete=pre_delete)
    return view.run()