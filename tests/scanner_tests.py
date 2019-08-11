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
        self.assertEqual(tokens[0].literal, None)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_multiple_whitespace(self):
        whitespace_text = '    \r\t\t\t'
        scanner = Scanner(whitespace_text)

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.WHITESPACE)
        self.assertEqual(tokens[0].lexeme, whitespace_text)
        self.assertEqual(tokens[0].literal, None)
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

class ScannerTest_Strings(unittest.TestCase):

    def test_single_empty_string(self):
        scanner = Scanner('""')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.STRING)
        self.assertEqual(tokens[0].lexeme, '""')
        self.assertEqual(tokens[0].literal, '')
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_single_nonempty_string(self):
        scanner = Scanner('"asdf"')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.STRING)
        self.assertEqual(tokens[0].lexeme, '"asdf"')
        self.assertEqual(tokens[0].literal, 'asdf')
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_unterminated_string(self):
        scanner = Scanner('"this string is missing a trailing quote')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], ScannerError)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_string_with_newlines(self):
        scanner = Scanner('"this string is \nover two lines"')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.STRING)
        self.assertEqual(tokens[0].lexeme, '"this string is \nover two lines"')
        self.assertEqual(tokens[0].literal, 'this string is \nover two lines')
        self.assertEqual(tokens[0].line, 2)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

class ScannerTest_Numbers(unittest.TestCase):

    def test_single_digit(self):
        scanner = Scanner('2')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.NUMBER)
        self.assertEqual(tokens[0].lexeme, '2')
        self.assertEqual(tokens[0].literal, 2)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_multi_digit(self):
        scanner = Scanner('234')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.NUMBER)
        self.assertEqual(tokens[0].lexeme, '234')
        self.assertEqual(tokens[0].literal, 234)

    def test_fractional_number(self):
        scanner = Scanner('100.12')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.NUMBER)
        self.assertEqual(tokens[0].lexeme, '100.12')
        self.assertEqual(tokens[0].literal, 100.12)

class ScannerTest_Identifiers(unittest.TestCase):

    def test_single_char(self):
        scanner = Scanner('a')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, 'a')
        self.assertEqual(tokens[0].literal, None)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

    def test_multiple_char(self):
        scanner = Scanner('ab')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, 'ab')
        self.assertEqual(tokens[0].literal, None)

    def test_multiple_chars_with_underscore(self):
        scanner = Scanner('a_b')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, 'a_b')
        self.assertEqual(tokens[0].literal, None)

    def test_identifier_starting_with_keyword(self):
        scanner = Scanner('orchid')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, 'orchid')
        self.assertEqual(tokens[0].literal, None)

    def test_identifier_made_of_two_keywords(self):
        scanner = Scanner('orclass')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, 'orclass')
        self.assertEqual(tokens[0].literal, None)

class ScannerTest_Keywords(unittest.TestCase):

    def test_or_keyword(self):
        scanner = Scanner('or')

        tokens = list(scanner.scan_tokens())

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenTypes.OR)
        self.assertEqual(tokens[0].lexeme, 'or')
        self.assertEqual(tokens[0].literal, None)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[1].type, TokenTypes.EOF)

class ScannerTest_Combinations(unittest.TestCase):

    def filter_useless_tokens(self, tokens):
        useless = set([
            TokenTypes.WHITESPACE,
            TokenTypes.NEWLINE,
        ])
        return (token for token in tokens if token.type not in useless)

    def scan_useful_tokens(self, string):
        tokens = Scanner(string).scan_tokens()
        return list(self.filter_useless_tokens(tokens))

    def test_this_or_that(self):
        tokens = self.scan_useful_tokens('this or that')

        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0].type, TokenTypes.THIS)
        self.assertEqual(tokens[1].type, TokenTypes.OR)
        self.assertEqual(tokens[2].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[2].lexeme, 'that')
        self.assertEqual(tokens[3].type, TokenTypes.EOF)

    def test_assign_var_with_comment(self):
        tokens = self.scan_useful_tokens('var a = "beef"; // yeah')

        self.assertEqual(len(tokens), 7)
        self.assertEqual(tokens[0].type, TokenTypes.VAR)
        self.assertEqual(tokens[1].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[1].lexeme, 'a')
        self.assertEqual(tokens[2].type, TokenTypes.EQUAL)
        self.assertEqual(tokens[3].type, TokenTypes.STRING)
        self.assertEqual(tokens[3].literal, 'beef')
        self.assertEqual(tokens[4].type, TokenTypes.SEMICOLON)
        self.assertEqual(tokens[5].type, TokenTypes.COMMENT)
        self.assertEqual(tokens[5].literal, ' yeah')
        self.assertEqual(tokens[5].line, 1)
        self.assertEqual(tokens[6].type, TokenTypes.EOF)

    def test_class(self):
        tokens = self.scan_useful_tokens("""
            class Breakfast {
                cook() {
                    print "yo";
                }
            }""")

        self.assertEqual(len(tokens), 13)
        self.assertEqual(tokens[0].type, TokenTypes.CLASS)
        self.assertEqual(tokens[0].line, 2)
        self.assertEqual(tokens[1].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[1].lexeme, 'Breakfast')
        self.assertEqual(tokens[2].type, TokenTypes.LEFT_BRACE)
        self.assertEqual(tokens[3].type, TokenTypes.IDENTIFIER)
        self.assertEqual(tokens[3].lexeme, 'cook')
        self.assertEqual(tokens[3].line, 3)
        self.assertEqual(tokens[4].type, TokenTypes.LEFT_PAREN)
        self.assertEqual(tokens[5].type, TokenTypes.RIGHT_PAREN)
        self.assertEqual(tokens[6].type, TokenTypes.LEFT_BRACE)
        self.assertEqual(tokens[7].type, TokenTypes.PRINT)
        self.assertEqual(tokens[7].line, 4)
        self.assertEqual(tokens[8].type, TokenTypes.STRING)
        self.assertEqual(tokens[8].literal, 'yo')
        self.assertEqual(tokens[9].type, TokenTypes.SEMICOLON)
        self.assertEqual(tokens[10].type, TokenTypes.RIGHT_BRACE)
        self.assertEqual(tokens[11].type, TokenTypes.RIGHT_BRACE)
        self.assertEqual(tokens[12].type, TokenTypes.EOF)