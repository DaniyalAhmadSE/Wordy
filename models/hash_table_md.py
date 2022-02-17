from copy import deepcopy
from tkinter import ttk
from models.avl import AVL
from constants.load_times import STRUCT_INIT_TIME


class HashTableMD:
    def __init__(self, sz: int = 27, init=True, dimensions=5) -> None:
        self._dimensions = dimensions
        if init:
            self.create_structure(sz)

    def create_structure(self, sz: int, prog_b: ttk.Progressbar = None):
        self._arr = [
            self.init_inners(sz, prog_b) for u in range(sz)
        ]

    def init_inners(self, sz, prog_b: ttk.Progressbar = None):
        if prog_b is not None:
            prog_b.step(STRUCT_INIT_TIME/sz)

        x = None

        dim = self.dimensions

        for d in range(dim - 1):
            x = [deepcopy(x) for _ in range(sz)]

        return x

    def get_dimensions(self) -> int:
        return self._dimensions

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
        nest = self.dimensions
        idx = [0]*nest
        sz = len(key)

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

    def insert(self, obj, key, init_i=None):
        nest = self.dimensions
        idx = [0]*nest
        sz = len(key)

        if init_i is not None:
            idx[0] = init_i
        start_hash_from = 0 if init_i is None else 1
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
        return dest.avl_insert(obj, key)

    def delete(self, key):
        nest = self.dimensions
        idx = [0]*nest
        sz = len(key)

        for i in range(0, nest):
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
        return dest.avl_delete(key)

    def update(self, obj, key):
        nest = self.dimensions
        idx = [0]*nest
        sz = len(key)

        for i in range(0, nest):
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
        return dest.avl_update(obj, key)

    dimensions = property(get_dimensions)
    arr = property(get_arr)
