
class EntryController(object):
    def __init__(self, tree):
        self._tree = tree

    def save_value(self, path, value):
        entry = self._tree.find_entry(path)
        entry.value = value

    def multiple_new(self, path):
        entry = self._tree.find_entry(path)
        entry.create_new()

    def multiple_delete(self, path, index):
        entry = self._tree.find_entry(path)
        entry.delete_entry(index)

    def multiple_up(self, path, index):
        entry = self._tree.find_entry(path)
        entry.move_up(index)

    def multiple_down(self, path, index):
        entry = self._tree.find_entry(path)
        entry.move_down(index)

    def get_entry(self, path):
        entry = self._tree.find_entry(path)
        return entry