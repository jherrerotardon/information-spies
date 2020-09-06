#!/usr/bin/env bash

echo -e "Auto formatting python code..."

find . -type f -name "*.py" | grep -v venv | xargs .venv/bin/python -m autopep8 --in-place --aggressive

exit 0