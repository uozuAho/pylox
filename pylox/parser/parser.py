from .expressions import Binary, Unary, Literal, Grouping
from ..token_types import TokenTypes as t


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_idx = 0

    def parse(self):
        try:
            return self._expression()
        except ParserException as e:
            print(e)
            return None

    def _expression(self):
        return self._equality()

    def _equality(self):
        expression = self._comparison()

        while self._consume_if(t.BANG_EQUAL, t.BANG):
            operator = self._previous_token()
            right = self._comparison()
            expression = Binary(expression, operator, right)

        return expression

    def _comparison(self):
        expression = self._addition()

        while self._consume_if(t.GREATER, t.GREATER_EQUAL, t.LESS, t.LESS_EQUAL):
            operator = self._previous_token()
            right = self._addition()
            expression = Binary(expression, operator, right)

        return expression

    def _addition(self):
        expression = self._multiplication()

        while self._consume_if(t.MINUS, t.PLUS):
            operator = self._previous_token()
            right = self._multiplication()
            expression = Binary(expression, operator, right)

        return expression

    def _multiplication(self):
        expression = self._unary()

        while self._consume_if(t.SLASH, t.STAR):
            operator = self._previous_token()
            right = self._unary()
            expression = Binary(expression, operator, right)

        return expression

    def _unary(self):
        if self._consume_if(t.BANG, t.MINUS):
            operator = self._previous_token()
            right = self._unary()
            return Unary(operator, right)

        return self._primary()

    def _primary(self):
        if self._consume_if(t.FALSE):
            return Literal(False)
        if self._consume_if(t.TRUE):
            return Literal(True)
        if self._consume_if(t.NIL):
            return Literal(None)

        if self._consume_if(t.NUMBER, t.STRING):
            return Literal(self._previous_token().literal)

        if self._consume_if(t.LEFT_PAREN):
            expression = self._expression()
            self._consume(t.RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expression)

        raise ParserException(self._current_token(), "Expected expression")

    def _consume(self, token_type, error_message):
        if self._current_token_is(token_type):
            return self._consume_current_token()

        raise ParserException(self._current_token(), error_message)

    def _consume_if(self, *token_types):
        for type in token_types:
            if self._current_token_is(type):
                self._consume_current_token()
                return True
        return False

    def _current_token_is(self, token_type):
        if self._is_finished():
            return False
        return self._current_token().type == token_type

    def _consume_current_token(self):
        if not self._is_finished():
            self.current_idx += 1
        return self._previous_token()

    def _is_finished(self):
        return self._current_token().type == t.EOF

    def _current_token(self):
        return self.tokens[self.current_idx]

    def _previous_token(self):
        return self.tokens[self.current_idx - 1]

    def _synchronise(self):
        self._consume_current_token()

        while not self._is_finished():
            if self._previous_token() == t.SEMICOLON:
                return

            current_token_type = self._current_token().type
            if self._current_token().type in [
                t.CLASS,
                t.FUN,
                t.VAR,
                t.FOR,
                t.IF,
                t.WHILE,
                t.PRINT,
                t.RETURN
            ]:
                return

            self._consume_current_token()


class ParserException(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
