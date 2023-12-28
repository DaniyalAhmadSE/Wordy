from contextlib import suppress
import threading
from models.vucab import Vucab
from models.wordy import Wordy


class WordyApi:
    def __init__(self, gui_mode=True) -> None:
        self._wordy = Wordy(init=not gui_mode)
        pass

    def start_thread(self, prog_bar=None, lbl=None):
        load_thread = threading.Thread(
            target=self.wordy.initialize, kwargs={"progress_bar": prog_bar, "lbl": lbl}
        )
        load_thread.start()
        return load_thread

    def get_wordy(self) -> Wordy:
        return self._wordy

    def get_are_unsaved_changes(self) -> bool:
        return self._wordy._change_handler._changes_unsaved

    def _push(self, word: str, meanings: str, see_also: str, add_flag=True):
        word = "" if word == "Enter Word" else word
        meanings = (
            "" if meanings == "Enter meanings, separated by blank lines\n" else meanings
        )
        see_also = "" if see_also == "See Also" else see_also

        if (word == "") or (meanings == "" and see_also == ""):
            response = "Invalid inputs"

        else:
            meanings_list = meanings.split("\n\n")
            see_also_list = see_also.split(", ")
            with suppress(ValueError):
                meanings_list.remove("")
            sz = len(meanings_list)
            for i in range(sz):
                while meanings_list[i][-1] == "\n":
                    meanings_list[i] = meanings_list[i][:-1]
                while meanings_list[i][0] == "\n":
                    meanings_list[i] = meanings_list[i][1:]

            if see_also_list[0] == "":
                see_also_list.clear()
            if not add_flag:
                if self.wordy.update_word(word, meanings_list, see_also_list):
                    response = "Word updated successfully"
                else:
                    response = "Word not found"
            else:
                if self.wordy.add_word(word, meanings_list, see_also_list):
                    response = "Word added successfully"
                else:
                    response = "Word exists already"

        return response

    def add(self, word: str, meanings: str, see_also: str) -> str:
        return self._push(word, meanings, see_also)

    def search(self, word: str) -> str:
        result = ""

        if word == "Enter Word" or word == "":
            result = "Please enter a world\n"
        else:
            vuc: Vucab = self.wordy.search(word)

            if vuc is None:
                result = "Word not found\n"

            else:
                meanings_list: list = vuc.meanings
                see_also_list: list = vuc.see_also

                for each in meanings_list:
                    result += each + "\n\n"

                if see_also_list:
                    see_txt = "See"
                    if meanings_list:
                        see_txt += " Also"
                    see_txt += ": \n"

                    result += see_txt
                    sz = len(see_also_list)
                    for i in range(sz):
                        result += see_also_list[i]
                        if i != sz - 1:
                            result += ", "
                    result += "\n"

        return result

    def update(self, word: str, meanings: str, see_also: str):
        return self._push(word, meanings, see_also, add_flag=False)

    def delete(self, word: str):
        if self.wordy.delete_word(word):
            response = "Word deleted successfully"
        else:
            response = "Word does not exist"
        return response

    def save_changes(self):
        self.wordy.write_changes()

    wordy: Wordy = property(get_wordy)
    are_unsaved_changes: bool = property(get_are_unsaved_changes)
