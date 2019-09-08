# pylox interpreter

My first implementation of lox from https://craftinginterpreters.com, using python.

Running tests:

    ./run_tests.sh

Run the pylox REPL:

    python pylox.py


# todo
- rename 'expr' imports to expressions. same for stmt
- repl: parameter for debug verbosity on/off
- parser error recovery: https://craftinginterpreters.com/statements-and-state.html#parsing-variables
    - try catch in declaration. throw for now?
- up to here: https://craftinginterpreters.com/statements-and-state.html#assignment
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