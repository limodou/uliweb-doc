from uliweb.form import *

class NoteForm(Form):
    message = TextField(label='Message', required=True)
    username = StringField(label='Username', required=True)
    homepage = StringField(label='Homepage')
    email = StringField(label='Email')

