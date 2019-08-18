# pylox interpreter

My first implementation of lox from https://craftinginterpreters.com,
using python.

# todo

- lox: merge run_str and _run
- lox: refactor, extract prompt runner
- bug: 1 == 1 == 1 is false due to (I think):
    - (1 == 1) == 1
    - ( True ) == 1
    - = False

# fun stuff for later

- python to javascript
    - try first, then look for existing tools
- python to webassembly
- c# to webassembly
    - what does blazor do?