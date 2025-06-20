import os
import unittest

from pylox.interpreter import InterpreterException
from pylox.lox import Lox, LoxFileRunner

from test_utils.test_io import TestOutputStream


class LoxTests_Execute_Expressions(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output, throw=False)

    def test_numerical(self):
        params = [
            ("1 + 1", 2),
            ("2 * 2", 4),
            ("1 + 4 / 2", 3),
            ("(1 + 4) / 2", 2.5),
            (
                """  ( 1 +  4/2) * 3*2 - 10
               == ( 1 +  2)   * 6   - 10   """,
                True,
            ),
        ]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(f"print {expression};")
                self.assertEqual(self.output.last_sent, expected)

    def test_strings(self):
        params = [('"cat" == "cat"', True), ('"dog" == "cat"', False)]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(f"print {expression};")
                self.assertEqual(self.output.last_sent, expected)

    def test_bools(self):
        params = [("true == 1 < 2", True), ("false != 1 < 2 + 4", True)]
        for expression, expected in params:
            with self.subTest():
                self.lox.execute(f"print {expression};")
                self.assertEqual(self.output.last_sent, expected)

    def test_incomplete_expression(self):
        self.lox.execute("1 +")
        self.assertTrue("Expected expression" in self.output.last_sent)


class LoxTests_Execute_Statements(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)

    def test_print_literal(self):
        self.lox.execute('print "yo";')
        self.assertEqual(self.output.last_sent, "yo")


class LoxTests_Variables(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output, throw=False)

    def test_declare_then_print(self):
        self.lox.execute("var a;")
        self.lox.execute("print a;")
        self.assertEqual(self.output.last_sent, "nil")

    def test_declare_with_initialiser_then_print(self):
        self.lox.execute("var a = 1;")
        self.lox.execute("print a;")
        self.assertEqual(self.output.last_sent, 1)

    def test_declare_with_initialiser_expression_then_print(self):
        self.lox.execute("var a = 1 + 1;")
        self.lox.execute("print a;")
        self.assertEqual(self.output.last_sent, 2)

    def test_declare_then_assign(self):
        self.lox.execute("var a = 1;")
        self.lox.execute("print a;")
        self.assertEqual(self.output.last_sent, 1)
        self.lox.execute('a = "asdf";')
        self.lox.execute("print a;")
        self.assertEqual(self.output.last_sent, "asdf")

    def test_can_print_assignment(self):
        # assignment is an expression, so has a value
        self.lox.execute("var a = 1;")
        self.lox.execute("print a = 2;")
        self.assertEqual(self.output.last_sent, 2)

    def test_bad_assign_target_should_print_error(self):
        self.lox.execute("var a; var b;")
        self.lox.execute("a + b = 3;")
        self.assertIn("Invalid assignment target", self.output.last_sent)


class LoxTests_Scoping(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)

    def test_reuse_name_in_inner_scope(self):
        self.lox.execute(
            """
            var a = 1;
            { var a = 2; print a; }
            print a;
            """)
        self.assertEqual(self.output.last_sent, 1)

    def test_assign_outer_in_inner_scope(self):
        self.lox.execute(
            """
            var a = 1;
            { a = 2; }
            print a;
            """)
        self.assertEqual(self.output.last_sent, 2)

    def test_resolve_closure(self):
        self.lox.execute(
            """
            var a = 1;
            {
                fun showA() {
                    print(a);
                }
                showA();   // 1
                var a = 2;
                showA();   // 1 (captured in closure)
            }
            """
        )
        self.assertEqual(self.output.num_sent(), 2)
        self.assertEqual(self.output.last_sent, 1)


class LoxTests_IfElse(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)

    def test_if_true_else(self):
        self.lox.execute('if (true) print "true"; else print "false";')
        self.assertEqual(self.output.last_sent, "true")

    def test_if_false_else(self):
        self.lox.execute('if (false) print "true"; else print "false";')
        self.assertEqual(self.output.last_sent, "false")

    def test_nested_if_else_should_grab_earliest_else(self):
        self.lox.execute("""
            if (true)
                if (true)
                    print "this should get printed";
                else
                    print "this should not get printed";
            """)
        self.assertEqual(self.output.last_sent, "this should get printed")


class LoxFileRunnerTests(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)
        self.runner = LoxFileRunner(self.lox)

    def test_run_file(self):
        this_dir = os.path.dirname(__file__)
        test_file = os.path.join(this_dir, "lox_test_file.lox")
        self.runner.run(test_file)


class LoxTests_LogicalOperators(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)

    def test_print_false_and_1(self):
        self.lox.execute("print false and 1;")
        self.assertEqual(self.output.last_sent, False)

    def test_print_true_and_1(self):
        self.lox.execute("print true and 1;")
        self.assertEqual(self.output.last_sent, 1)


class LoxTests_WhileLoops(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)

    def test_while_var_one_loop(self):
        self.lox.execute("var do_loop = true;")
        self.lox.execute("while (do_loop) { print 1; do_loop = false; }")
        self.assertEqual(self.output.last_sent, 1)

    def test_while_false_does_nothing(self):
        self.lox.execute("while (false) print 1;")
        self.assertEqual(self.output.num_sent(), 0)

    def test_while_loops_multiple_times(self):
        self.lox.execute("var temp = 5;")
        self.lox.execute("while (temp > 0) { print 1; temp = temp - 1; }")
        self.assertEqual(self.output.num_sent(), 5)


class LoxTests_ForLoops(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)

    def test_for_var_one_loop(self):
        self.lox.execute("""
                         for (var do_loop = true; do_loop; do_loop = false) {
                            print 1;
                         }
                         """)
        self.assertEqual(self.output.num_sent(), 1)
        self.assertEqual(self.output.last_sent, 1)

    def test_for_false_does_nothing(self):
        self.lox.execute("for (;false;) print 1;")
        self.assertEqual(self.output.num_sent(), 0)

    def test_for_loops_multiple_times(self):
        self.lox.execute("""
                         for (var i = 0; i < 5; i = i + 1) {
                            print i;
                         }
                         """)
        self.assertEqual(self.output.num_sent(), 5)
        self.assertEqual(self.output.last_sent, 4)


class LoxTests_Functions(unittest.TestCase):
    def setUp(self):
        self.output = TestOutputStream()
        self.lox = Lox(output=self.output)

    def test_declaration(self):
        self.lox.execute(
            """
            fun print_sum(a, b) {
                print a + b;
            }
            """
        )

    def test_decl_and_run(self):
        self.lox.execute(
            """
            fun print_sum(a, b) {
                print a + b;
            }

            print_sum(1, 2);
            """
        )
        self.assertEqual(self.output.num_sent(), 1)
        self.assertEqual(self.output.last_sent, 3)

    def test_native_call(self):
        self.lox.execute("print(clock());")
        self.assertEqual(self.output.num_sent(), 1)
        self.assertGreater(self.output.last_sent, 1234.56)

    def test_return_val(self):
        self.lox.execute(
            """
            fun sum(a, b) { return a + b; }
            print sum(1, 2);
            """
        )
        self.assertEqual(self.output.num_sent(), 1)
        self.assertEqual(self.output.last_sent, 3)

    def test_fib(self):
        """tests a whole bunch of stuff: function, conditional, arithmetic,
        parameters, more
        """
        self.lox.execute(
            """
            fun fib(n) {
                if (n <= 1) return n;
                return fib(n - 2) + fib(n - 1);
            }
            print fib(6);
            """
        )
        self.assertEqual(self.output.num_sent(), 1)
        self.assertEqual(self.output.last_sent, 8)

    def test_throws_on_call_non_function(self):
        def run():
            self.lox.execute('"asdf"();')

        self.assertRaises(InterpreterException, run)

    def test_too_few_args(self):
        def run():
            self.lox.execute(
                """
            fun sum(a, b) { return a + b; }
            print sum(1);
            """
            )

        self.assertRaises(InterpreterException, run)

    def test_local_func(self):
        self.lox.execute(
            """
            fun makeCounter() {
                var i = 0;
                fun count() {
                    i = i + 1;
                    return i;
                }
                return count;
            }
            var counter = makeCounter();
            print(counter()); // 1
            print(counter()); // 2
            """
        )
        self.assertEqual(self.output.num_sent(), 2)
        self.assertEqual(self.output.last_sent, 2)
