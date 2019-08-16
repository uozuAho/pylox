import unittest

from pylox.interpreter import Interpreter
from pylox.parser.expressions import Grouping, Literal, Unary
from pylox.token import Token
from pylox.token_types import TokenTypes as t

class InterpreterTests(unittest.TestCase):

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
        unary = Unary(Token(t.BANG, '!', None, 1), Literal(False))

        result = self.interpreter.visit_unary_expression(unary)

        self.assertEqual(result, True)

    def test_unary_minux(self):
        unary = Unary(Token(t.MINUS, '-', None, 1), Literal(2))

        result = self.interpreter.visit_unary_expression(unary)

        self.assertEqual(result, -2)
