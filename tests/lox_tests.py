import os
import unittest

from pylox.lox import Lox, LoxFileRunner
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
                self.lox.execute(f'print {expression};')
                self.assertEqual(self.output.last_sent, expected)

    def test_strings(self):
        params = [
            ('"cat" == "cat"', True),
            ('"dog" == "cat"', False)
        ]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(f'print {expression};')
                self.assertEqual(self.output.last_sent, expected)

    def test_bools(self):
        params = [
            ('true == 1 < 2', True),
            ('false != 1 < 2 + 4', True)
        ]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(f'print {expression};')
                self.assertEqual(self.output.last_sent, expected)

    def test_incomplete_expression(self):
        self.lox.execute('1 +')
        self.assertTrue('Expected expression' in self.output.last_sent)


class LoxTests_Execute_Statements(unittest.TestCase):

    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output = self.output)

    def test_print_literal(self):
        self.lox.execute('print "yo";')
        self.assertEqual(self.output.last_sent, "yo")


class LoxTests_Variables(unittest.TestCase):

    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output = self.output)

    def test_declare_then_print(self):
        self.lox.execute('var a;')
        self.lox.execute('print a;')
        self.assertEqual(self.output.last_sent, "nil")

    def test_declare_with_initialiser_then_print(self):
        self.lox.execute('var a = 1;')
        self.lox.execute('print a;')
        self.assertEqual(self.output.last_sent, 1)

    def test_declare_with_initialiser_expression_then_print(self):
        self.lox.execute('var a = 1 + 1;')
        self.lox.execute('print a;')
        self.assertEqual(self.output.last_sent, 2)

    def test_declare_then_assign(self):
        self.lox.execute('var a = 1;')
        self.lox.execute('print a;')
        self.assertEqual(self.output.last_sent, 1)
        self.lox.execute('a = "asdf";')
        self.lox.execute('print a;')
        self.assertEqual(self.output.last_sent, 'asdf')

    def test_can_print_assignment(self):
        # assignment is an expression, so has a value
        self.lox.execute('var a = 1;')
        self.lox.execute('print a = 2;')
        self.assertEqual(self.output.last_sent, 2)

    def test_bad_assign_target_should_print_error(self):
        self.lox.execute('var a; var b;')
        self.lox.execute('a + b = 3;')
        self.assertIn('Invalid assignment target', self.output.last_sent)


class LoxTests_Scoping(unittest.TestCase):

    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output = self.output)

    def test_reuse_name_in_inner_scope(self):
        self.lox.execute('var a = 1;')
        self.lox.execute('{ var a = 2; print a; }')
        self.assertEqual(self.output.last_sent, 2)
        self.lox.execute('print a;')
        self.assertEqual(self.output.last_sent, 1)

    def test_assign_outer_in_inner_scope(self):
        self.lox.execute('var a = 1;')
        self.lox.execute('{ a = 2; }')
        self.lox.execute('print a;')
        self.assertEqual(self.output.last_sent, 2)

class LoxFileRunnerTests(unittest.TestCase):

    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output = self.output)
        self.runner = LoxFileRunner(self.lox)

    def test_run_file(self):
        this_dir = os.path.dirname(__file__)
        test_file = os.path.join(this_dir, 'lox_test_file.lox')
        self.runner.run(test_file)
        self.assertEqual(self.output.last_sent, 2.0)
