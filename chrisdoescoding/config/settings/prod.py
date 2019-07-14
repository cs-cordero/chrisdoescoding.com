import os
from typing import Optional

from .common import *  # noqa: F403

DEBUG = False
SECRET_KEY: Optional[str]

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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "USER": os.environ["DB_USER"],
    }
}

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
