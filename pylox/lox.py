from .scanner import Scanner

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
        scanner = Scanner(bytes)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)
