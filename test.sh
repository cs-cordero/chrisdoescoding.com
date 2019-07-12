ROOT=$(dirname $0)
export PYTHONPATH=$ROOT
export DJANGO_SETTINGS_MODULE='config.settings.local'

echo -ne "Running mypy..."\\r
mypy chrisdoescoding --no-incremental
[ ! $? = 0 ] && echo "Mypy failed. Exiting..." && exit
echo "Running mypy...Success!"
echo

echo -ne "Running flake8..."\\r
flake8 chrisdoescoding
[ ! $? = 0 ] && echo "Flake8 failed. Exiting..." && exit
echo "Running flake8...Success!"
echo

python $ROOT/chrisdoescoding/manage.py test chrisdoescoding/
