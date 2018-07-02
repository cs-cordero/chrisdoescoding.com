ROOT=$(dirname $0)

function help {
    echo "$0 - start the server"
    echo
    echo "$0 [options]"
    echo
    echo "Options:"
    echo "-h, --help  show brief help"
    echo "-d, --dev   run in dev mode, without gunicorn"
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
            NO_GUNICORN=1
            shift
            ;;
        *)
            help
            ;;
    esac
done


export PYTHONPATH=$ROOT:$ROOT/chrisdoescoding
export DJANGO_SETTINGS_MODULE='config.settings.local'
if [[ $NO_GUNICORN = 0 ]]; then
    gunicorn chrisdoescoding.wsgi
else
    python chrisdoescoding/manage.py runserver
fi
