#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Undo.change import ValueChange, NewMultipleChange, \
    RemoveMultipleChange, MoveDownMultipleChange, MoveUpMultipleChange
from src.Model.Undo.undo import Undo
from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class UndoPresenter(Presenter):
    """undo presenter manipulate with undo model
    """
    def __init__(self):
        super().__init__()
        self._undo = Undo()

    def value_change(self, entry, old_value, new_value):
        """save value action to undo

        :param entry:
        :param old_value:
        :param new_value:
        """
        if new_value != old_value:
            self._undo.save(ValueChange(entry, old_value))

    def multiple_new(self, entry, newone):
        """save multiple new action to undo

        :param entry:
        :param newone: new item in multiple entry
        """
        if entry is not None:
            self._undo.save(NewMultipleChange(entry, newone))

    def multiple_delete(self, entry, removed):
        """save multiple delete action to undo

        :param entry:
        :param removed: removed item in multiple entry
        """
        if entry is not None:
            self._undo.save(RemoveMultipleChange(entry, removed))

    def multiple_up(self, entry, index, is_move):
        """save multiple up action to undo

        :param entry:
        :param index: index of item in multiple entry
        :param is_move: bool indicate if item is really move
        """
        if is_move:
            self._undo.save(MoveUpMultipleChange(entry, int(index) - 1))
            pass

    def multiple_down(self, entry, index, is_move):
        """save multiple down action to Undo

        :param entry:
        :param index: index of item in multiple entry
        :param is_move: bool indicate if item is really move
        """
        if is_move:
            self._undo.save(MoveDownMultipleChange(entry, int(index) + 1))

    def undo(self):
        """do undo action

        """
        return self._undo.undo()

    def redo(self):
        """do redo action

        """
        return self._undo.redo()
