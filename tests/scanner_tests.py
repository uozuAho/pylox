import unittest

from pylox.scanner import Scanner, ScannerError
from pylox.token_types import TokenTypes

class ScannerTest_UnambiguousSingleCharTokens(unittest.TestCase):

    def test_single_left_paren(self):
        scanner = Scanner('(')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)

        self.assertEqual(tokens[0].type, TokenTypes.LEFT_PAREN)
        self.assertEqual(tokens[0].lexeme, '(')
        self.assertEqual(tokens[0].literal, None)
        self.assertEqual(tokens[0].line, 1)

        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_multiple_single_char_tokens(self):
        scanner = Scanner('(-*')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0].type, TokenTypes.LEFT_PAREN)
        self.assertEqual(tokens[1].type, TokenTypes.MINUS)
        self.assertEqual(tokens[2].type, TokenTypes.STAR)
        self.assertEqual(tokens[3].type, TokenTypes.EOF)

    def test_single_invalid_char_should_return_scanner_error(self):
        scanner = Scanner('@')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], ScannerError)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

class ScannerTest_OperatorTokens(unittest.TestCase):

    def test_not(self):
        scanner = Scanner('!')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.BANG)

    def test_not_equal(self):
        scanner = Scanner('!=')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.BANG_EQUAL)
