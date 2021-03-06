import sys, os

path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)
apps_dir = os.path.join(path, 'apps')

from uliweb.manage import make_application
application = make_application(apps_dir=apps_dir)
