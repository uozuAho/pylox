from .parser.expressions import Expression, Literal, Grouping, Unary, Binary
from .token_types import TokenTypes as t
from .token import Token


class Interpreter:
    def visit_binary_expression(self, expr: Binary):
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

    def visit_grouping_expression(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expression(self, expr: Literal):
        return expr.value

    def visit_unary_expression(self, expr: Unary):
        right = self._evaluate(expr.right)

        if expr.operator.type == t.MINUS:
            if type(right) is not float:
                raise InterpreterException(expr, expr.operator, 'operand must be a number')
            return -right
        elif expr.operator.type == t.BANG:
            return not self._is_truthy(right)

        raise Exception("shouldn't get here")

    def _evaluate(self, expr):
        return expr.accept(self)

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

    def _ensure_number_operands(self, expr: Expression, token: Token, left, right):
        if type(left) is float and type(right) is float: return
        raise InterpreterException(expr, token, 'operands must be numbers')


class InterpreterException(Exception):
    def __init__(self, expression: Expression, token: Token, message: str):
        self.expression = expression
        self.token = token
        self.message = message
