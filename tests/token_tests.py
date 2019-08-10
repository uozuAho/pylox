import unittest

from pylox.token import Token
from pylox.token_types import TokenTypes

class TokenTests(unittest.TestCase):

    def test_string1(self):
        token = Token(TokenTypes.LEFT_PAREN, 'asdf', 'noo', 34)
        self.assertEqual('TokenTypes.LEFT_PAREN asdf noo', str(token))

    def test_string2(self):
        token = Token(TokenTypes.RIGHT_PAREN, 'bert', 'ernie', 34)
        self.assertEqual('TokenTypes.RIGHT_PAREN bert ernie', str(token))
