import json
from tkinter import ttk
from models.hash_table_5d import HashTable5D
from models.vucab import Vucab

from glob import glob
from constants import load_times as lt, test_mode as tm


class Wordy(HashTable5D):
    def __init__(self, sz: int = 27, init=True) -> None:
        super().__init__(sz, init)
        if init:
            self.initialize()

    def load_data(self, path, known_i, prog_b=None, step=None):
        w_count = 0
        with open(path) as file:
            each_json: dict = json.load(file)
            each_list = list(each_json.items())
            each_sz = each_list.__len__()
            for j in range(each_sz):
                if step is not None and prog_b is not None:
                    prog_b.step(step/each_sz)
                to_insert = each_list[j]
                vuc = Vucab(to_insert[0], to_insert[1])
                self.insert(vuc, vuc.word, known_i)
                w_count += 1
        return w_count

    def initialize(
        self, default: str = 'database/default/gcide_',
        custom: str = 'database/custom/',
        prog_bar: ttk.Progressbar = None,
        lbl: ttk.Label = None
    ):
        if tm.IS_IN_TEST_MODE:
            default = 'database/test/gcide_'

        if lbl is not None:
            lbl.config(text='Initializing Data Structure')

        print('Initializing Data Structure')
        self.create_structure(27, prog_bar)

        w_count = 0

        file_paths = glob(default + '*.json')

        lw = 'Loading Words: '
        for i in range(26):
            each_ch = chr(i+65)
            print(lw + each_ch + f' ({w_count})')
            if lbl is not None:
                lbl.config(text=lw + each_ch + f' ({w_count})')
            w_count += self.load_data(
                file_paths[i], i, prog_bar, lt.EACH_FILE_TIME
            )

        cus_sym = default[:-6] + 'symbols.json'
        si = 'Symbolic'
        print(lw + si + f' ({w_count})' + ' from ' + cus_sym)
        if lbl is not None:
            lbl.config(text=lw + si + f' ({w_count})')
        w_count += self.load_data(cus_sym, 26, prog_bar, lt.EACH_FILE_TIME)

        cus_wrd = custom + 'words.json'
        ca = 'Custom'
        print(lw + ca + f' ({w_count})')
        if lbl is not None:
            lbl.config(text=lw + ca + f' ({w_count})')
        w_count += self.load_data(cus_wrd, 26, prog_bar, lt.EACH_FILE_TIME)

        print(f'Finalizing ({w_count})')

        if lbl is not None and prog_bar is not None:
            lbl.config(text=f'Finalizing ({w_count})')
            prog_bar.step(99.9 - prog_bar['value'])
            prog_bar['value'] += 0.1

        return w_count

    def add(self, word, meanings):
        vuc = Vucab(word, meanings)
        self.insert(vuc, word, 0)
