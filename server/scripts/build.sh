#!/bin/bash

SCRIPT_NAME=$(basename "$0")
SCRIPTS_FOLDER=$(dirname "$0")
PROJECT_ROOT=$SCRIPTS_FOLDER/../../

if [[ ! -e "$PROJECT_ROOT/pyproject.toml" ]]; then
    printf "E: %s is not the project root.\n" "$PROJECT_ROOT" >&2;
    exit 1
fi

function usage(){
    echo "$SCRIPT_NAME"
    echo "Builds a docker image from the repository and pushes it to Docker Hub."
    echo
    echo "Usage:"
    echo "    $SCRIPT_NAME tag"
    echo
    echo "Arguments:"
    echo "    tag:  Must be in the format vX.Y.Z, e.g., v1.1.0"
    exit 1
}

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

TAG=
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -t=*|--tag=*)
            [[ -n "$TAG" ]] && usage
            TAG="${1#*=}"
            shift
            ;;
        -t|--tag)
            [[ -n "$TAG" ]] && usage
            TAG="$2"
            shift
            shift
            ;;
        *)
            [[ -n "$TAG" ]] && usage
            TAG="$1"
            shift
            ;;
    esac
done

if ! grep -q 'v\d\+\.\d\+\.\d\+' <<< "$TAG"; then
    printf "E: A tag label with the format vX.Y.Z is required.\n" >&2;
    usage
fi

# This assumes that you are inside the root git folder.
# TODO allow this to be run from anywhere.
BASE_NAME=cscordero/chrisdoescoding.com
IMAGE_NAME=$BASE_NAME:$TAG
LATEST_NAME=$BASE_NAME:latest

echo
echo "Script will now perform the following commands:"
echo "  1. Run tests locally."
echo "  2. Update the version number in pyproject.toml to $TAG"
echo "  3. Build docker image for $TAG and reset the 'latest' tag."
echo
echo "Any errors will cause the script to abort."
echo
confirm "Proceed with $TAG?"
echo

set -e
if ! git diff-index --quiet HEAD; then
    echo "You have unstaged git changes.  Please stage or reset all changes."
    exit 1
fi
MASTER_BRANCH=master
if [[ $(git rev-parse --abbrev-ref HEAD) -ne "$MASTER_BRANCH" ]]; then
    echo "You are not checked out to the $MASTER_BRANCH branch."
    exit 1
fi

./test.sh

PATTERN="^version.*$"
gsed -i "0,/${PATTERN}/s/${PATTERN}/version = \"${TAG#v}\"/" pyproject.toml

docker build -t "$IMAGE_NAME" "$PROJECT_ROOT"
docker tag "$IMAGE_NAME" "$LATEST_NAME"

echo
echo "Script will now perform the following commands:"
echo "  1. Git commit all changes in pyproject.toml to a new release commit."
echo "  2. Git tag the latest commit."
echo "  3. Push git commit to GitHub."
echo "  4. Push docker images to Docker Hub."
echo
echo "Any errors will cause the script to abort."
echo
confirm "Proceed?"
echo

git add pyproject.toml
git commit -m "Release $TAG"
git tag -a "$TAG" -m "Release $TAG"

docker push "$IMAGE_NAME"
docker push "$LATEST_NAME"
git push
git push origin "$TAG"
