from uliweb.orm import *

class Note(Model):
    username = Field(CHAR)
    message = Field(TEXT)
    homepage = Field(str, max_length=128)
    email = Field(str, max_length=128)
    datetime = Field(datetime.datetime, auto_now_add=True)
