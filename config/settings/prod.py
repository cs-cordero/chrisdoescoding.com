from .common import *

import os

BASE_DIR = os.path.abspath(os.path.join(__file__, '..', '..', '..'))

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = [
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cs-cordero',
    }
}

STATIC_URL = '/static/'

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

INSTALLED_APPS = INSTALLED_APPS + ['mod_wsgi.server']
