import unittest
from pylox.environment import Environment, EnvironmentException
from pylox.token import Token
from pylox.token_types import TokenTypes as t


def var_token(name: str) -> Token:
    return Token(t.IDENTIFIER, name, name, 1)


class EnvironmentTests(unittest.TestCase):

    def test_define_and_get(self):
        env = Environment()
        env.define('a', 1)
        val = env.get(var_token('a'))
        self.assertEqual(val, 1)

    def test_define_assign_and_get(self):
        env = Environment()
        env.define('a', 1)
        env.assign(var_token('a'), 2)
        val = env.get(var_token('a'))
        self.assertEqual(val, 2)

    def test_get_undefined_throws(self):
        env = Environment()
        with self.assertRaises(EnvironmentException):
            env.get(var_token('asdf'))