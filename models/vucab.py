class Vucab:
    def __init__(self, word: str, meanings: list, see_also: list = []) -> None:
        self._word = word
        self._meanings = meanings
        self._see_also = see_also

    def get_word(self):
        return self._word

    def get_meanings(self):
        return self._meanings

    def get_see_also(self):
        return self._see_also

    def display(self):
        print('Word: ' + self.word)
        print('Meanings: ' + str(self.meanings))
        print('See Also: ' + str(self.meanings))

    word = property(get_word)
    meanings = property(get_meanings)
    see_also = property(get_see_also)
