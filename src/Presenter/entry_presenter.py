from src.Presenter.presenter import Presenter
from src.Presenter.undo_presenter import UndoPresenter

__author__ = 'Ondřej Lanč'


class EntryPresenter(Presenter):
    def __init__(self, tree):
        self._tree = tree
        self._undo = UndoPresenter()

    @property
    def tree(self):
        return self._tree

    def get_entry(self, path):
        return self.tree.find_entry(path)

    def save_value(self, path, value):
        entry = self.get_entry(path)
        old_value=entry.value
        entry.value = value
        new_value=entry.value
        self._undo.value_change(entry, old_value, new_value)

    def multiple_new(self, path):
        entry = self.get_entry(path)
        newone = entry.create_new()
        self._undo.multiple_new(entry, newone)
        return newone

    def multiple_delete(self, path, index):
        entry = self.get_entry(path)
        removed = entry.delete_entry(index)
        self._undo.multiple_delete(entry, removed)
        return removed

    def multiple_up(self, path, index):
        entry = self.get_entry(path)
        is_move = entry.move_up(index)
        self._undo.multiple_up(entry, index, is_move)
        return is_move

    def multiple_down(self, path, index):
        entry = self.get_entry(path)
        is_move = entry.move_down(index)
        self._undo.multiple_down(entry, index, is_move)
        return is_move
