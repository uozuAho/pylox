import time

from pylox.callable import Callable


class Clock(Callable):
    def arity(self):
        return 0

    def call(self, interpreter, args):
        return time.time()
