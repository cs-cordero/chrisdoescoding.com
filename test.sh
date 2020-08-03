#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m'

AT_LEAST_ONE_ERROR=0

function capture_stdout_and_stderr_if_successful {
    set +e
    COMMAND=$*
    printf "Running %s ... " "${COMMAND}"

    if ! OUTPUT=$($COMMAND 2>&1); then
        AT_LEAST_ONE_ERROR=1
        printf "%bFailed%b\n" "${RED}" "${RESET}"
        printf "%s\n\n" "${OUTPUT}"
    else
        printf "%bSuccess!%b\n" "${GREEN}" "${RESET}"
    fi
    set -e
}


export DJANGO_SETTINGS_MODULE=config.settings.local
export PYTHONPATH=chrisdoescoding
export MYPYPATH=chrisdoescoding/stubs

capture_stdout_and_stderr_if_successful mypy chrisdoescoding --no-incremental
capture_stdout_and_stderr_if_successful flake8 chrisdoescoding --count
capture_stdout_and_stderr_if_successful isort -rc chrisdoescoding --check-only
capture_stdout_and_stderr_if_successful black chrisdoescoding --check
capture_stdout_and_stderr_if_successful python chrisdoescoding/manage.py makemigrations --check
capture_stdout_and_stderr_if_successful python chrisdoescoding/manage.py test

exit $AT_LEAST_ONE_ERROR
