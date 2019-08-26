class TestOutputStream:
    def __init__(self):
        self.last_sent = None

    def send(self, data):
        self.last_sent = data
