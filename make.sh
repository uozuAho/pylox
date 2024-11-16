#!/bin/bash
#
# I hate make, https://github.com/casey/just is painful to get working
# on windows. Sigh.

set -eu

command=${1:-""}

if [ "$command" == "help" ] || [ "$command" == "" ]; then
    echo "See the readme"
    echo "Available commands:"
    cat make.sh | grep -oE '\$command" == "(.*)"'
elif [ "$command" == "lint" ]; then
    uv run ruff check
    uv run mypy .
elif [ "$command" == "format" ]; then
    uv run ruff format
elif [ "$command" == "test" ]; then
    pattern=${2:-"*_tests.py"}
    uv run python -m unittest discover -s tests -p "$pattern"
elif [ "$command" == "lox-repl" ]; then
    uv run python pylox.py
fi
