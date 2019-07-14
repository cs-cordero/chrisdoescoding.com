from typing import Dict, List

from .common import *  # noqa: F401, F403

DEBUG = True
SECRET_KEY = "x1&6njoiwqnje!y63((#$y!o(y)@929&%!y31dftl0_ef(xrnz"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {"ENGINE": "django.db.backends.postgresql", "NAME": "cs-cordero"}
}

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = []

INSTALLED_APPS.append("django_extensions")  # noqa: F405
