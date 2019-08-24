import unittest

from .test_io import TestOutputStream


class TestOutputStreamTests(unittest.TestCase):

    def setUp(self):
        self.output = TestOutputStream()

    def test_run_str_simple_output(self):
        self.output.send('asdf')
        self.assertEqual(self.output.last_sent, 'asdf')
