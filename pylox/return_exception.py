class ReturnException(Exception):
    """ This is a hack to unwind the execution stack back to the function call
        when a return statement is encountered
    """
    def __init__(self, value):
        self.value = value
