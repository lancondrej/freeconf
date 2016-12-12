#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Ondřej Lanč'


class Change(object):
    """Base Change class. Just abstraction.
    :param entry: entry which has been change
    """
    def __init__(self, entry):
        self.entry = entry

    def transform(self):
        """method returning opposite Change object. Need to be implemented in subclass.
        :return Change: opposite Change object
        """
        raise NotImplementedError

    def change(self):
        """method realizing change"""
        raise NotImplementedError


class ValueChange(Change):
    """Class for value changes
    :param entry: entry which has been change
    :param old_value: old value of entry
    """
    def __init__(self, entry, old_value):
        Change.__init__(self, entry)
        self.old_value = old_value

    def transform(self):
        """set actual value as new old value
        :return ValueChange
        """
        return ValueChange(self.entry, self.entry.value)

    def change(self):
        """set value of entry as old_value"""
        self.entry.value = self.old_value


class NewMultipleChange(Change):
    """Class for multiple entry new creation
    :param entry: multiple entry
    :param newone: new entry of multiple
    """
    def __init__(self, entry, newone):
        Change.__init__(self, entry)
        self.newone = newone

    def transform(self):
        """return RemoveMultipleChange with newone as removed
        :return RemoveMultipleChange
        """
        return RemoveMultipleChange(self.entry, self.newone)

    def change(self):
        """delete newone form entry"""
        self.entry.delete_entry(self.newone.index)


class RemoveMultipleChange(Change):
    """Class for multiple entry remove change
    :param entry: multiple entry
    :param removed: entry which has been remove
    """
    def __init__(self, entry, removed):
        Change.__init__(self, entry)
        self.removed = removed

    def transform(self):
        """return NewMultipleChange with removed as newone
        :return NewMultipleChange
        """
        return NewMultipleChange(self.entry, self.removed)

    def change(self):
        """insert removed back to entry"""
        self.entry.insert(self.removed.index, self.removed)


class MoveUpMultipleChange(Change):
    """Class for multiple entry move up change
    :param entry: multiple entry
    :param index: index of entry which is move in multiple entry
    """
    def __init__(self, entry, index):
        Change.__init__(self, entry)
        self.index = int(index)

    def transform(self):
        """return MoveDownMultipleChange with increased index
        :return MoveDownMultipleChange
        """
        return MoveDownMultipleChange(self.entry, self.index + 1)

    def change(self):
        """move down indexed entry in multiple entry"""
        self.entry.move_down(self.index)


class MoveDownMultipleChange(Change):
    """Class for multiple entry move down change
    :param entry: multiple entry
    :param index: index of entry which is move in multiple entry
    """
    def __init__(self, entry, index):
        Change.__init__(self, entry)
        self.index = int(index)

    def transform(self):
        """return MoveUpMultipleChange with decreased index
        :return MoveUpMultipleChange
        """
        return MoveUpMultipleChange(self.entry, self.index - 1)

    def change(self):
        """move up indexed entry in multiple entry"""
        self.entry.move_up(self.index)
