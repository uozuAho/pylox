#!/bin/bash

TEST_PATTERN=$1
if [ -z "$1" ]; then
    TEST_PATTERN='*_tests.py'
fi

echo
echo running tests matching $TEST_PATTERN
echo

python -m unittest discover -s tests -p "$TEST_PATTERN"
