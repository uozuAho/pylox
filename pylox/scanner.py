from .token import Token
from .token_types import TokenTypes

class Scanner:
    def __init__(self, bytes):
        self.bytes = bytes
        self.start = 0
        self.current  = 0
        self.line = 1

    def scan_tokens(self):
        while not self._is_finished():
            self.start = self.current;
            yield self._scan_next_token();
        yield Token(TokenTypes.EOF, '', None, self.line)

    def _is_finished(self):
        return self.current >= len(self.bytes)

    def _scan_next_token(self):
        c = self._advance();

        single_chars = {
            '(': TokenTypes.LEFT_PAREN,
            ')': TokenTypes.RIGHT_PAREN,
            '{': TokenTypes.LEFT_BRACE,
            '}': TokenTypes.RIGHT_BRACE,
            ',': TokenTypes.COMMA,
            '.': TokenTypes.DOT,
            '-': TokenTypes.MINUS,
            '+': TokenTypes.PLUS,
            ';': TokenTypes.SEMICOLON,
            '/': TokenTypes.SLASH,
            '*': TokenTypes.STAR,
        }

        if c in single_chars:
            return self._create_token(single_chars[c])

        # todo: return scanner error (don't throw)

    def _advance(self):
        self.current += 1
        return self.bytes[self.current - 1]

    def _create_token(self, type, literal=None):
        text = str(self.bytes[self.start:self.current])
        return Token(type, text, literal, self.line)
