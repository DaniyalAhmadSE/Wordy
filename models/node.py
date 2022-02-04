class Node:

    def __init__(self, val) -> None:
        self.__data = val
        self.__count = 1
        self.__left = None
        self.__right = None

    def get_data(self):
        return self.__data

    def set_data(self, val) -> None:
        self.__data = val

    def get_count(self):
        return self.__count

    def set_count(self, val) -> None:
        self.__count = val

    def get_left(self):
        return self.__left

    def set_left(self, val) -> None:
        self.__left = val

    def get_right(self):
        return self.__right

    def set_right(self, val) -> None:
        self.__right = val

    def display(self):
        if isinstance(self.data, int) or isinstance(self.data, str):
            print(f'{self.__data}', end=' ')
        else:
            self.data.display()
        if self.count > 1:
            print(f' ({self.count})')

    data = property(get_data, set_data)
    count = property(get_count, set_count)
    left = property(get_left, set_left)
    right = property(get_right, set_right)
