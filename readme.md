# pylox interpreter

My first implementation of lox from https://craftinginterpreters.com,
using python.

# todo

- lox repl to use output stream
- bug: double output in repl
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