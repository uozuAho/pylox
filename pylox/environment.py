from __future__ import annotations
from .token import Token
import typing as t


class Environment:
    def __init__(self, parent: t.Optional[Environment] = None):
        self.parent = parent
        self.values: t.Dict[str, t.Any] = {}

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

    def assign_at(self, distance: int, name: Token, value):
        self._ancestor(distance).values[name.lexeme] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.parent:
            return self.parent.get(name)
        raise EnvironmentException(f"Undefined variable {name.lexeme}")

    def get_at(self, distance, name: str):
        return self._ancestor(distance).values.get(name)

    def _ancestor(self, distance: int):
        env = self
        for _ in range(distance):
            if env.parent:
                env = env.parent
            else:
                raise EnvironmentException("too far!")
        return env


class EnvironmentException(Exception):
    def __init__(self, message: str):
        self.message = message
