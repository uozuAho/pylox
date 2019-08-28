import unittest

from pylox.parser.parser import Parser
from pylox.parser.expressions import Literal, Unary, Grouping
from pylox.parser.statements import PrintStatement
from pylox.token import Token
from pylox.token_types import TokenTypes as t

EOF = Token(t.EOF, None, None, None)

class ParserTests(unittest.TestCase):

    @unittest.skip('todo: not sure if this is a valid statement')
    def test_single_string(self):
        tokens = [Token(t.STRING, "asdf", "asdf", 1), EOF]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertIsInstance(statements[0], Literal)

    @unittest.skip('todo: not sure if this is a valid statement')
    def test_unary_negative_number(self):
        tokens = [
            Token(t.MINUS, "-", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertIsInstance(statements, Unary)
        self.assertEqual(statements.operator.type, t.MINUS)
        self.assertIsInstance(statements.right, Literal)
        self.assertEqual(statements.right.value, 1)

    @unittest.skip('todo: not sure if this is a valid statement')
    def test_grouping_unary_negative_number(self):
        tokens = [
            Token(t.LEFT_PAREN, "(", None, 1),
            Token(t.MINUS, "-", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.RIGHT_PAREN, ")", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertIsInstance(statements, Grouping)
        self.assertIsInstance(statements.expression, Unary)

    def test_print_string_literal(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.STRING, "yo", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))

        self.assertIsInstance(statements[0], PrintStatement)
        self.assertIsInstance(statements[0].expression, Literal)