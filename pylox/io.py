class Io:
    """ abstract io 'interface' """
    def send(self, data):
        pass


class StdOutIo(Io):
    def send(self, data):
        print(data)
