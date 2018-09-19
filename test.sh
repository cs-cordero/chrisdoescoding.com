ROOT=$(dirname $0)
echo $ROOT

export PYTHONPATH=$ROOT
export DJANGO_SETTINGS_MODULE='config.settings.local'
export MYPYPATH="$ROOT/chrisdoescoding/stubs"
echo -ne "Running mypy tests..."\\r
mypy --config-file $ROOT/chrisdoescoding/mypy.ini $ROOT/chrisdoescoding/posts
[ ! $? = 0 ] && echo "Mypy test failed. Exiting..." && exit
echo "Running mypy tests...Success!"
echo
python $ROOT/chrisdoescoding/manage.py test chrisdoescoding/
