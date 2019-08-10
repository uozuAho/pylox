import unittest

from pylox.scanner import Scanner

class ScannerTest(unittest.TestCase):

    def test_single_left_paren(self):
        scanner = Scanner('(')
        tokens = list(scanner.scan_tokens())

        self.assertEqual(1, len(tokens))
