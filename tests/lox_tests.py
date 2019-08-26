import unittest

from pylox.lox import Lox
from pylox.io import NullOutputStream

from test_utils.test_io import TestOutputStream


class LoxTests_Execute_Expressions(unittest.TestCase):

    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output = self.output)

    def test_numerical(self):
        params = [
            ('1 + 1', 2),
            ('2 * 2', 4),
            ('1 + 4 / 2', 3),
            ('(1 + 4) / 2', 2.5),
            ("""  ( 1 +  4/2) * 3*2 - 10
               == ( 1 +  2)   * 6   - 10   """, True),
        ]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(expression)
                self.assertEqual(self.output.last_sent, expected)

    def test_strings(self):
        params = [
            ('"cat" == "cat"', True),
            ('"dog" == "cat"', False)
        ]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(expression)
                self.assertEqual(self.output.last_sent, expected)

    def test_bools(self):
        params = [
            ('true == 1 < 2', True),
            ('false != 1 < 2 + 4', True)
        ]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(expression)
                self.assertEqual(self.output.last_sent, expected)

    def test_incomplete_expression(self):
        self.lox.execute('1 +')
        self.assertTrue('Expected expression' in self.output.last_sent)
