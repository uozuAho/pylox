import sys

from pylox.lox import Lox

if __name__ == "__main__":
    args = sys.argv[1:]  # arg 0 is the name of this script
    if len(args) == 0:
        Lox().run_prompt()
    elif len(args) == 1:
        Lox().run_file(args[0])
    else:
        print('nah')
