from pylox.callable import Callable
from pylox.environment import Environment
from pylox.parser import statements
from pylox.return_exception import ReturnException


class LoxFunction(Callable):
    def __init__(
        self, declaration: statements.FunctionDeclaration, closure: Environment
    ):
        self._declaration = declaration
        self._closure = closure

    def call(self, interpreter, args):
        env = Environment(self._closure)
        for i, p in enumerate(self._declaration.params):
            env.define(p.lexeme, args[i])
        try:
            interpreter.execute_block(self._declaration.body, env)
        except ReturnException as r:
            return r.value
        return None

    def arity(self):
        return len(self._declaration.params)

    def __repr__(self):
        return f"<fn {self._declaration.name.lexeme}>"
