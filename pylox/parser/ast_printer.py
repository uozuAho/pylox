from .statements import ExpressionStatement, PrintStatement


class AstPrinter:

    def to_string(self, expression):
        return expression.accept(self)

    def print(self, expression):
        print(self.to_string(expression))

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

    def visit_expression_statement(self, stmt: ExpressionStatement):
        return stmt.expression.accept(self)

    def visit_print_statement(self, stmt: PrintStatement):
        return self._parenthesize('print', stmt.expression)

    def _parenthesize(self, name, *expressions) -> str:
        output = "(" + name
        for expression in expressions:
            output += " "
            output += expression.accept(self)
        output += ")"

        return output
