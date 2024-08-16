"""
---------------------------------------------------
         --- Deploy Django Productive ---
---------------------------------------------------
"""

import socket
from .base import *

# Configurations DNS, False for productive
DEBUG = False

name_computer = socket.gethostname()
the_ip = socket.gethostbyname(name_computer)

ALLOWED_HOSTS = ['*']

print(".: IP PRODUCTIVE :.\n {}".format(the_ip))

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5441',
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# FILES STATIC CONFIGURATIONS

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

print(".: The static folder :. \n"+ STATIC_ROOT)

# FILES MEDIA CONFIGURATIONS

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

print(".: The media folder :. \n"+ MEDIA_ROOT)

# The static finders

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]