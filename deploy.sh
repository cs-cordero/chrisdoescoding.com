SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

export DJANGO_SETTINGS_MODULE='config.settings.prod'
export PYTHONPATH="$SCRIPTPATH/chrisdoescoding:$SCRIPTPATH"

# Clear the static and dist directories
[ -d dist/ ] && rm -rf dist
[ -d static/ ] && rm -rf static

# Collect the Static Files
python chrisdoescoding/manage.py collectstatic --noinput

# Throw things into the dist directory
mkdir dist

# includes all project files, excluding:
#       dist/ folder
#       __pycache__/ folders
#       .pyc files
#       internal /static/ folders
zip -r dist/chrisdoescoding.zip ./ -D -x dist/** __pycache__/** **/*.pyc *.git* chrisdoescoding/**/static/**

# pre-made secret_key
SECRET_KEY_CHARS='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
unset SECRET_KEY
for i in {1..50} ; do
    SECRET_KEY="$SECRET_KEY${SECRET_KEY_CHARS:RANDOM%${#SECRET_KEY_CHARS}:1}"
done
echo $SECRET_KEY > dist/secret

# nginx config
cp /etc/nginx/nginx.conf dist/nginx.conf

# give success message
echo
echo
echo "created static/"
echo "created dist/chrisdoescoding.zip"
echo "created dist/secret"
echo "created dist/nginx.conf"
