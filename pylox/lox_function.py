from pylox.callable import Callable
from pylox.environment import Environment
from pylox.parser import statements


class LoxFunction(Callable):
    def __init__(self, declaration: statements.FunctionDeclaration):
        self._declaration = declaration

    def call(self, interpreter, args):
        env = Environment(interpreter.globals)
        for i, p in enumerate(self._declaration.params):
            env.define(p.lexeme, args[i])
        interpreter.execute_block(self._declaration.body, env)
        return None

    def arity(self):
        return len(self._declaration.params)

    def __repr__(self):
        return f'<fn {self._declaration.name.lexeme}>'
