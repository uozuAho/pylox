import sys

from pylox.lox import Lox, LoxRepl, LoxFileRunner

DEBUG = False

if __name__ == "__main__":
    args = sys.argv[1:]  # arg 0 is the name of this script
    lox = Lox(debug=DEBUG)
    if len(args) == 0:
        LoxRepl(lox).run()
    elif len(args) == 1:
        LoxFileRunner(lox).run(args[0])
    else:
        print("nah")
