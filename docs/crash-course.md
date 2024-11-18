# Interpreter crash course

This is being written 5 years after I put down this project. There may be some
mistakes!

# Scanner, parser, grammar
- [scanner](../pylox/scanner.py): scans characters, turns them into tokens
- [tokens](../pylox/token.py): the 'alphabet' of the language. Groups of
  characters that represent things: strings, comments, numbers, operators
- grammar: a definition of valid tokens, expressions and or statements
    - the complete lox grammar is here: https://craftinginterpreters.com/appendix-i.html
    - lexical grammar: defines valid tokens
    - syntax grammar: defines valid declarations, statements, expressions
    - each grammar rule consists of a name -> some symbols
    - symbols can be "terminals" or non-terminals. Terminals are as-is,
      non-terminals can be substituted with any rule of the same name. For
      example:
        - sentence -> "the answer is" answer
        - answer -> "yes" | "no"
    - there are two valid phrases for the above grammar: "the answer is yes",
      "the answer is no"
    - lox's grammar definition uses some regex: * = 0 or more, + = 1 or more etc.
    - for more detail, see https://craftinginterpreters.com/representing-code.html
- [parser](../pylox/parser/parser.py): scans tokens, produces statements,
  expressions, declarations. Compare the parser to the lox grammar - each rule
  is implemented by a function in the parser. The parser is a 'recursive descent
  parser', which according to Wikipedia, closely mirrors the grammar it
  recognises: https://en.wikipedia.org/wiki/Recursive_descent_parser

# Quick walkthrough of executing a statement
Look at the following example of using the repl (`./make.sh lox-repl`):

```
$ ./make.sh lox-repl    # start the repl
> print 1 + 1;          # input this line and press enter
2.0                     # pylox prints the result
```

- `./make.sh lox-repl` starts the [REPL](../pylox/lox.py#L63)
- [_execute](../pylox/lox.py#L34) is the interesting part. It
    - scans characters into tokens
    - parses tokens into statements
    - feeds statements to the [Interpreter](../pylox/interpreter.py)
- token scanning is pretty straightforward, so I won't cover that
- if you set `DEBUG = True` in pylox.py, it will print out the
  tokens, and `(print (+ 1.0 1.0))`
- the parser stores the list of tokens, and works its way through it
  with functions that consume the tokens. If you open up the
  [lox grammar](https://craftinginterpreters.com/appendix-i.html),
  you can follow along with what the parser is doing, starting from `parse`.
- first it tries to consume a declaration. There is none, and I haven't
  implemented the other declarations yet, so it moves onto `statement`.
- `_statement()` eventually reaches `PRINT`, which matches the current
  token, so the print token is consumed, and the parser 'descends' into
  the print statement function.
- a print statement expects an expression, so `_print_statement()` descends
  into `_expression()`.
- hopefully you get it by now. An expression is returned, and
  `_print_statement()` returns a `Print(Statement)` object.
- all tokens have been consumed, so the parser returns the print statement
- the intepreter is given all statements, and executes them one by one:
    - [interpreter.interpret](../pylox/interpreter.py#L19)
- the interpreter contains an 'environment' that stores variables

# Adding a language feature
- add a test to lox_tests.py
- run the test, be guided by the errors. You'll usually go in the following
  order:
- parser: parse code to an expression/statement
    - add the expression/statement type
- interpreter: evaluate the expression/statement
