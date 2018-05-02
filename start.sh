ROOT=$(dirname $0)

function help {
    echo "$0 - start the server"
    echo
    echo "$0 [options]"
    echo
    echo "Options:"
    echo "-h, --help                show brief help"
    echo "-p, --prod                run in prod mode, with gunicorn"
    echo
    echo
    exit 0
}

# Parse Options
PROD_MODE=0
while test $# -gt 0; do
    case "$1" in
        -h|--help)
            help
            ;;
        -p|--prod)
            PROD_MODE=1
            shift
            ;;
        *)
            break
            ;;
    esac
done


export PYTHONPATH=$ROOT:$ROOT/chrisdoescoding
if [[ $PROD_MODE = 1 ]]; then
    export DJANGO_SETTINGS_MODULE='config.settings.prod'
    gunicorn chrisdoescoding.wsgi
else
    export DJANGO_SETTINGS_MODULE='config.settings.local'
    python $ROOT/chrisdoescoding/manage.py runserver
fi
