from typing import Iterator, List

from . import expressions
from . import statements
from ..token_types import TokenTypes as t
from ..token import Token


class Parser:
    def __init__(self, tokens):
        ignore_tokens = [t.COMMENT, t.WHITESPACE, t.NEWLINE]
        self.tokens = [tk for tk in tokens if tk.type not in ignore_tokens]
        self.current_idx = 0

    def parse(self) -> Iterator[statements.Statement]:
        while not self._is_finished():
            yield self._declaration()

    def _declaration(self):
        if self._consume_if(t.VAR):
            return self._var_declaration()
        return self._statement()

    def _var_declaration(self):
        identifier = self._consume(t.IDENTIFIER, "expected variable name")
        expression = None
        if self._consume_if(t.EQUAL):
            expression = self._expression()
        self._consume(t.SEMICOLON, "expected ';' after variable declaration")
        return statements.VariableDeclaration(identifier, expression)

    def _statement(self):
        if self._consume_if(t.IF):
            return self._if_statement()
        if self._consume_if(t.WHILE):
            return self._while_statement()
        if self._consume_if(t.PRINT):
            return self._print_statement()
        if self._consume_if(t.LEFT_BRACE):
            return statements.Block(self._block())
        return self._expression_statement()

    def _if_statement(self):
        self._consume(t.LEFT_PAREN, "Expected '(' after 'if'.")
        condition = self._expression()
        self._consume(t.RIGHT_PAREN, "Expected ')' after if condition.")

        then_branch = self._statement()
        else_branch = None
        if self._consume_if(t.ELSE):
            else_branch = self._statement()

        return statements.If(condition, then_branch, else_branch)

    def _while_statement(self):
        self._consume(t.LEFT_PAREN, "Expected '(' after 'while'.")
        condition = self._expression()
        self._consume(t.RIGHT_PAREN, "Expected ')' after while condition.")

        body = self._statement()
        return statements.While(condition, body)

    def _block(self) -> List[statements.Statement]:
        stmts = []

        while not self._current_token_is(t.RIGHT_BRACE) and not self._is_finished():
            stmts.append(self._declaration())

        self._consume(t.RIGHT_BRACE, "Expected '}' after block.")
        return stmts

    def _print_statement(self):
        expr = self._expression()
        self._consume(t.SEMICOLON, "expected ';' after expression")
        return statements.Print(expr)

    def _expression_statement(self):
        expr = self._expression()
        self._consume(t.SEMICOLON, "expected ';' after expression")
        return statements.Expression(expr)

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        expression = self._or()

        if self._consume_if(t.EQUAL):
            equals = self._previous_token()
            value = self._assignment()
            if isinstance(expression, expressions.Variable):
                identifier = expression.identifier
                return expressions.Assignment(identifier, value)

            raise ParserException(equals, "Invalid assignment target.")

        return expression

    def _or(self):
        expression = self._and()

        while self._consume_if(t.OR):
            operator = self._previous_token()
            right = self._and()
            expression = expressions.Logical(expression, operator, right)

        return expression

    def _and(self):
        expression = self._equality()

        while self._consume_if(t.AND):
            operator = self._previous_token()
            right = self._equality()
            expression = expressions.Logical(expression, operator, right)

        return expression

    def _equality(self):
        expression = self._comparison()

        while self._consume_if(t.BANG_EQUAL, t.EQUAL_EQUAL):
            operator = self._previous_token()
            right = self._comparison()
            expression = expressions.Binary(expression, operator, right)

        return expression

    def _comparison(self):
        expression = self._addition()

        while self._consume_if(t.GREATER, t.GREATER_EQUAL, t.LESS, t.LESS_EQUAL):
            operator = self._previous_token()
            right = self._addition()
            expression = expressions.Binary(expression, operator, right)

        return expression

    def _addition(self):
        expression = self._multiplication()

        while self._consume_if(t.MINUS, t.PLUS):
            operator = self._previous_token()
            right = self._multiplication()
            expression = expressions.Binary(expression, operator, right)

        return expression

    def _multiplication(self):
        expression = self._unary()

        while self._consume_if(t.SLASH, t.STAR):
            operator = self._previous_token()
            right = self._unary()
            expression = expressions.Binary(expression, operator, right)

        return expression

    def _unary(self):
        if self._consume_if(t.BANG, t.MINUS):
            operator = self._previous_token()
            right = self._unary()
            return expressions.Unary(operator, right)

        return self._primary()

    def _primary(self):
        if self._consume_if(t.FALSE):
            return expressions.Literal(False)
        if self._consume_if(t.TRUE):
            return expressions.Literal(True)
        if self._consume_if(t.NIL):
            return expressions.Literal(None)

        if self._consume_if(t.NUMBER, t.STRING):
            return expressions.Literal(self._previous_token().literal)

        if self._consume_if(t.IDENTIFIER):
            return expressions.Variable(self._previous_token())

        if self._consume_if(t.LEFT_PAREN):
            expression = self._expression()
            self._consume(t.RIGHT_PAREN, "Expected ')' after expression")
            return expressions.Grouping(expression)

        raise ParserException(self._current_token(), "Expected expression")

    def _consume(self, token_type, error_message) -> Token:
        if self._current_token_is(token_type):
            return self._consume_current_token()

        raise ParserException(self._current_token(), error_message)

    def _consume_if(self, *token_types) -> bool:
        for type in token_types:
            if self._current_token_is(type):
                self._consume_current_token()
                return True
        return False

    def _current_token_is(self, token_type):
        if self._is_finished():
            return False
        return self._current_token().type == token_type

    def _consume_current_token(self) -> Token:
        if not self._is_finished():
            self.current_idx += 1
        return self._previous_token()

    def _is_finished(self):
        return self._current_token().type == t.EOF

    def _current_token(self) -> Token:
        return self.tokens[self.current_idx]

    def _previous_token(self) -> Token:
        return self.tokens[self.current_idx - 1]

    def _synchronise(self):
        self._consume_current_token()

        while not self._is_finished():
            if self._previous_token() == t.SEMICOLON:
                return

            if self._current_token().type in [
                t.CLASS,
                t.FUN,
                t.VAR,
                t.FOR,
                t.IF,
                t.WHILE,
                t.PRINT,
                t.RETURN,
            ]:
                return

            self._consume_current_token()


class ParserException(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
