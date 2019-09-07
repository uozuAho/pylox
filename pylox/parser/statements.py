from ..token import Token
from .expressions import Expression


class Statement:
    """ abstract statement """

    def accept(self, visitor):
        """ Uses visitor pattern to extend statement functionality """
        pass

class Expression(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

class Print(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)

class VariableDeclaration(Statement):
    def __init__(self, identifier: Token, expression: Expression):
        self.identifier = identifier
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_variable(self)
