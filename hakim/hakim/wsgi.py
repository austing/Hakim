import os, sys, site

# Tell wsgi to add the Python site-packages to its path. 
site.addsitedir('/home/username/.virtualenvs/hakim/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'hakim.settings'

activate_this = os.path.expanduser("~/.virtualenvs/hakim/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/mark97229/webapps/hakim/Hakim/hakim'
workspace = os.path.dirname(project)
sys.path.append(workspace)

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()