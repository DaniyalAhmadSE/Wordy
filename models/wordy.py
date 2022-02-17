import json
from tkinter import ttk

from glob import glob
from models.change import Change

from models.hash_table_md import HashTableMD
from models.vucab import Vucab
from utils.change_handler import ChangeHandler
from constants import load_times as lt, test_mode as tm, change_types as ct


class Wordy(HashTableMD):
    def __init__(self, sz: int = 27, init=True) -> None:
        super().__init__(sz, init)
        self._change_handler = ChangeHandler()
        if init:
            self.initialize()

    def get_change_handler(self):
        return self._change_handler

    def load_data(self, path, init_i=None, prog_b=None, step=None, is_change=False):
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
                if not is_change:
                    see_also = [s[3:] for s in data if s[:3] == '___']
                    meanings = [s for s in data if s[:3] != '___']
                else:
                    see_also = [s[3:] for s in data[:-1] if s[:3] == '___']
                    meanings = [s for s in data[:-1] if s[:3] != '___']
                vuc = Vucab(to_insert[0], meanings, see_also)
                if is_change:
                    order = data[-1]
                    meanings = meanings[:-1]
                    change = Change(vuc, order, ct.ADDED)
                    self.change_handler.added(change)
                else:
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
                see_also = [s[3:] for s in data[:-1] if s[:3] == '___']
                meanings = [s for s in data[:-1] if s[:3] != '___']
                vuc = Vucab(to_insert[0], meanings, see_also)
                order = data[-1]
                meanings = meanings[:-1]
                change = Change(vuc, order, ct.UPDATED)
                self.change_handler.updated(change)
                w_count += 1
        return w_count

    def unload_data(self, path, prog_b=None, step=None):
        w_count = 0
        with open(path) as file:
            each_json: dict = json.load(file)
            each_list = list(each_json.items())
            each_sz = len(each_list)
            for j in range(each_sz):
                if step is not None and prog_b is not None:
                    prog_b.step(step/each_sz)
                to_del_change = each_list[j]
                to_del = to_del_change[0]
                order = to_del_change[1]
                change = Change(to_del, order, ct.DELETED)
                self.change_handler.deleted(change)
            w_count += 1
        return w_count

    def execute_changes(self, user_path, w_count, prog_b=None):
        add_path = user_path + 'added.json'
        del_path = user_path + 'deleted.json'
        upd_path = user_path + 'edited.json'
        w_count += self.load_data(
            add_path,
            prog_b=prog_b,
            step=lt.ADD_FILE_TIME,
            is_change=True
        )
        self.update_data(upd_path, prog_b, lt.UPD_FILE_TIME)
        w_count -= self.unload_data(
            del_path, prog_b,
            lt.DEL_FILE_TIME
        )

        changes = self.change_handler.all_changes

        for change in changes:
            if change.type == ct.ADDED:
                self.insert(change.item, change.item.word)
            elif change.type == ct.UPDATED:
                self.update(change.item, change.item.word)
            elif change.type == ct.DELETED:
                self.delete(change.item)

        return w_count

    def write_to_file(self, path, is_update=False, is_del=False):
        if is_del:
            changes_list = self.change_handler.deleted_list
        elif is_update:
            changes_list = self.change_handler.updated_list
        else:
            changes_list = self.change_handler.added_list

        sz = len(changes_list)

        key_list = [None for x in range(sz)]
        val_list = [[None for x in range(sz)] for y in range(sz)]

        for i in range(sz):
            each_order = changes_list[i].order
            if is_del:
                each_word = changes_list[i].item
                val_list[i] = each_order
            else:
                each_vuc: Vucab = changes_list[i].item
                each_word = each_vuc.word
                each_meanings = each_vuc.meanings
                each_see_also = each_vuc.see_also

                val_list[i] = each_meanings + \
                    ['___' + x for x in each_see_also]
                val_list[i].append(each_order)

            key_list[i] = each_word

        changes_dict = dict(zip(key_list, val_list))

        with open(path, 'w') as file:
            json.dump(changes_dict, file)

    def write_changes(self, usr_pth: str = 'database/user/'):
        add_path = usr_pth + 'added.json'
        del_path = usr_pth + 'deleted.json'
        upd_path = usr_pth + 'edited.json'
        self.write_to_file(add_path)
        self.write_to_file(upd_path, is_update=True)
        self.write_to_file(del_path, is_del=True)

    def initialize(
        self, def_pth: str = 'database/default/gcide_',
        usr_pth: str = 'database/user/',
        prg_bar: ttk.Progressbar = None,
        lbl: ttk.Label = None
    ):
        if tm.IS_IN_TEST_MODE:
            def_pth = 'database/test/gcide_'

        def_paths = sorted(glob(def_pth + '*.json'))
        w_count = 0
        lw = 'Loading Words: '
        sy = 'Symbolic'
        sym_path = def_pth[:-6] + 'symbols.json'

        if lbl is not None:
            lbl.config(text='Initializing Data Structure')

        print('Initializing Data Structure')
        self.create_structure(27, prg_bar)

        for i in range(26):
            each_ch = chr(i+65)
            print(lw + each_ch + f' ({w_count})')
            if lbl is not None:
                lbl.config(text=lw + each_ch + f' ({w_count})')
            w_count += self.load_data(
                def_paths[i], i, prg_bar, lt.ADD_FILE_TIME
            )

        print(lw + sy + f' ({w_count})' + ' from ' + sym_path)
        if lbl is not None:
            lbl.config(text=lw + sy + f' ({w_count})')
        w_count += self.load_data(sym_path, 26, prg_bar, lt.ADD_FILE_TIME)

        print(f'Finalizing ({w_count})')

        if lbl is not None and prg_bar is not None:
            lbl.config(text=f'Finalizing ({w_count})')

        w_count = self.execute_changes(usr_pth, w_count, prg_bar)

        if lbl is not None and prg_bar is not None:
            lbl.config(text=f'Finalizing ({w_count})')
            prg_bar.step(99.9 - prg_bar['value'])
            prg_bar['value'] += 0.1

        return w_count

    def add_word(self, word: str, meanings: list, see_also: list):
        self.change_handler.changes_unsaved = True
        vuc = Vucab(word, meanings, see_also)
        self.change_handler.added(
            Change(vuc, self.change_handler.change_count + 1, ct.ADDED)
        )
        result = self.insert(vuc, word)
        return result

    def delete_word(self, word):
        self.change_handler.changes_unsaved = True
        self.change_handler.deleted(
            Change(word, self.change_handler.change_count + 1, ct.DELETED)
        )
        result = self.delete(word)
        return result

    def update_word(self, word, meanings, see_also):
        self.change_handler.changes_unsaved = True
        vuc = Vucab(word, meanings, see_also)
        self.change_handler.updated(
            Change(vuc, self.change_handler.change_count + 1, ct.UPDATED)
        )
        result = self.update(vuc, word)
        return result

    change_handler: ChangeHandler = property(get_change_handler)
