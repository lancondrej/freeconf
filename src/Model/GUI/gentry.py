from Model.constants import Types

__author__ = 'Ondřej Lanč'


class GEntry(object):
    """Base class for GUI entries"""
    def __init__ (self, parent=None):
        self._name = ""
        self._parent = parent
        self._label = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def type (self):
        return Types.UNKNOWN_ENTRY

    @property
    def label(self, language=""):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

