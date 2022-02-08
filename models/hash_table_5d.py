from tkinter import ttk
from models.avl import AVL
from constants.load_times import STRUCT_INIT_TIME


class HashTable5D:
    def __init__(self, sz: int = 27, init=True) -> None:
        if init:
            self.create_structure(sz)

    def create_structure(self, sz: int, prog_b: ttk.Progressbar = None):
        self._arr = [
            self.init_inners(sz, prog_b) for t in range(sz)
        ]

    def init_inners(self, sz, prog_b: ttk.Progressbar = None):
        if prog_b is not None:
            prog_b.step(STRUCT_INIT_TIME/sz)
        return [
            [
                [
                    [None for p in range(sz)] for q in range(sz)
                ] for r in range(sz)
            ] for s in range(sz)
        ]

    def get_arr(self) -> list:
        return self._arr

    def hash(self, key: str) -> int:
        ascii = ord(key)

        if (ascii < 97):
            ascii = ascii + 32

        index = ascii - 97

        if not (index >= 0 and index < 26):
            return 26

        return index

    def search(self, key: str):
        nest = 5
        idx = [0]*nest
        sz = key.__len__()

        for i in range(0, nest):
            if i >= sz:
                break
            idx[i] = self.hash(key[i])

        loc_path = self.arr
        for i in range(nest):
            loc_path = loc_path[idx[i]]

        loc: AVL = loc_path
        if loc is None:
            return None
        result = loc.search_node(key)
        if result is None:
            return None
        return result.data

    def insert(self, obj, key, init_i=0):
        nest = 5
        idx = [0]*nest
        sz = key.__len__()

        idx[0] = init_i
        start_hash_from = 0 if init_i == 0 else 1
        for i in range(start_hash_from, nest):
            if i >= sz:
                break
            idx[i] = self.hash(key[i])

        dest_path = self.arr
        for i in range(nest):
            loc = idx[i]
            if dest_path[loc] is None:
                dest_path[loc] = AVL()

            dest_path = dest_path[loc]

        dest: AVL = dest_path
        dest.avl_insert(obj, key)

    arr = property(get_arr)
