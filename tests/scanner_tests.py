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

    def test_not_equal_greater(self):
        scanner = Scanner('!=>')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenTypes.BANG_EQUAL)
        self.assertEqual(tokens[1].type, TokenTypes.GREATER)

    def test_not_equal_greater_equal(self):
        scanner = Scanner('!=>=')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenTypes.BANG_EQUAL)
        self.assertEqual(tokens[1].type, TokenTypes.GREATER_EQUAL)

    def test_div_equal(self):
        scanner = Scanner('/=')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenTypes.SLASH)
        self.assertEqual(tokens[1].type, TokenTypes.EQUAL)

class ScannerTest_Comments(unittest.TestCase):

    def test_slash_slash(self):
        scanner = Scanner('//')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.COMMENT)
        self.assertEqual(tokens[0].lexeme, '//')
        self.assertEqual(tokens[0].literal, '')
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_a_comment(self):
        scanner = Scanner('// a comment')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.COMMENT)
        self.assertEqual(tokens[0].lexeme, '// a comment')
        self.assertEqual(tokens[0].literal, ' a comment')
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

class ScannerTest_Whitespace(unittest.TestCase):

    def test_single_space(self):
        scanner = Scanner(' ')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.WHITESPACE)
        self.assertEqual(tokens[0].lexeme, ' ')
        self.assertEqual(tokens[0].literal, ' ')
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_multiple_whitespace(self):
        whitespace_text = '    \r\t\t\t'
        scanner = Scanner(whitespace_text)

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.WHITESPACE)
        self.assertEqual(tokens[0].lexeme, whitespace_text)
        self.assertEqual(tokens[0].literal, whitespace_text)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

class ScannerTest_Newlines(unittest.TestCase):

    def test_single_newline(self):
        scanner = Scanner('\n')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.NEWLINE)
        self.assertEqual(tokens[0].lexeme, '\n')
        self.assertEqual(tokens[0].literal, None)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_two_newlines(self):
        scanner = Scanner('\n\n')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenTypes.NEWLINE)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.NEWLINE)
        self.assertEqual(tokens[1].line, 2)

    def test_operators_and_newlines(self):
        scanner = Scanner('.\n.\n\n.')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 7)
        self.assertEqual(tokens[0].type, TokenTypes.DOT)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.NEWLINE)
        self.assertEqual(tokens[1].line, 1)
        self.assertEqual(tokens[2].type, TokenTypes.DOT)
        self.assertEqual(tokens[2].line, 2)
        self.assertEqual(tokens[3].type, TokenTypes.NEWLINE)
        self.assertEqual(tokens[3].line, 2)
        self.assertEqual(tokens[4].type, TokenTypes.NEWLINE)
        self.assertEqual(tokens[4].line, 3)
        self.assertEqual(tokens[5].type, TokenTypes.DOT)
        self.assertEqual(tokens[5].line, 4)
        self.assertEqual(tokens[6].type, TokenTypes.EOF)