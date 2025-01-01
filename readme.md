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

# run lox
./make.sh lox [lox_file]
# example
./make.sh lox tests/lox_test_file.lox
```

# crash course
See the [crash course](/docs/crash-course.md)

# useful docs
- [lox grammar](https://craftinginterpreters.com/appendix-i.html)

# todo
- do next: classes: https://craftinginterpreters.com/classes.html
- repl: parameter for debug verbosity on/off
- repl: don't throw on undefined var
- parser error recovery: https://craftinginterpreters.com/statements-and-state.html#parsing-variables
    - try catch in declaration. throw for now?
- bug: 1 == 1 == 1 is false due to (I think):
    - (1 == 1) == 1
    - ( True ) == 1
    - = False
