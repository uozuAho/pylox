import sys

from pylox.lox import Lox

DEBUG = True

if __name__ == "__main__":
    args = sys.argv[1:]  # arg 0 is the name of this script
    lox = Lox(debug=DEBUG)
    if len(args) == 0:
        print('bort')
        lox.run_prompt()
    elif len(args) == 1:
        lox.run_file(args[0])
    else:
        print('nah')
