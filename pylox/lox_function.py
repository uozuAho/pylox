from pylox.callable import Callable
from pylox.environment import Environment
from pylox.interpreter import Interpreter
from pylox.parser import statements


class LoxFunction(Callable):
    def __init__(self, declaration: statements.FunctionDeclaration):
        self._declaration = declaration

    def call(self, interpreter: Interpreter, args):
        env = Environment(interpreter.globals)
        for p in self._declaration.params:
            env.define(p.lexeme, p)
        interpreter.execute_block(self._declaration.body, env)
        return None

    def __repr__(self):
        return f'<fn {self._declaration.name.lexeme}>'
