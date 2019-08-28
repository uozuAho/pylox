import unittest

from pylox.parser.parser import Parser
from pylox.parser.expressions import Literal, Unary, Grouping, Binary
from pylox.parser.statements import PrintStatement
from pylox.token import Token
from pylox.token_types import TokenTypes as t

EOF = Token(t.EOF, None, None, None)

class ParserTests(unittest.TestCase):

    def test_single_string(self):
        tokens = [
            Token(t.STRING, "asdf", "asdf", 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(len(statements), 1)
        statement = statements[0]
        expression = statement.expression

        self.assertIsInstance(expression, Literal)

    def test_unary_negative_number(self):
        tokens = [
            Token(t.MINUS, "-", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(len(statements), 1)
        statement = statements[0]
        expression = statement.expression

        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.type, t.MINUS)
        self.assertIsInstance(expression.right, Literal)
        self.assertEqual(expression.right.value, 1)

    def test_grouping_unary_negative_number(self):
        tokens = [
            Token(t.LEFT_PAREN, "(", None, 1),
            Token(t.MINUS, "-", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.RIGHT_PAREN, ")", None, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(len(statements), 1)
        statement = statements[0]
        expression = statement.expression

        self.assertIsInstance(expression, Grouping)
        self.assertIsInstance(expression.expression, Unary)

    def test_print_string_literal(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.STRING, "yo", None, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))

        self.assertIsInstance(statements[0], PrintStatement)
        self.assertIsInstance(statements[0].expression, Literal)

    def test_print_addition(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.PLUS, "+", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))
        statement = statements[0]

        self.assertIsInstance(statement, PrintStatement)
        self.assertIsInstance(statement.expression, Binary)

    def test_print_addition_equality_number(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.PLUS, "+", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.EQUAL_EQUAL, "==", None, 1),
            Token(t.NUMBER, "2", 2, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))
        statement = statements[0]

        self.assertIsInstance(statement, PrintStatement)
        self.assertIsInstance(statement.expression, Binary)

        expression_to_print = statement.expression

        self.assertIsInstance(expression_to_print.left, Binary)
        self.assertEqual(expression_to_print.operator.type, t.EQUAL_EQUAL)
        self.assertIsInstance(expression_to_print.right, Literal)
