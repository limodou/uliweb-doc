from uliweb.orm import *

class File(Model):
    filename = Field(FILE, upload_to_sub='test')