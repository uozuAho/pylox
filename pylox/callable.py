class Callable:
    """abstract callable"""

    def call(interpreter, args):
        pass

    def arity(self):
        return len(self.args)
