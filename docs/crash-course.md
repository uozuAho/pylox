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
  is implemented by a function in the parser

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
