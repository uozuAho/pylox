# pylox interpreter

My implementation of lox from https://craftinginterpreters.com, using python.

# quick start
Install required programs:
- [python](https://www.python.org/)
    - last tested with 3.12
- bash-compatible shell
    - my go-to is [git for windows](https://git-scm.com/download/win)

```sh
./make.sh test
./make.sh help

# before committing
./make.sh test
./make.sh format
./make.sh lint
```

# todo
- WIP: type/lint/test fixes
    - see inline todos "todo: type"
- WIP: document a crash course
    - see [](/docs/crash-course.md)
- up to here: https://craftinginterpreters.com/control-flow.html#logical-operators
- repl: parameter for debug verbosity on/off
- repl: don't throw on undefined var
- parser error recovery: https://craftinginterpreters.com/statements-and-state.html#parsing-variables
    - try catch in declaration. throw for now?
- bug: 1 == 1 == 1 is false due to (I think):
    - (1 == 1) == 1
    - ( True ) == 1
    - = False
