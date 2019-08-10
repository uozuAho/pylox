import unittest

from pylox.scanner import Scanner
from pylox.token_types import TokenTypes

class ScannerTest(unittest.TestCase):

    def test_single_left_paren(self):
        scanner = Scanner('(')
        tokens = list(scanner.scan_tokens())

        self.assertEqual(2, len(tokens))

        token0 = tokens[0]
        self.assertEqual(TokenTypes.LEFT_PAREN, token0.type)
        self.assertEqual('(', token0.lexeme)
        self.assertEqual(None, token0.literal)
        self.assertEqual(1, token0.line)

        token1 = tokens[1]
        self.assertEqual(TokenTypes.EOF, token1.type)
