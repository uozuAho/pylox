#!/bin/bash
#
# I hate make, https://github.com/casey/just is painful to get working
# on windows. Sigh.

set -eu

if [ ! -d ".venv" ]; then
    py -3.12 -m venv .venv
    source .venv/Scripts/activate
    pip install pip-tools
    pip-compile requirements.in
    pip-sync
else
    source .venv/Scripts/activate
fi

command=${1:-""}

if [ "$command" == "help" ] || [ "$command" == "" ]; then
    echo "See the readme"
    echo "Available commands:"
    cat make.sh | grep -oE '\$command" == "(.*)"'
elif [ "$command" == "update-deps" ]; then
    pip-compile
    pip-sync
elif [ "$command" == "lint" ]; then
    ruff check
    mypy .
elif [ "$command" == "format" ]; then
    ruff format
elif [ "$command" == "test" ]; then
    pattern=${2:-"*_tests.py"}
    python -m unittest discover -s tests -p "$pattern"
elif [ "$command" == "lox-repl" ]; then
    python pylox.py
fi

echo "Don't forget to:"
echo ". .venv/Scripts/activate"
