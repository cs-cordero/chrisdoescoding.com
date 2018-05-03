ROOT=$(dirname $0)

function help {
    echo "$0 - start the server"
    echo
    echo "$0 [options]"
    echo
    echo "Options:"
    echo "-h, --help            show brief help"
    echo "-nog, --no-gunicorn   run in dev mode, without gunicorn"
    echo
    echo
    exit 0
}

# Parse Options
NO_GUNICORN=0
while test $# -gt 0; do
    case "$1" in
        -h|--help)
            help
            ;;
        -d|--dev)
            DEV_MODE=1
            shift
            ;;
        *)
            help
            ;;
    esac
done


export PYTHONPATH=$ROOT:$ROOT/chrisdoescoding
if [[ $DEV_MODE = 0 ]]; then
    export DJANGO_SETTINGS_MODULE='config.settings.local'
    gunicorn chrisdoescoding.wsgi
else
    export DJANGO_SETTINGS_MODULE='config.settings.local'
    python chrisdoescoding/manage.py runserver
fi
