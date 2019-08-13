from .scanner import Scanner
from .parser.parser import Parser
from .parser.ast_printer import AstPrinter

class Lox:
    def run_file(self, file):
        with open(file, 'rb') as infile:
            bytes = infile.read()
            self._run(bytes)

    def run_prompt(self):
        while True:
            line = input('> ')
            self._run(line)

    def _run(self, bytes):
        tokens = list(Scanner(bytes).scan_tokens())
        expression = Parser(tokens).parse()

        for token in tokens:
            print(token)

        AstPrinter().print(expression)
