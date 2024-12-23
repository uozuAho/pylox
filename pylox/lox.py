import typing as typ

from pylox.resolver import Resolver

from .scanner import Scanner
from .parser.parser import Parser, ParserException
from .interpreter import Interpreter, InterpreterException
from .parser.ast_printer import AstPrinter
from .token_types import TokenTypes as t
from .io import OutputStream, StdOutputStream


class Lox:
    def __init__(
        self,
        output: typ.Optional[OutputStream] = None,
        debug: bool = False,
        throw: bool = True,
    ):
        self.out = output or StdOutputStream()
        self.interpreter = Interpreter(self.out)
        self.resolver = Resolver(self.interpreter)
        self.print_tokens = debug
        self.print_ast = debug
        self.throw = throw

    def execute(self, input: str):
        error_message = None

        try:
            self._execute(input)
        except ParserException as p:
            error_message = self._parser_exception_to_message(p)
            p.add_note(error_message)
            if self.throw:
                raise
        except InterpreterException as i:
            error_message = self._interpreter_exception_to_message(i)
            i.add_note(error_message)
            if self.throw:
                raise

        if error_message:
            self.out.send(error_message)

    def _execute(self, input: str):
        tokens = list(Scanner(input).scan_tokens())
        if self.print_tokens:
            for token in tokens:
                self._output(token)

        statements = list(Parser(tokens).parse())
        for statement in statements:
            if self.print_ast:
                ast = AstPrinter().to_string(statement)
                self._output(ast)

        self.resolver._resolve_all(statements)
        self.interpreter.interpret(statements)

    def _output(self, data):
        self.out.send(data)

    def _parser_exception_to_message(self, exception: ParserException):
        if exception.token.type == t.EOF:
            position_msg = "at end of file"
        else:
            position_msg = (
                f'on line {exception.token.line}, token "{exception.token.lexeme}"'
            )
        return f"{position_msg}: {exception.message}"

    def _interpreter_exception_to_message(self, exception: InterpreterException):
        expression_str = AstPrinter().to_string(exception.expression)
        return f'at expression "{expression_str}": {exception.message}'


class LoxRepl:
    def __init__(self, lox: Lox):
        self.lox = lox

    def run(self):
        while True:
            line = input("> ")
            self.lox.execute(line)


class LoxFileRunner:
    def __init__(self, lox: Lox):
        self.lox = lox

    def run(self, path: str):
        with open(path) as infile:
            contents = infile.read()
            self.lox.execute(contents)
