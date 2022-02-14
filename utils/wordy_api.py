import threading
from models.vucab import Vucab
from models.wordy import Wordy


class WordyApi:
    def __init__(self, gui_mode=True) -> None:
        self._wordy = Wordy(init=not gui_mode)
        pass

    def start_thread(self, prog_bar=None, lbl=None):
        load_thread = threading.Thread(
            target=self.wordy.initialize,
            kwargs={'prog_bar': prog_bar, 'lbl': lbl}
        )
        load_thread.start()
        return load_thread

    def get_wordy(self) -> Wordy:
        return self._wordy

    def add(self, word: str, meaning: str):
        self.wordy.add(word, meaning)
        return 'Word added successfully'

    def search(self, word: str):
        vuc: Vucab = self.wordy.search(word)

        result = ''
        if vuc is None:
            result = 'Word not found\n'

        else:
            meanings_list: list = vuc.meanings
            sz = meanings_list.__len__()
            for i in range(sz):
                if meanings_list[i][0:3] == '___':
                    see_txt = 'See'
                    if sz > 1:
                        see_txt += ' Also'
                    result += see_txt + ': ' + meanings_list[i][3:] + '\n\n'
                else:
                    result += meanings_list[i] + '\n\n'

        return result

    wordy: Wordy = property(get_wordy)
