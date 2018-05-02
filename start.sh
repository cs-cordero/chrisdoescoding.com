ROOT=$(dirname $0)

function help {
    echo "$0 - start the server"
    echo
    echo "$0 [options]"
    echo
    echo "Options:"
    echo "-h, --help        show brief help"
    echo "-p, --prod        run in prod mode, with gunicorn"
    echo "-d, --dev         run in dev mode, without gunicorn"
    echo
    echo
    exit 0
}

# Parse Options
PROD_MODE=0
DEV_MODE=0
while test $# -gt 0; do
    case "$1" in
        -h|--help)
            help
            ;;
        -p|--prod)
            PROD_MODE=1
            [[ $DEV_MODE = 1 ]] && help
            shift
            ;;
        -d|--dev)
            DEV_MODE=1
            [[ $PROD_MODE = 1 ]] && help
            shift
            ;;
        *)
            help
            ;;
    esac
done


export PYTHONPATH=$ROOT:$ROOT/chrisdoescoding
if [[ $PROD_MODE = 1 ]]; then
    export DJANGO_SETTINGS_MODULE='config.settings.prod'
    gunicorn chrisdoescoding.wsgi --bind=unix:/tmp/gunicorn.sock
elif [[ $DEV_MODE = 0 ]]; then
    export DJANGO_SETTINGS_MODULE='config.settings.local'
    gunicorn chrisdoescoding.wsgi
else
    export DJANGO_SETTINGS_MODULE='config.settings.local'
    python chrisdoescoding/manage.py runserver
fi
