from .scanner import Scanner
from .parser.parser import Parser, ParserException
from .parser.ast_printer import AstPrinter
from .token_types import TokenTypes as t

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
        try:
            expression = Parser(tokens).parse()
            for token in tokens:
                print(token)
            AstPrinter().print(expression)
        except ParserException as p:
            if p.token.type == t.EOF:
                position_msg = 'at end of file'
            else:
                position_msg = f'at token "{p.token.lexeme}"'
            print(f'{position_msg}: {p.message}')
