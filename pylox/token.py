import typing as t

from .token_types import TokenTypes

class Token:
    def __init__(
            self,
            type: TokenTypes,
            lexeme: t.Optional[str],
            literal: t.Optional[str],
            line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "{o.type} {o.lexeme} {o.literal}".format(o=self)
