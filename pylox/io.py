class OutputStream:
    """ abstract io 'interface' """
    def send(self, data):
        pass


class StdOutputStream(OutputStream):
    def send(self, data):
        print(data)


class NullOutputStream(OutputStream):
    pass
