from typing import List

from ..token import Token
from .expressions import Expression


class Statement:
    """abstract statement"""

    def accept(self, visitor):
        """Uses visitor pattern to extend statement functionality"""
        pass


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


class Print(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)


class Return(Statement):
    def __init__(self, keyword: Token, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


class FunctionDeclaration(Statement):
    def __init__(self, name: Token, params: List[Token], body: List[Statement]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


class VariableDeclaration(Statement):
    def __init__(self, identifier: Token, initialiser: Expression):
        self.identifier = identifier
        self.initialiser = initialiser

    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


class Block(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)


class If(Statement):
    def __init__(
        self, condition: Expression, thenBranch: Statement, elseBranch: Statement
    ):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor):
        return visitor.visit_if(self)


class While(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)
