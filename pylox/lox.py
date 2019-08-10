from .scanner import Scanner

class Lox:
    def run(self, args):
        if len(args) > 1:
            print("Usage: python lox.py [script]")
            return 64
        elif len(args) == 1:
            self._run_file(args[0])
        else:
            self._run_prompt()

    def _run_file(self, file):
        with open(file, 'rb') as infile:
            bytes = infile.read()
            self._run(bytes)

    def _run_prompt(self):
        while True:
            line = input('>')
            self._run(line)

    def _run(self, bytes):
        scanner = Scanner(bytes)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def _report_error(line, message):
        print('line: {line} error: {message}')
