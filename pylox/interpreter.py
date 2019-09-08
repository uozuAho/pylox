from typing import Iterable

from .parser import expressions as expr
from .parser import statements as stmt
from .token_types import TokenTypes as t
from .token import Token
from .io import OutputStream, StdOutputStream
from .environment import Environment


class Interpreter:
    def __init__(self, output: OutputStream=None, environment: Environment=None):
        self.out = output or StdOutputStream()
        self.env = environment or Environment()

    def interpret(self, statements: Iterable[stmt.Statement]):
        for statement in statements:
            self._execute(statement)

    def visit_variable_declaration(self, stmt: stmt.VariableDeclaration):
        value = None
        if stmt.initialiser:
            value = self._evaluate(stmt.initialiser)
        self.env.define(stmt.identifier.lexeme, value)

    def visit_assignment_expression(self, expr: expr.Assignment):
        # ensure var exists
        self.env.get(expr.identifier)
        value = self._evaluate(expr.expression)
        # todo: make a set method
        self.env.define(expr.identifier.lexeme, value)

    def visit_variable_expression(self, expr: expr.Variable):
        return self.env.get(expr.identifier)

    def visit_expression_statement(self, stmt: stmt.Expression):
        self._evaluate(stmt.expression)

    def visit_print_statement(self, stmt: stmt.Print):
        value = self._evaluate(stmt.expression)
        if value is None:
            value = 'nil'
        self.out.send(value)

    def visit_binary_expression(self, expr: expr.Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        # arithmetic
        if expr.operator.type == t.MINUS:
            self._ensure_number_operands(expr, expr.operator, left, right)
            return left - right
        if expr.operator.type == t.SLASH:
            self._ensure_number_operands(expr, expr.operator, left, right)
            return left / right
        if expr.operator.type == t.STAR:
            self._ensure_number_operands(expr, expr.operator, left, right)
            return left * right
        if expr.operator.type == t.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right;
            raise InterpreterException(expr, expr.operator, 'invalid operands for binary expression')

        # comparison
        if expr.operator.type == t.GREATER:
            self._ensure_number_operands(expr, expr.operator, left, right)
            return left > right
        if expr.operator.type == t.GREATER_EQUAL:
            self._ensure_number_operands(expr, expr.operator, left, right)
            return left >= right
        if expr.operator.type == t.LESS:
            self._ensure_number_operands(expr, expr.operator, left, right)
            return left < right
        if expr.operator.type == t.LESS_EQUAL:
            self._ensure_number_operands(expr, expr.operator, left, right)
            return left <= right
        if expr.operator.type == t.BANG_EQUAL:
            return not self._is_equal(left, right)
        if expr.operator.type == t.EQUAL_EQUAL:
            return self._is_equal(left, right)

        raise Exception("shouldn't get here")

    def visit_grouping_expression(self, expr: expr.Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expression(self, expr: expr.Literal):
        return expr.value

    def visit_unary_expression(self, expr: expr.Unary):
        right = self._evaluate(expr.right)

        if expr.operator.type == t.MINUS:
            if type(right) is not float:
                raise InterpreterException(expr, expr.operator, 'operand must be a number')
            return -right
        elif expr.operator.type == t.BANG:
            return not self._is_truthy(right)

        raise Exception("shouldn't get here")

    def _execute(self, statement: stmt.Statement):
        statement.accept(self)

    def _evaluate(self, expression: expr.Expression):
        return expression.accept(self)

    def _is_truthy(self, object):
        if object is None: return False
        if isinstance(object, bool): return object
        return True

    def _is_equal(self, left, right):
        if left is None and right is None:
            return True
        if left is None:
            return False
        if type(left) is not type(right):
            return False
        return left == right

    def _ensure_number_operands(self, expr: expr.Expression, token: Token, left, right):
        if type(left) is float and type(right) is float: return
        raise InterpreterException(expr, token, 'operands must be numbers')


class InterpreterException(Exception):
    def __init__(self, expression: expr.Expression, token: Token, message: str):
        self.expression = expression
        self.token = token
        self.message = message
