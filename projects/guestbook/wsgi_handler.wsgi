import sys, os
path = os.path.dirname(__file__)
sys.path.insert(0, path)
from uliweb.manage import make_application
application = make_application()
