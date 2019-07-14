IMAGE_LOCATION="$1"

[ -z "$1" ] && echo 'Need an image_file from mounting_point.' && exit
[ ! -f "$1" ] && echo "Could not find $1" && exit

BUILD_SITE="$HOME/chrisdoescoding"

echo "Removing the last _old archive..."
[ -d "${BUILD_SITE}_old" ] && rm -rf "${BUILD_SITE}_old"

# killing gunicorn
pkill gunicorn

echo "Destroying old virtual environment and archiving old build"
if [ -d $BUILD_SITE ]; then
    cd $BUILD_SITE
    # pipenv --rm
    cd $HOME
    mv "$BUILD_SITE" "${BUILD_SITE}_old"
fi

echo "Unzipping Image files..."
unzip $IMAGE_LOCATION -d $BUILD_SITE
cd $BUILD_SITE
mv chrisdoescoding/* ./
rm -r chrisdoescoding
unzip chrisdoescoding.zip
rm chrisdoescoding.zip

echo "Copying old database pointer to new site..."
cd $HOME
FOUND_DB_FILE=0
if [ -d "${BUILD_SITE}_old" ]; then
    if [ -f "${BUILD_SITE}_old/database" ]
        cp "${BUILD_SITE}_old/database" $BUILD_SITE
        FOUND_DB_FILE=1
    fi
fi
[ $FOUND_DB_FILE = 0 ] && echo "Could not find old database file! You'll have to create it manually."

echo "Building the environment..."
cd $BUILD_SITE
pipenv install

echo "Performing some health checks..."
ERROR=0
[ ! -f "${BUILD_SITE}/database" ] && echo "Missing ${BUILD_SITE}/database file." && ERROR=1
[ ! -f "${BUILD_SITE}/secret" ] && echo "Missing ${BUILD_SITE}/secret file." && ERROR=1
[ ! -d "${BUILD_SITE}/static" ] && echo "Missing ${BUILD_SITE}/static directory." && ERROR=1
if [ ! -f "/etc/nginx/nginx.conf" ]; then
    if [ ! -f "${BUILD_SITE}/nginx.conf" ]; then
        echo "Missing ${BUILD_SITE}/database file."
    else
        echo "Manually copy the ${BUILD_SITE}/nginx.conf file to /etc/nginx/."
    fi
    ERROR=1
fi
[ $ERROR = 1 ] && exit

echo "Build complete.  Call pipenv shell then source start_prod to begin the server.  Double check that the app is running and that the server is listening using sudo netstat -tulpn.  Good luck."
