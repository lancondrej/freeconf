from src.Model.Undo.change import ValueChange, NewMultipleChange, RemoveMultipleChange, MoveDownMultipleChange, MoveUpMultipleChange
from src.Model.Undo.undo import Undo
from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class UndoPresenter(Presenter):
    def __init__(self):
        self._undo = Undo()

    def value_change(self, entry, old_value, new_value):
        if new_value != old_value:
            self._undo.save(ValueChange(entry, old_value))

    def multiple_new(self, entry, newone):
        if entry is not None:
            self._undo.save(NewMultipleChange(entry, newone))

    def multiple_delete(self, entry, removed):
        if entry is not None:
            self._undo.save(RemoveMultipleChange(entry, removed))

    def multiple_up(self, entry, index, is_move):
        if is_move:
            self._undo.save(MoveUpMultipleChange(entry, int(index) - 1))
            pass

    def multiple_down(self, entry, index, is_move):
        if is_move:
            self._undo.save(MoveDownMultipleChange(entry, int(index)+1))

    def undo(self):
        return self._undo.undo()

    def redo(self):
        return self._undo.redo()
