class Callable:
    """abstract callable"""

    def call(self, interpreter, args):
        pass

    def arity(self):
        return len(self.args)
