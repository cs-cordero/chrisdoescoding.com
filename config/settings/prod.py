from .common import *

import os

DEBUG = False

try:
    with open(os.path.join(BASE_DIR, 'secret'), 'r') as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'chrisdoescoding.com',
    'www.chrisdoescoding.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cs-cordero',
    }
}

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
