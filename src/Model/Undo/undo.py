from src.Model.Undo.stack import Stack

__author__ = 'Ondřej Lanč'


class Undo(object):
    def __init__(self, limit=20):
        self._stack_limit = limit
        self._undo_stack = Stack(self._stack_limit)
        self._redo_stack = Stack(self._stack_limit)

    def undo(self):
        item = self._undo_stack.pop()
        if item:
            self._redo_stack.push(item.transform())
            item.change()
        return item

    def redo(self):
        item = self._redo_stack.pop()
        if item:
            self._undo_stack.push(item.transform())
            item.change()
        return item

    def save(self, item):
        self._undo_stack.push(item)
        self._redo_stack.flush()
