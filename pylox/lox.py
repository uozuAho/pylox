from .scanner import Scanner
from .parser.parser import Parser, ParserException
from .interpreter import Interpreter
from .parser.ast_printer import AstPrinter
from .token_types import TokenTypes as t


class Lox:

    def __init__(self, debug: bool=False):
        self.print_tokens = debug
        self.print_ast = debug

    def run_str(self, string: str):
        tokens = list(Scanner(string).scan_tokens())
        if self.print_tokens:
            for token in tokens:
                print(token)

        expression = Parser(tokens).parse()
        if self.print_ast:
            AstPrinter().print(expression)

        interpreter = Interpreter()
        result = expression.accept(interpreter)
        return result


class LoxRepl:

    def __init__(self, lox: Lox):
        self.lox = lox

    def run(self, input_lines=None):
        # todo (?):
        # read()
        # execute()
        # print()
        # loop()
        def get_inputs():
            if input_lines is None:
                while True:
                    yield input('> ')
            else:
                for line in input_lines:
                    yield line

        outputs = []
        for line in get_inputs():
            output = self.execute(line)

            # todo: abstract io
            if input_lines is None:
                print(output)
            else:
                outputs.append(output)

        return outputs

    def execute(self, input) -> str:
        try:
            output = self.lox.run_str(input)
        except ParserException as p:
            output = self._parser_exception_to_message(p)
        # todo: handle interpreter exception

        return str(output)

    def _parser_exception_to_message(self, exception: ParserException):
        if exception.token.type == t.EOF:
            position_msg = 'at end of file'
        else:
            position_msg = f'at token "{exception.token.lexeme}"'
        return f'{position_msg}: {exception.message}'