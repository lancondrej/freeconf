#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Undo.stack import Stack

__author__ = 'Ondřej Lanč'


class Undo(object):
    """Undo model object. It contains two stacks, first is for storing undo changes and second for redo changes.

    :param limit: max value of changes stored in both stacks
    """

    def __init__(self, limit=20):
        self._undo_stack = Stack(limit)
        self._redo_stack = Stack(limit)

    def undo(self):
        """Retrieve change if is available and push it to redo stack.

        :return: last Change object or None if stack is empty
        """
        item = self._undo_stack.pop()
        if item:
            self._redo_stack.push(item.transform())
            item.change()
        return item

    def redo(self):
        """Retrieve change if is available and push it back to undo stack.

        :return: last Change object or None if stack is empty
        """
        item = self._redo_stack.pop()
        if item:
            self._undo_stack.push(item.transform())
            item.change()
        return item

    def save(self, item):
        """Save new change to undo stack.

        :param item: Change object
        """
        self._undo_stack.push(item)
        self._redo_stack.flush()
