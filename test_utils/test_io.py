class TestOutputStream:
    def __init__(self):
        self.last_sent = None
        self._num_sent = 0

    def send(self, data):
        self.last_sent = data
        self._num_sent += 1

    def num_sent(self) -> int:
        return self._num_sent
