from .token import Token


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value):
        self.values[name] = value

    def assign(self, name: Token, value):
        if name.lexeme not in self.values:
            raise Exception(f"Undefined variable {name.lexeme}")
        self.values[name.lexeme] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise Exception(f"Undefined variable {name.lexeme}")
