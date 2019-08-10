from .token import Token
from .token_types import TokenTypes

class Scanner:
    def __init__(self, bytes):
        self.bytes = bytes
        self.start_idx = 0
        self.current_idx  = 0
        self.line = 1

    def scan_tokens(self):
        while not self._is_finished():
            self.start_idx = self.current_idx;
            yield self._scan_next_token();
        yield Token(TokenTypes.EOF, '', None, self.line)

    def _is_finished(self):
        return self.current_idx >= len(self.bytes)

    def _scan_next_token(self):
        first_char = self._next_char();

        if first_char in UNAMBIGUOUS_SINGLE_CHARS:
            return self._create_token(UNAMBIGUOUS_SINGLE_CHARS[first_char])
        elif first_char == '!':
            if self._advance_if('='):
                return self._create_token(TokenTypes.BANG_EQUAL)
            else:
                return self._create_token(TokenTypes.BANG)
        elif first_char == '=':
            if self._advance_if('='):
                return self._create_token(TokenTypes.EQUAL_EQUAL)
            else:
                return self._create_token(TokenTypes.EQUAL)
        elif first_char == '<':
            if self._advance_if('='):
                return self._create_token(TokenTypes.LESS_EQUAL)
            else:
                return self._create_token(TokenTypes.LESS)
        elif first_char == '>':
            if self._advance_if('='):
                return self._create_token(TokenTypes.GREATER_EQUAL)
            else:
                return self._create_token(TokenTypes.GREATER)
        else:
            message = 'unexpected character "{}" at line {}'.format(first_char, self.line)
            return ScannerError(self.line, message)

    def _next_char(self):
        self.current_idx += 1
        return self.bytes[self.current_idx - 1]

    def _advance_if(self, char):
        if self._is_finished():
            return False
        if self.bytes[self.current_idx] != char:
            return False

        self.current_idx += 1
        return True

    def _create_token(self, type, literal=None):
        text = str(self.bytes[self.start_idx:self.current_idx])
        return Token(type, text, literal, self.line)


class ScannerError:
    def __init__(self, line, message):
        self.line = line
        self.message = message


UNAMBIGUOUS_SINGLE_CHARS = {
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
