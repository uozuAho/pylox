import unittest

from pylox.parser.parser import Parser
import pylox.parser.expressions as expr
import pylox.parser.statements as stmt
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

        self.assertIsInstance(expression, expr.Literal)

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

        self.assertIsInstance(expression, expr.Unary)
        self.assertEqual(expression.operator.type, t.MINUS)
        self.assertIsInstance(expression.right, expr.Literal)
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

        self.assertIsInstance(expression, expr.Grouping)
        self.assertIsInstance(expression.expression, expr.Unary)

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

        self.assertIsInstance(statements[0], stmt.Print)
        self.assertIsInstance(statements[0].expression, expr.Literal)

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

        self.assertIsInstance(statement, stmt.Print)
        self.assertIsInstance(statement.expression, expr.Binary)

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

        self.assertIsInstance(statement, stmt.Print)
        self.assertIsInstance(statement.expression, expr.Binary)

        expression_to_print = statement.expression

        self.assertIsInstance(expression_to_print.left, expr.Binary)
        self.assertEqual(expression_to_print.operator.type, t.EQUAL_EQUAL)
        self.assertIsInstance(expression_to_print.right, expr.Literal)

    def test_declaration_with_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [
            Token(t.VAR, "var", None, 1),
            identifier_token,
            Token(t.EQUAL, "=", 1, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]

        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))
        statement = statements[0]

        self.assertIsInstance(statement, stmt.VariableDeclaration)
        self.assertIs(statement.identifier, identifier_token)
        self.assertIsInstance(statement.initialiser, expr.Literal)
        self.assertEqual(statement.initialiser.value, 1)

    def test_declaration_without_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [
            Token(t.VAR, "var", None, 1),
            identifier_token,
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]

        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))
        statement = statements[0]

        self.assertIsInstance(statement, stmt.VariableDeclaration)
        self.assertIs(statement.identifier, identifier_token)
        self.assertIsNone(statement.initialiser)

    def test_var_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [
            identifier_token,
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]

        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))
        statement = statements[0]

        self.assertIsInstance(statement, stmt.Expression)
        self.assertIsInstance(statement.expression, expr.Variable)

    def test_assignment_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [
            identifier_token,
            Token(t.EQUAL, "=", None, 1),
            Token(t.NUMBER, "4", 4, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF
        ]

        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(1, len(statements))
        statement = statements[0]

        self.assertIsInstance(statement, stmt.Expression)
        self.assertIsInstance(statement.expression, expr.Assignment)
