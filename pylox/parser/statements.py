# from ..token import Token
from .expressions import Expression


class Statement:
    """ abstract statement """

    def accept(self, visitor):
        """ Uses visitor pattern to extend statement functionality """
        pass

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

class PrintStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)
