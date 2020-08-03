#!/bin/bash
DIR=$(dirname "$0")
ENVS=$DIR/envs

if [[ ! -e "$ENVS" ]]; then
    printf "E: Missing envs file.\n" >&2;
    exit 1;
fi

function confirm() {
    while true
    do
        read -p "$* (y/n): " -n 1 -r
        echo    # (optional) move to a new line
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            return 0
        elif [[ $REPLY =~ ^[Nn]$ ]]; then
            exit 1
        fi
    done
}

DOCKER_IMAGE=cscordero/chrisdoescoding.com:latest
MIGRATING_DOCKER_NAME=chrisdoescoding-migrate
RUNNING_DOCKER_NAME=chrisdoescoding
DOCKER_NETWORK=chrisdoescoding


confirm "Will kill the currently running container to run migrate offline. Proceed?"

docker kill $RUNNING_DOCKER_NAME;
docker rm $RUNNING_DOCKER_NAME;
docker pull $DOCKER_IMAGE;
docker run \
    -it \
    --rm \
    --network $DOCKER_NETWORK \
    --name $MIGRATING_DOCKER_NAME \
    --env-file $ENVS \
    $DOCKER_IMAGE \
    poetry run chrisdoescoding/manage.py migrate

echo "Script complete.  If successful, run the run_container.sh script now."
