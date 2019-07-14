set -e  # Exit immediately after first non-zero return value
DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE || 'config.settings.local'

mypy chrisdoescoding --no-incremental
flake8 chrisdoescoding --count
isort -rc chrisdoescoding --check-only
black chrisdoescoding --check
python chrisdoescoding/manage.py makemigrations --check
python chrisdoescoding/manage.py test
