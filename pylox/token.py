import typing as t

from .token_types import TokenTypes

class Token:
    """ A 'word' of the language. May be one or more characters. For all the
        tokens of lox, see TokenTypes.

        https://craftinginterpreters.com/scanning.html#lexemes-and-tokens

        lexeme:  group of characters that make up the token
        literal: where applicable, the interpreter's representation of the
                 lexeme, eg number values
    """
    def __init__(
            self,
            type: TokenTypes,
            lexeme: str,
            literal: t.Optional[str],  # todo: type: should be Optional[IDENTIFIER | STRING | NUMBER] ?
            line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "{o.type} {o.lexeme} {o.literal}".format(o=self)
