# pylox interpreter

My implementation of lox from https://craftinginterpreters.com, using python.

# quick start
Install required programs:
- [uv](https://github.com/astral-sh/uv)
- bash-compatible shell

```sh
./make.sh test
./make.sh help

# before committing
./make.sh test
./make.sh format
./make.sh lint
```

# crash course
See the [crash course](/docs/crash-course.md)

# todo
- functions: https://craftinginterpreters.com/functions.html
    - WIP: document how to add a language feature in crash-course
    - WIP: func decl
        - add visit func decl stub to interpreter
    - maybe: func call
    - read from start of https://craftinginterpreters.com/functions.html
- when functions implemented: write tests in lox
- repl: parameter for debug verbosity on/off
- repl: don't throw on undefined var
- parser error recovery: https://craftinginterpreters.com/statements-and-state.html#parsing-variables
    - try catch in declaration. throw for now?
- bug: 1 == 1 == 1 is false due to (I think):
    - (1 == 1) == 1
    - ( True ) == 1
    - = False
