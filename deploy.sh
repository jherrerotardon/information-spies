#!/bin/bash

clear

# Get paths.
PROJECT_PATH=$(dirname "$(realpath "$0")")

# Get env.
APP_ENV=$(grep '^APP_ENV=*' ${PROJECT_PATH}/.env | awk -F '"' '{print $2;}')
if [[ -z ${APP_ENV} ]]; then
    echo "Please, set environment var."

    exit 1
fi

# Update repository.
git -C "${PROJECT_PATH}" pull

# Set development flag if is necessary.
if [[ ${APP_ENV} != 'prod' && ${APP_ENV} != 'pre' ]]; then
  # Set Development flag to install dev packages.
  DEV='--dev'
fi

# Install dependencies.
export PIPENV_VENV_IN_PROJECT=true && python3 -m pipenv sync ${DEV}
