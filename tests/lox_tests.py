import unittest

from pylox.lox import Lox, LoxRepl


class TestOutputStream:
    def __init__(self):
        self.last_sent = None

    def send(self, data):
        self.last_sent = data


class LoxTests_Io(unittest.TestCase):

    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(self.output)

    def test_run_str_simple_output(self):
        self.lox.run_str('1 + 1')
        self.assertEqual(self.output.last_sent, 2)


class LoxTests_RunStr_Expressions(unittest.TestCase):

    def setUp(self):
        self.lox = Lox()

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
                result = self.lox.run_str(expression)
                self.assertEqual(result, expected)

    def test_strings(self):
        params = [
            ('"cat" == "cat"', True),
            ('"dog" == "cat"', False)
        ]
        for expression, expected in params:
            with self.subTest():
                result = self.lox.run_str(expression)
                self.assertEqual(result, expected)

    def test_bools(self):
        params = [
            ('true == 1 < 2', True),
            ('false != 1 < 2 + 4', True)
        ]
        for expression, expected in params:
            with self.subTest():
                result = self.lox.run_str(expression)
                self.assertEqual(result, expected)


class LoxReplTests_Expressions(unittest.TestCase):

    def setUp(self):
        self.lox = Lox()
        self.prompt = LoxRepl(self.lox)
        super().setUp()

    def test_execute_single(self):
        output = self.prompt.execute('1 + 1')

        self.assertEqual(output, '2.0')

    def test_execute_incomplete_expression(self):
        output = self.prompt.execute('1 +')

        self.assertTrue('Expected expression' in output)