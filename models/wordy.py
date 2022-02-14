import json
from tkinter import ttk
from models.hash_table_md import HashTableMD
from models.vucab import Vucab

from glob import glob
from constants import load_times as lt, test_mode as tm


class Wordy(HashTableMD):
    def __init__(self, sz: int = 27, init=True) -> None:
        super().__init__(sz, init)
        if init:
            self.initialize()

    def load_data(self, path, init_i=None, prog_b=None, step=None):
        w_count = 0
        with open(path) as file:
            each_json: dict = json.load(file)
            each_list = list(each_json.items())
            each_sz = len(each_list)
            for j in range(each_sz):
                if step is not None and prog_b is not None:
                    prog_b.step(step/each_sz)
                to_insert = each_list[j]
                data: list = to_insert[1]
                see_also = [s[3:] for s in data if s[:3] == '___']
                meanings = [s for s in data if s[:3] != '___']
                vuc = Vucab(to_insert[0], meanings, see_also)
                self.insert(vuc, vuc.word, init_i)
                w_count += 1
        return w_count

    def update_data(self, path, prog_b=None, step=None):
        w_count = 0
        with open(path) as file:
            each_json: dict = json.load(file)
            each_list = list(each_json.items())
            each_sz = len(each_list)
            for j in range(each_sz):
                if step is not None and prog_b is not None:
                    prog_b.step(step/each_sz)
                to_insert = each_list[j]
                data: list = to_insert[1]
                see_also = [s[3:] for s in data if s[:3] == '___']
                meanings = [s for s in data if s[:3] != '___']
                vuc = Vucab(to_insert[0], meanings, see_also)
                self.update(vuc, vuc.word)
                w_count += 1
        return w_count

    def unload_data(self, path, prog_b=None, step=None):
        w_count = 0
        with open(path) as file:
            each_list: list = json.load(file)
            each_sz = len(each_list)
            for j in range(each_sz):
                if step is not None and prog_b is not None:
                    prog_b.step(step/each_sz)
                to_del = each_list[j]
                self.delete(to_del)
                w_count += 1
        return w_count

    def initialize(
        self, default: str = 'database/default/gcide_',
        user: str = 'database/user/',
        prog_bar: ttk.Progressbar = None,
        lbl: ttk.Label = None
    ):
        if tm.IS_IN_TEST_MODE:
            default = 'database/test/gcide_'
        def_paths = sorted(glob(default + '*.json'))
        w_count = 0
        lw = 'Loading Words: '
        sy = 'Symbolic'
        sym_path = default[:-6] + 'symbols.json'
        add_path = user + 'added.json'
        del_path = user + 'deleted.json'
        upd_path = user + 'edited.json'

        if lbl is not None:
            lbl.config(text='Initializing Data Structure')

        print('Initializing Data Structure')
        self.create_structure(27, prog_bar)

        for i in range(26):
            each_ch = chr(i+65)
            print(lw + each_ch + f' ({w_count})')
            if lbl is not None:
                lbl.config(text=lw + each_ch + f' ({w_count})')
            w_count += self.load_data(
                def_paths[i], i, prog_bar, lt.ADD_FILE_TIME
            )

        print(lw + sy + f' ({w_count})' + ' from ' + sym_path)
        if lbl is not None:
            lbl.config(text=lw + sy + f' ({w_count})')
        w_count += self.load_data(sym_path, 26, prog_bar, lt.ADD_FILE_TIME)

        print(f'Finalizing ({w_count})')

        if lbl is not None and prog_bar is not None:
            lbl.config(text=f'Finalizing ({w_count})')

        w_count += self.load_data(
            add_path,
            prog_b=prog_bar,
            step=lt.ADD_FILE_TIME
        )
        self.update_data(upd_path, prog_bar, lt.UPD_FILE_TIME)
        w_count -= self.unload_data(del_path, prog_bar, lt.DEL_FILE_TIME)

        if lbl is not None and prog_bar is not None:
            lbl.config(text=f'Finalizing ({w_count})')
            prog_bar.step(99.9 - prog_bar['value'])
            prog_bar['value'] += 0.1

        return w_count

    def add_word(self, word: str, meanings: list, see_also: list):
        vuc = Vucab(word, meanings, see_also)
        return self.insert(vuc, word)

    def delete_word(self, word):
        return self.delete(word)

    def update_word(self, word, meanings):
        vuc = Vucab(word, meanings)
        return self.update(vuc, word)
