import unittest

from pylox.lox import Lox


class LoxTests_RunStr_Expressions(unittest.TestCase):

    def setUp(self):
        self.lox = Lox(debug=False)
        super().setUp()

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


class LoxTests_RunPrompt_Expressions(unittest.TestCase):

    def setUp(self):
        self.lox = Lox(debug=False)
        super().setUp()

    def test_asdf(self):
        output = self.lox.run_prompt([
            '1 + 1'
        ])

        output = list(output)

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], '2')