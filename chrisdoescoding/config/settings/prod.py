import os

from django.core.exceptions import ImproperlyConfigured

from .common import *  # noqa: F403

DEBUG = False

try:
    with open(os.path.join(BASE_DIR, "secret"), "r") as f:  # noqa: F405
        SECRET_KEY = f.read()
except FileNotFoundError:
    SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    "45.56.107.251",
    "chrisdoescoding.com",
    "www.chrisdoescoding.com",
]


try:
    with open(os.path.join(BASE_DIR, "database"), "r") as f:  # noqa: F405
        _DATABASE = f.read()
except FileNotFoundError:
    _DATABASE = os.environ.get("DATABASE")

DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": _DATABASE}}

if not DATABASES["default"]["NAME"]:
    raise ImproperlyConfigured("Missing DATABASE environment variable")
del _DATABASE

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
