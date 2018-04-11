ROOT=$(dirname $0)
echo $ROOT

export PYTHONPATH=$ROOT
export DJANGO_SETTINGS_MODULE='config.settings.local'
python $ROOT/chrisdoescoding/manage.py runserver
