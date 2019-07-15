SCRIPT_NAME=$(basename "$0")
SCRIPTS_FOLDER=$(dirname "$0")
PROJECT_ROOT=$SCRIPTS_FOLDER/../../

if [[ ! -e "$PROJECT_ROOT/pyproject.toml" ]]; then
    printf "E: $PROJECT_ROOT is not the project root.\n" >&2;
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

TAG=
for i in "$@"; do
    case $i in
        -h|--help)
            usage
            ;;
        -t=*|--tag=*)
            [[ -n "$TAG" ]] && usage
            TAG="${i#*=}"
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
            TAG="$i"
            shift
            ;;
    esac
done

if [[ -z "$TAG" ]] || [[ -z $(echo "$TAG" | grep 'v\d\+\.\d\+\.\d\+') ]]; then
    printf "E: A tag label with the format vX.Y.Z is required.\n" >&2;
    usage
fi

# This assumes that you are inside the root git folder.
# TODO allow this to be run from anywhere.
IMAGE_NAME=cscordero/chrisdoescoding.com:$TAG
docker build -t $IMAGE_NAME $PROJECT_ROOT
docker push $IMAGE_NAME

docker tag $IMAGE_NAME cscordero/chrisdoescoding.com:latest
docker push cscordero/chrisdoescoding.com:latest
