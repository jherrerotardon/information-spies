#!/usr/bin/env bash

PROJECT_PATH=$(dirname $(dirname $(realpath $0)))

PYLINT="${PROJECT_PATH}/.venv/bin/python -m pylint"

# Get option and generate command.
OPTION=$1
FILES=$(eval "find ${PROJECT_PATH} -path ${PROJECT_PATH}/venv -prune -o -type f -name '*.py' | grep -v venv")
COMMAND="${PYLINT}"
if [[ ${OPTION} == '-E' ]]
then
    COMMAND="${COMMAND} ${OPTION}"
elif [[ ${OPTION} == '--help' ]]
then
    echo -e "Usage:\n"
    echo -e "Options:"
    echo -e "\t --help:\t Print usage."
    echo -e "\t -q:\t\t Print only code rate."
    echo -e "\t -E:\t\t Print only errors."

    exit 0
fi

# Execute command.
if [[ ${OPTION} == '-q' ]]
then
    COMMAND="${COMMAND} $FILES | awk '\$0 ~ /Your code/ || \$0 ~ /Global/ {print}'"
    eval ${COMMAND}
else
    ${COMMAND} ${FILES}
fi

ACK=$?

# Pylint code outputs.
# 0   no error.
# 1   fatal message issued.
# 2   message issued.
# 4   message issued.
# 8   refactor message issued.
# 16  convention message issued.
# 32  usage error.
INVALID_EXIT_CODES=(1 2 32)

# Only return error with pylint errors. Ignore warnings.
if [[ ${INVALID_EXIT_CODES[@]} =~ ${ACK} ]]
then
    echo -e "\033[0;31mError scanning code.'\033[0m Please, fix errors."
    EXIT_CODE=${ACK}
else
    EXIT_CODE=0
fi

exit ${EXIT_CODE}
