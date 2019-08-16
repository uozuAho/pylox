from .parser.expressions import Expression, Literal, Grouping, Unary
from .token_types import TokenTypes as t

class Interpreter:
    def visit_binary_expression(self, expr):
        pass

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
