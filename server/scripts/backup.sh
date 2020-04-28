#!/bin/bash
GREEN='\033[0;32m'
NC='\033[0m'

SCRIPT_NAME=$(basename "$0")

function usage(){
    echo "$SCRIPT_NAME"
    echo "Runs pg_dump on the database and uploads it to S3."
    echo
    echo "Usage:"
    echo "    $SCRIPT_NAME [--env-file env-file]"
    echo
    echo "Arguments:"
    echo "    env-file:  (Optional) path to an env file which define the expected environment variables."
    echo "               If provided, this file will override any environment variables"
    echo
    echo "Required environment variables"
    echo "    The following environment variables are either required to be set manually"
    echo "    in your termnal or defined in the file provided in the env-file optional argument."
    echo
    echo "    AWS_ACCESS_KEY_ID"
    echo "    AWS_SECRET_ACCESS_KEY"
    echo "    AWS_DEFAULT_REGION"
    echo "    AWS_S3_BUCKET_NAME"
    echo "    DB_NAME"
    echo "    DB_HOST"
    echo "    DB_PORT"
    echo "    DB_USER"
    exit 1
}

ENV_FILE=
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -e=*|--env-file=*)
            [[ -n "$ENV_FILE" ]] && usage
            ENV_FILE="${i#*=}"
            shift
            ;;
        -e|--env-file)
            [[ -n "$ENV_FILE" ]] && usage
            ENV_FILE="$2"
            shift
            shift
            ;;
        *)
            [[ -n "$ENV_FILE" ]] && usage
            usage
            ;;
    esac
done

if [[ -f "$ENV_FILE" ]]; then
    # shellcheck source=/dev/null
    if ! . "$ENV_FILE"; then
        exit 1
    fi
fi

REQUIRED_ENV_KEY=(
    "AWS_ACCESS_KEY_ID"
    "AWS_SECRET_ACCESS_KEY"
    "AWS_DEFAULT_REGION"
    "AWS_S3_BUCKET_NAME"
    "DB_NAME"
    "DB_HOST"
    "DB_PORT"
    "DB_USER"
)
MISSING_ENVS=()
for key in "${REQUIRED_ENV_KEY[@]}"; do
    [[ -z "${!key}" ]] && MISSING_ENVS+=("$key")
done

if [[ ${#MISSING_ENVS[@]} -gt 0 ]]; then
    echo "The following required environment variables are not set.  See help for more information:"
    for i in "${MISSING_ENVS[@]}"; do
        echo "    $i"
    done
    exit 1
fi


TEMP_DIR="/tmp"
BACKUP_FILE_NAME="$DB_NAME-backup-$(date +'%Y%m%d-%k%M%S')"

pg_dump \
    --dbname="$DB_NAME" \
    --host="$DB_HOST" \
    --port="$DB_PORT" \
    --username="$DB_USER" \
    --no-password \
    --file="/tmp/$BACKUP_FILE_NAME"

S3_BUCKET_URI="s3://$AWS_S3_BUCKET_NAME/$BACKUP_FILE_NAME"

if docker run \
        --rm \
        --interactive \
        --tty \
        --env-file "$ENV_FILE" \
        --volume $TEMP_DIR:$TEMP_DIR \
        amazon/aws-cli:latest \
        s3 mv "$TEMP_DIR/$BACKUP_FILE_NAME" "$S3_BUCKET_URI"; then
    echo -e "${GREEN}Successfully uploaded $BACKUP_FILE_NAME to S3.${NC}"
    exit 0
fi
