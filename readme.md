# pylox interpreter

My first implementation of lox from https://craftinginterpreters.com,
using python.

# todo

- bug: when running prompt:
        > "asdf" + 4
        asdf
    while
        > "asdf"+4
        (+ asdf 4.0)
- try type hints