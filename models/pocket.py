class Pocket:
    def __init__(self):
        self._data = None
        self._pocket = None

    def set_data(self, val):
        self._data = val

    def get_data(self):
        return self._data

    def set_pocket(self, pkt):
        self._pocket = pkt

    def get_pocket(self):
        return self._pocket

    def insert(self, val):
        self.set_data(val)

    data = property(get_data, set_data)
    pocket = property(get_pocket, set_pocket)
