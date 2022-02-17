class Change:
    def __init__(self, item, order: int, type: int) -> None:
        self._item = item
        self._order = order
        self._type = type

    def get_item(self):
        return self._item

    def get_order(self) -> int:
        return self._order

    def get_type(self) -> int:
        return self._type

    item = property(get_item)
    order = property(get_order)
    type = property(get_type)
