class Vucab:
    def __init__(self, word: str, meanings: list) -> None:
        self._word = word
        self._meanings = meanings

    def get_word(self):
        return self._word

    def get_meanings(self):
        return self._meanings

    def display(self):
        print('Word: ' + self.word)
        print('meanings: ' + str(self.meanings))

    word = property(get_word)
    meanings = property(get_meanings)
