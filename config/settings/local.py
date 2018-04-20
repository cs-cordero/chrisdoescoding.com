from .common import *

import os

DEBUG = True
SECRET_KEY = 'x1&6njoiwqnje!y63((#$y!o(y)@929&%!y31dftl0_ef(xrnz'
ALLOWED_HOSTS = [
    '*'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cs-cordero',
    }
}
