from ..token import Token
from typing import List


class Expression:
    """abstract expression"""

    def accept(self, visitor):
        """Uses visitor pattern to extend expression functionality"""
        pass


class Binary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


class Grouping(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expression(self)


class Literal(Expression):
    def __init__(self, value):
        if type(value) is int:  # noqa: E721   # for some reason, isinstance breaks this
            self.value = float(value)
        else:
            self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expression(self)


class Unary(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


class Variable(Expression):
    def __init__(self, identifier: Token):
        self.identifier = identifier

    def accept(self, visitor):
        return visitor.visit_variable_expression(self)


class Assignment(Expression):
    def __init__(self, identifier: Token, expression: Expression):
        self.identifier = identifier
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)


class Logical(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expression(self)


class Call(Expression):
    def __init__(
        self, callee: Expression, closing_paren: Token, args: List[Expression]
    ):
        self.callee = callee
        self.closing_paren = closing_paren
        self.args = args

    def accept(self, visitor):
        return visitor.visit_call(self)
