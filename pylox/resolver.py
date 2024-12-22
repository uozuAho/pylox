from typing import Dict, List
from pylox.interpreter import Interpreter
from pylox.parser import expressions, statements
from pylox.token import Token


class Resolver:
    """ Resolves variable definitions, eg for the following case:

        ```
        var a = 1;
        {
            var a = 2;
            print(a);   // 2
        }
        print(a);       // 1

        // or

        var a = 1;
        {
            fun showA() {
                print(a);
            }
            showA();   // 1
            var a = 2;
            showA();   // 1 (captured in closure)
        }
        ```

        This resolver is an alternative to creating immutable/persistent
        environments on each variable declaration/definition.

        See https://craftinginterpreters.com/resolving-and-binding.html
    """
    def __init__(self, interpreter: Interpreter):
        self._interpreter = interpreter
        # list[{lexeme(str): is_ready(bool)}]
        self._scopes: List[Dict[str, bool]] = []

    def visit_block(self, stmt: statements.Block):
        self._begin_scope()
        self._resolve_all(stmt.statements)
        self._end_scope()

    def visit_variable_declaration(self, stmt: statements.VariableDeclaration):
        self._declare(stmt.identifier)
        if stmt.initialiser:
            self._resolve(stmt.initialiser)
        self._define(stmt.identifier)

    def visit_variable_expression(self, expr: expressions.Variable):
        if self._scopes and not self._scopes[-1].get(expr.identifier.lexeme):
            raise ResolverException(expr.identifier, "Can't read local variable in its own initialiser")
        self._resolve_local(expr, expr.identifier.lexeme)

    def visit_assignment_expression(self, expr: expressions.Assignment):
        self._resolve_expr(expr.expression)
        self._resolve_local(expr, expr.identifier.lexeme)

    def visit_function_declaration(self, stmt: statements.FunctionDeclaration):
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt)

    def visit_expression_statement(self, stmt: statements.ExpressionStatement):
        self._resolve(stmt.expression)

    def visit_if_statement(self, stmt: statements.If):
        self._resolve(stmt.condition)
        self._resolve(stmt.thenBranch)
        if stmt.elseBranch:
            self._resolve(stmt.elseBranch)

    def visit_print_statement(self, stmt: statements.Print):
        self._resolve(stmt.expression)

    def visit_return_statment(self, stmt: statements.Return):
        if stmt.value:
            self._resolve(stmt.value)

    def visit_while(self, stmt: statements.While):
        self._resolve(stmt.condition)
        self._resolve(stmt.body)

    def visit_binary_expression(self, expr: expressions.Binary):
        self._resolve(expr.left)
        self._resolve(expr.right)

    def visit_call_expression(self, expr: expressions.Call):
        self._resolve(expr.callee)
        for arg in expr.args:
            self._resolve(arg)

    def visit_grouping_expression(self, expr: expressions.Grouping):
        self._resolve(expr.expression)

    def visit_literal_expression(self, expr: expressions.Literal):
        pass

    def visit_logical_expression(self, expr: expressions.Logical):
        self._resolve(expr.left)
        self._resolve(expr.right)

    def visit_unary_expression(self, expr: expressions.Unary):
        self._resolve(expr.right)

    def _resolve_local(self, expr: expressions.Expression, name: str):
        irev = reversed(range(len(self._scopes)))
        for i in irev:
            if name in self._scopes[i]:
                self._interpreter.resolve(expr, len(self._scopes) - 1 - i)
                return

    def _resolve_all(self, stmts: List[statements.Statement]):
        for s in stmts:
            self._resolve(s)

    def _resolve(self, thing: statements.Statement | expressions.Expression):
        thing.accept(self)

    def _resolve_expr(self, expr: expressions.Expression):
        expr.accept(self)

    def _resolve_function(self, func: statements.FunctionDeclaration):
        self._begin_scope()
        for param in func.params:
            self._declare(param)
            self._define(param)
        self._resolve_all(func.body)
        self._end_scope()

    def _begin_scope(self):
        self._scopes.append({})

    def _end_scope(self):
        self._scopes.pop()

    def _declare(self, name: Token):
        if len(self._scopes) == 0:
            return
        scope = self._scopes[-1]
        scope[name.lexeme] = False

    def _define(self, name: Token):
        if len(self._scopes) == 0:
            return
        scope = self._scopes[-1]
        scope[name.lexeme] = True


class ResolverException(Exception):
    def __init__(self, token: Token, msg: str, *args):
        super().__init__(*args)
        self.token = token
        self.msg = msg
