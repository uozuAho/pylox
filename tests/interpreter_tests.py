import unittest

from pylox.interpreter import Interpreter, InterpreterException
from pylox.parser.expressions import Grouping, Literal, Unary, Binary
from pylox.token import Token
from pylox.token_types import TokenTypes as t

def new_token(type):
    return Token(type, None, None, 1)

class InterpreterTests_Expressions(unittest.TestCase):

    def setUp(self):
        self.interpreter = Interpreter()

    def test_grouping_should_equal_inner_value(self):
        inner_expression = Literal(1)
        grouping = Grouping(inner_expression)

        result = self.interpreter.visit_grouping_expression(grouping)

        self.assertEqual(result, 1)

    def test_literal_should_equal_value(self):
        literal = Literal(2)

        result = self.interpreter.visit_literal_expression(literal)

        self.assertEqual(result, 2)

    def test_unary_not(self):
        unary = Unary(new_token(t.BANG), Literal(False))

        result = self.interpreter.visit_unary_expression(unary)

        self.assertEqual(result, True)

    def test_unary_minus(self):
        unary = Unary(new_token(t.MINUS), Literal(2))

        result = self.interpreter.visit_unary_expression(unary)

        self.assertEqual(result, -2)


class InterpreterTests_BinaryEqualityExpressions(unittest.TestCase):

    def setUp(self):
        self.interpreter = Interpreter()

    def test_equality_numbers(self):
        binary = Binary(Literal(2), new_token(t.EQUAL_EQUAL), Literal(2))

        result = self.interpreter.visit_binary_expression(binary)

        self.assertEqual(result, True)

    def test_equality_bools(self):
        binary = Binary(Literal(True), new_token(t.EQUAL_EQUAL), Literal(False))

        result = self.interpreter.visit_binary_expression(binary)

        self.assertEqual(result, False)

    def test_equality_number_and_bool(self):
        binary = Binary(Literal(1), new_token(t.EQUAL_EQUAL), Literal(True))

        result = self.interpreter.visit_binary_expression(binary)

        self.assertEqual(result, False)

    @unittest.skip('this is a known issue (see readme). Hopefully gets fixed in blog...')
    def test_double_equality(self):
        # 1 == 1 == 1
        comparison = Binary(
            Binary(Literal(1), new_token(t.EQUAL_EQUAL), Literal(1)),
            new_token(t.EQUAL_EQUAL),
            Literal(1)
        )

        result = self.interpreter.visit_binary_expression(comparison)

        self.assertEqual(result, True)


class InterpreterTests_BinaryExpressions(unittest.TestCase):

    def setUp(self):
        self.interpreter = Interpreter()

    def test_multiply(self):
        binary = Binary(Literal(2), new_token(t.STAR), Literal(4))

        result = self.interpreter.visit_binary_expression(binary)

        self.assertEqual(result, 8)

    def test_add_numbers(self):
        binary = Binary(Literal(1), new_token(t.PLUS), Literal(1))

        result = self.interpreter.visit_binary_expression(binary)

        self.assertEqual(result, 2)

    def test_add_strings(self):
        binary = Binary(Literal("hello "), new_token(t.PLUS), Literal("kitty"))

        result = self.interpreter.visit_binary_expression(binary)

        self.assertEqual(result, "hello kitty")

    def test_add_number_and_string(self):
        binary = Binary(Literal(1), new_token(t.PLUS), Literal("kitty"))

        with self.assertRaises(InterpreterException) as context:
            result = self.interpreter.visit_binary_expression(binary)

            self.assertEqual(context.expression, binary)

    def test_comparison(self):
        comparison = Binary(Literal(1), new_token(t.LESS), Literal(2))

        result = self.interpreter.visit_binary_expression(comparison)

        self.assertEqual(result, True)

    def test_equality(self):
        comparison = Binary(Literal(1), new_token(t.EQUAL_EQUAL), Literal(1))

        result = self.interpreter.visit_binary_expression(comparison)

        self.assertEqual(result, True)
