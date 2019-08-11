class AstPrinter:
    def print(self, expression):
        return expression.accept(self)

    def visit_binary_expression(self, expr):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expression(self, expr):
        return self._parenthesize("group", expr.expression)

    def visit_literal_expression(self, expr):
        if (expr.value == None):
            return "nil"
        return str(expr.value)

    def visit_unary_expression(self, expr):
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name, *expressions):
        output = "(" + name
        for expression in expressions:
            output += " "
            output += expression.accept(self)
        output += ")"

        return output
