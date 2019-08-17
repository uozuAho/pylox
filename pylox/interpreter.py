from .parser.expressions import Expression, Literal, Grouping, Unary, Binary
from .token_types import TokenTypes as t

class Interpreter:
    def visit_binary_expression(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        # arithmetic
        if expr.operator.type == t.MINUS:
            return left - right
        if expr.operator.type == t.SLASH:
            return left / right
        if expr.operator.type == t.STAR:
            return left * right
        if expr.operator.type == t.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right;
            raise InterpreterException(expr, "invalid operands for binary expression")

        # comparison
        if expr.operator.type == t.GREATER:
            return left > right
        if expr.operator.type == t.GREATER_EQUAL:
            return left >= right
        if expr.operator.type == t.LESS:
            return left < right
        if expr.operator.type == t.LESS_EQUAL:
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
        return left == right


class InterpreterException(Exception):
    def __init__(self, expression: Expression, message: str):
        self.expression = expression
        self.message = message
