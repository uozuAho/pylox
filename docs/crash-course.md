# Interpreter crash course

This is being written 5 years after I put down this project. There may be some
mistakes!

# Scanner, parser, grammar
- [scanner](../pylox/scanner.py): scans characters, turns them into tokens
- [tokens](../pylox/token.py): the 'alphabet' of the language. Groups of
  characters that represent things: strings, comments, numbers, operators
- **todo** parser, grammar

# Quick walkthrough of executing a statement
Look at the following example of using the repl (`./make.sh lox-repl`):

```
$ ./make.sh lox-repl    # start the repl
> print 1 + 1;          # input this line and press enter
2.0                     # pylox prints the result
```

How does this work? **todo**
