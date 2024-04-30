from ..token import Token


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
        if type(value) is int:
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
