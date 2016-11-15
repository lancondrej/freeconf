from src.Model.Undo.stack import Stack

__author__ = 'Ondřej Lanč'


class Undo(object):
    def __init__(self, limit=20):
        self._stack_limit = limit
        self._undo_stack = Stack(self._stack_limit)
        self._redu_stack = Stack(self._stack_limit)

    def undo(self):
        item = self._undo_stack.pop()
        if item:
            self._redu_stack.push(item)
        return item

    def redo(self):
        item = self._redu_stack.pop()
        if item:
            self._undo_stack.push(item)
        return item

    def save(self):
        item = None
        self._undo_stack.push(item)
