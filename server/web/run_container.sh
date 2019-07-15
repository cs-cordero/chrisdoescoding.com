#!/bin/bash
DIR=$(dirname "$0")
ENVS=$DIR/envs

if [[ ! -e "$ENVS" ]]; then
    printf "E: Missing envs file.\n" >&2;
    exit 1;
fi

DOCKER_IMAGE=cscordero/chrisdoescoding.com:latest
DOCKER_NAME=chrisdoescoding
DOCKER_IP=172.18.0.2
DOCKER_NETWORK=chrisdoescoding
DOCKER_PORT=8000
NGINX_PROXY_PORT=8000

docker kill $DOCKER_NAME;
docker rm $DOCKER_NAME;
docker pull $DOCKER_IMAGE;
docker run \
    --detach \
    --publish $NGINX_PROXY_PORT:$DOCKER_PORT \
    --network $DOCKER_NETWORK \
    --ip $DOCKER_IP \
    --name $DOCKER_NAME \
    --env-file $ENVS \
    $DOCKER_IMAGE;
