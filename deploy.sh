SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
SCPDESTINATION="$1:~/mounting_point"

[ -z "$1" ] && echo 'Need a destination <username>@<ip_address>.' && exit


###############################################################################
# Clear the static/ and dist/ directories
###############################################################################

[ -d dist/ ] && rm -rf dist
[ -d static/ ] && rm -rf static


###############################################################################
# Collect all static files into a static/ directory
###############################################################################

DJANGO_SETTINGS_MODULE='config.settings.local'
PYTHONPATH="$SCRIPTPATH/chrisdoescoding:$SCRIPTPATH"
python chrisdoescoding/manage.py collectstatic --noinput


###############################################################################
# Create Temp Directory
###############################################################################

TEMPDIR=$(mktemp -d)
mkdir $TEMPDIR/chrisdoescoding


###############################################################################
# Zip the Project to the Temp Directory
###############################################################################

zip -r $TEMPDIR/chrisdoescoding/chrisdoescoding.zip ./ \
    -D \
    -x \
        dist/** \
        **/__pycache__/** \
        **/*.pyc \
        *.git* \
        chrisdoescoding/**/static/**


###############################################################################
# Create Secret Key in Temp Directory
###############################################################################

SECRET_KEY_CHARS='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
unset SECRET_KEY
for i in {1..50} ; do
    SECRET_KEY="$SECRET_KEY${SECRET_KEY_CHARS:RANDOM%${#SECRET_KEY_CHARS}:1}"
done
echo $SECRET_KEY > $TEMPDIR/chrisdoescoding/secret


###############################################################################
# Copy the Nginx.conf to the Temp Directory
###############################################################################

cp /etc/nginx/nginx.conf $TEMPDIR/chrisdoescoding/nginx.conf


###############################################################################
# Create the dist/ directory and zip the Temp Directory into it
###############################################################################

mkdir dist
OUTNAME="$(pwd)/dist/$(date +%Y%m%d-%s)-chrisdoescoding.zip"
cd $TEMPDIR
zip $OUTNAME ./chrisdoescoding/*


###############################################################################
# Finally SCP the file to the server
###############################################################################

scp $OUTNAME $SCPDESTINATION
