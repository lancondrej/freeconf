from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class EntryPresenter(Presenter):
    def __init__(self, tree):
        self._tree=tree

    @property
    def tree(self):
        return self._tree

    def get_entry(self, path):
        return self.tree.find_entry(path)

    def save_value(self, path, value):
        entry = self.get_entry(path)
        entry.value = value

    def multiple_new(self, path):
        entry = self.get_entry(path)
        return entry.create_new()

    def multiple_delete(self, path, index):
        entry = self.get_entry(path)
        return entry.delete_entry(index)

    def multiple_up(self, path, index):
        entry = self.get_entry(path)
        entry.move_up(index)

    def multiple_down(self, path, index):
        entry = self.get_entry(path)
        entry.move_down(index)