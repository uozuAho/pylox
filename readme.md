# pylox interpreter

My first implementation of lox from https://craftinginterpreters.com, using python.

Running tests:

    ./run_tests.sh

Run the pylox REPL:

    python pylox.py


# todo
- dont import classes explicitly from statements, expressions etc.
- rename VariableExpression to Variable
- up to here: https://craftinginterpreters.com/statements-and-state.html
- bug: 1 == 1 == 1 is false due to (I think):
    - (1 == 1) == 1
    - ( True ) == 1
    - = False

# fun stuff for later

- python to javascript
    - try first, then look for existing tools
- python to bash
- python to webassembly
- c# to webassembly
    - what does blazor do?