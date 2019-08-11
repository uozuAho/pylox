from .token import Token
from .token_types import TokenTypes

class Scanner:
    def __init__(self, bytes):
        self.bytes = bytes
        self.start_idx = 0
        self.current_idx  = 0
        self.line_num = 1

    def scan_tokens(self):
        while not self._is_finished():
            self.start_idx = self.current_idx;
            yield self._consume_token();
        yield Token(TokenTypes.EOF, '', None, self.line_num)

    def _is_finished(self):
        return self.current_idx >= len(self.bytes)

    def _consume_token(self):
        first_char = self._consume_next_char();

        if first_char in UNAMBIGUOUS_SINGLE_CHARS:
            return self._create_token(UNAMBIGUOUS_SINGLE_CHARS[first_char])
        elif first_char in REMAINING_OPERATORS:
            return self._consume_remaining_operators_token(first_char)
        elif first_char in WHITESPACE:
            return self._consume_whitespace_token()
        elif first_char == NEWLINE:
            token = self._create_token(TokenTypes.NEWLINE)
            self.line_num += 1
            return token
        elif first_char == '"':
            return self._consume_string_token()
        elif first_char.isdigit():
            return self._consume_number_token()
        elif first_char.isalpha():
            return self._consume_identifier_token()
        else:
            message = 'unexpected character "{}" at line {}'.format(first_char, self.line_num)
            return ScannerError(self.line_num, message)

    def _consume_remaining_operators_token(self, first_char):
        if first_char == '!':
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
        elif first_char == '/':
            if self._advance_if('/'):
                while self._peek() != '\n' and not self._is_finished():
                    self._consume_next_char()
                comment_text = self.bytes[self.start_idx + 2:self.current_idx]
                return self._create_token(TokenTypes.COMMENT, comment_text)
            else:
                return self._create_token(TokenTypes.SLASH)

        raise Exception("Shouldn't get here")

    def _consume_whitespace_token(self):
        while self._peek() in WHITESPACE and not self._is_finished():
            self._consume_next_char()
        whitespace_text = self.bytes[self.start_idx:self.current_idx]
        return self._create_token(TokenTypes.WHITESPACE, whitespace_text)

    def _consume_string_token(self):
        while self._peek() != '"' and not self._is_finished():
            if self._peek() == '\n':
                self.line_num += 1
            self._consume_next_char()

        if self._is_finished():
            message = 'unterminated string at line {}'.format(self.line_num)
            return ScannerError(self.line_num, message)

        # consume the closing "
        self._consume_next_char()

        string_value = self.bytes[self.start_idx + 1 : self.current_idx - 1]
        return self._create_token(TokenTypes.STRING, string_value)

    def _consume_number_token(self):
        while self._peek().isdigit():
            self._consume_next_char()

        if self._peek() == '.' and self._peek(1).isdigit():
            # consume decimal point
            self._consume_next_char()
            # continue consuming numbers
            while self._peek().isdigit():
                self._consume_next_char()

        value = self.bytes[self.start_idx : self.current_idx]
        return self._create_token(TokenTypes.NUMBER, value)

    def _consume_identifier_token(self):
        def is_alnum_or_underscore(char):
            return char.isalnum() or char == '_'

        while is_alnum_or_underscore(self._peek()):
            self._consume_next_char()

        value = self.bytes[self.start_idx : self.current_idx]

        type = TokenTypes.IDENTIFIER
        if value in KEYWORDS:
            type = KEYWORDS[value]

        return self._create_token(type)

    def _consume_next_char(self):
        self.current_idx += 1
        return self.bytes[self.current_idx - 1]

    def _advance_if(self, char):
        if self._is_finished():
            return False
        if self.bytes[self.current_idx] != char:
            return False

        self.current_idx += 1
        return True

    def _peek(self, offset=0):
        idx = self.current_idx + offset
        if idx >= len(self.bytes):
            return '\0'
        return self.bytes[idx]

    def _create_token(self, type, literal=None):
        text = str(self.bytes[self.start_idx:self.current_idx])
        return Token(type, text, literal, self.line_num)


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
    '*': TokenTypes.STAR,
}

REMAINING_OPERATORS = '!=<>/'

WHITESPACE = ' \r\t'

NEWLINE = '\n'

KEYWORDS = {
    'and':    TokenTypes.AND,
    'class':  TokenTypes.CLASS,
    'else':   TokenTypes.ELSE,
    'false':  TokenTypes.FALSE,
    'for':    TokenTypes.FOR,
    'fun':    TokenTypes.FUN,
    'if':     TokenTypes.IF,
    'nil':    TokenTypes.NIL,
    'or':     TokenTypes.OR,
    'print':  TokenTypes.PRINT,
    'return': TokenTypes.RETURN,
    'super':  TokenTypes.SUPER,
    'this':   TokenTypes.THIS,
    'true':   TokenTypes.TRUE,
    'var':    TokenTypes.VAR,
    'while':  TokenTypes.WHILE,
}
