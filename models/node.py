class Node:
    def __init__(self, val, parent=None) -> None:
        self.__data = val
        self.__parent = parent
        self.__left = None
        self.__right = None
        self.__height = 0

    def get_data(self):
        return self.__data

    def set_data(self, val) -> None:
        self.__data = val

    def get_parent(self):
        return self.__parent

    def set_parent(self, val) -> None:
        self.__parent = val

    def get_left(self):
        return self.__left

    def set_left(self, val) -> None:
        self.__left = val
        if val is not None:
            val.parent = self

    def get_right(self):
        return self.__right

    def set_right(self, val) -> None:
        self.__right = val
        if val is not None:
            val.parent = self

    def get_height(self):
        return self.__height

    def set_height(self, val) -> None:
        self.__height = val

    def increment_height(self) -> None:
        self.height += 1

    def decrement_height(self) -> None:
        self.height -= 1

    def display(self):
        if isinstance(self.data, int) or isinstance(self.data, str):
            print(f"{self.__data}", end=" ")
        else:
            self.data.display()

    data = property(get_data, set_data)
    height = property(get_height, set_height)
    parent = property(get_parent, set_parent)
    left = property(get_left, set_left)
    right = property(get_right, set_right)
