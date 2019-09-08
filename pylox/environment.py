from __future__ import annotations
from .token import Token


class Environment:
    def __init__(self, parent: Environment=None):
        self.parent = parent
        self.values = {}

    def define(self, name: str, value):
        self.values[name] = value

    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise EnvironmentException(f"Undefined variable {name.lexeme}")

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.parent:
            return self.parent.get(name)
        raise EnvironmentException(f"Undefined variable {name.lexeme}")


class EnvironmentException(Exception):
    def __init__(self, message: str):
        self.message = message
