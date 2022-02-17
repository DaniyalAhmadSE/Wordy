from models.change import Change


class ChangeHandler:
    def __init__(self) -> None:
        self._change_count = 0
        self._changes_unsaved = False
        self._added_list = []
        self._updated_list = []
        self._deleted_list = []

    def get_change_count(self):
        return self._change_count

    def set_change_count(self, val):
        self._change_count = val

    def get_changes_unsaved(self):
        return self._changes_unsaved

    def set_changes_unsaved(self, val):
        self._changes_unsaved = val

    def get_added_list(self):
        return self._added_list

    def set_added_list(self, add_list):
        self._added_list = add_list

    def get_updated_list(self):
        return self._updated_list

    def set_updated_list(self, upd_list):
        self._updated_list = upd_list

    def get_deleted_list(self):
        return self._deleted_list

    def set_deleted_list(self, del_list):
        self._deleted_list = del_list

    def added(self, change: Change):
        if change.order > self.change_count:
            self.change_count = change.order
        self.added_list.append(change)

    def updated(self, change: Change):
        if change.order > self.change_count:
            self.change_count = change.order
        self.updated_list.append(change)

    def deleted(self, change: Change):
        if change.order > self.change_count:
            self.change_count = change.order
        self.deleted_list.append(change)

    def get_all_changes(self):
        all_changes = self.added_list + self.updated_list + self.deleted_list
        all_changes.sort(key=lambda x: x.order)
        return all_changes

    def clear(self):
        self.added_list.clear()
        self.updated_list.clear()
        self.deleted_list.clear()

    added_list: list = property(get_added_list)
    updated_list: list = property(get_updated_list)
    deleted_list: list = property(get_deleted_list)
    all_changes: list = property(get_all_changes)
    change_count: int = property(get_change_count, set_change_count)
    changes_unsaved: bool = property(get_changes_unsaved, set_changes_unsaved)
