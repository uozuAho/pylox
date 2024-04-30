import unittest

from pylox.parser.parser import Parser
from pylox.parser import expressions
from pylox.parser import statements
from pylox.token import Token
from pylox.token_types import TokenTypes as t

EOF = Token(t.EOF, None, None, None)


class ParserTests(unittest.TestCase):
    def test_single_string(self):
        tokens = [
            Token(t.STRING, "asdf", "asdf", 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(len(statements), 1)
        statement = statements[0]
        expression = statement.expression

        self.assertIsInstance(expression, expressions.Literal)

    def test_unary_negative_number(self):
        tokens = [
            Token(t.MINUS, "-", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(len(statements), 1)
        statement = statements[0]
        expression = statement.expression

        self.assertIsInstance(expression, expressions.Unary)
        self.assertEqual(expression.operator.type, t.MINUS)
        self.assertIsInstance(expression.right, expressions.Literal)
        self.assertEqual(expression.right.value, 1)

    def test_grouping_unary_negative_number(self):
        tokens = [
            Token(t.LEFT_PAREN, "(", None, 1),
            Token(t.MINUS, "-", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.RIGHT_PAREN, ")", None, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]
        parser = Parser(tokens)
        statements = list(parser.parse())

        self.assertEqual(len(statements), 1)
        statement = statements[0]
        expression = statement.expression

        self.assertIsInstance(expression, expressions.Grouping)
        self.assertIsInstance(expression.expression, expressions.Unary)

    def test_print_string_literal(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.STRING, "yo", None, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]
        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))

        self.assertIsInstance(stmts[0], statements.Print)
        self.assertIsInstance(stmts[0].expression, expressions.Literal)

    def test_print_addition(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.PLUS, "+", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]
        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        stmt = stmts[0]

        self.assertIsInstance(stmt, statements.Print)
        self.assertIsInstance(stmt.expression, expressions.Binary)

    def test_print_addition_equality_number(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.PLUS, "+", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.EQUAL_EQUAL, "==", None, 1),
            Token(t.NUMBER, "2", 2, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]
        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        stmt = stmts[0]

        self.assertIsInstance(stmt, statements.Print)
        self.assertIsInstance(stmt.expression, expressions.Binary)

        expression_to_print = stmt.expression

        self.assertIsInstance(expression_to_print.left, expressions.Binary)
        self.assertEqual(expression_to_print.operator.type, t.EQUAL_EQUAL)
        self.assertIsInstance(expression_to_print.right, expressions.Literal)

    def test_declaration_with_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [
            Token(t.VAR, "var", None, 1),
            identifier_token,
            Token(t.EQUAL, "=", 1, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]

        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        stmt = stmts[0]

        self.assertIsInstance(stmt, statements.VariableDeclaration)
        self.assertIs(stmt.identifier, identifier_token)
        self.assertIsInstance(stmt.initialiser, expressions.Literal)
        self.assertEqual(stmt.initialiser.value, 1)

    def test_declaration_without_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [
            Token(t.VAR, "var", None, 1),
            identifier_token,
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]

        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        stmt = stmts[0]

        self.assertIsInstance(stmt, statements.VariableDeclaration)
        self.assertIs(stmt.identifier, identifier_token)
        self.assertIsNone(stmt.initialiser)

    def test_var_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [identifier_token, Token(t.SEMICOLON, ";", None, 1), EOF]

        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        statement = stmts[0]

        self.assertIsInstance(statement, statements.ExpressionStatement)
        self.assertIsInstance(statement.expression, expressions.Variable)

    def test_assignment_expression(self):
        identifier_token = Token(t.IDENTIFIER, "blah", "blah", 1)
        tokens = [
            identifier_token,
            Token(t.EQUAL, "=", None, 1),
            Token(t.NUMBER, "4", 4, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]

        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        stmt = stmts[0]

        self.assertIsInstance(stmt, statements.ExpressionStatement)
        self.assertIsInstance(stmt.expression, expressions.Assignment)

    def test_single_block_with_two_statements(self):
        tokens = [
            Token(t.LEFT_BRACE, "{", None, 1),
            Token(t.PRINT, "print", None, 1),
            Token(t.STRING, "blah", "blah", 1),
            Token(t.SEMICOLON, ";", None, 1),
            Token(t.PRINT, "print", None, 1),
            Token(t.STRING, "blah", "blah", 1),
            Token(t.SEMICOLON, ";", None, 1),
            Token(t.RIGHT_BRACE, "}", None, 1),
            EOF,
        ]

        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        block = stmts[0]

        self.assertIsInstance(block, statements.Block)
        self.assertEqual(len(block.statements), 2)

    def test_logical_operator_expression(self):
        tokens = [
            Token(t.PRINT, "print", None, 1),
            Token(t.FALSE, "false", None, 1),
            Token(t.AND, ";", None, 1),
            Token(t.STRING, "hello", None, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]

        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        print_stmt = stmts[0]

        self.assertIsInstance(print_stmt, statements.Print)
        self.assertIsInstance(print_stmt.expression, expressions.Logical)

        logical = print_stmt.expression
        self.assertIsInstance(logical.left, expressions.Literal)
        self.assertIsInstance(logical.operator, Token)
        self.assertIsInstance(logical.right, expressions.Literal)

    def test_while_true_statement(self):
        tokens = [
            Token(t.WHILE, "while", None, 1),
            Token(t.LEFT_PAREN, "(", None, 1),
            Token(t.TRUE, "true", True, 1),
            Token(t.RIGHT_PAREN, ")", None, 1),
            Token(t.PRINT, "print", None, 1),
            Token(t.NUMBER, "1", 1, 1),
            Token(t.SEMICOLON, ";", None, 1),
            EOF,
        ]

        parser = Parser(tokens)
        stmts = list(parser.parse())

        self.assertEqual(1, len(stmts))
        while_stmt = stmts[0]

        self.assertIsInstance(while_stmt, statements.While)
