from src.Model.constants import Types

__author__ = 'Ondřej Lanč'


class GEntry(object):
    """Base class for GUI entries"""
    def __init__ (self, buddy=None, parent=None):
        self._buddy = buddy
        self._parent = parent
        self._label = ""
        self._name = ""

    @property
    def name(self):
        if self._name != "":
            return self._name
        if self._buddy is not None:
            return self._buddy.name
        else:
            return ""

    @name.setter
    def name(self, name):
        self._name = name
        # implicit fallback to key name
        if self._label == "":
            self._label = name

    @property
    def type (self):
        if self._buddy is not None:
            return self._buddy.type
        return Types.UNKNOWN_ENTRY

    @property
    def label(self, language=""):
        if self._buddy is not None:
            label = self._buddy.keyLabel(language)
            if label == "":
                return self._buddy.name
            else:
                return label
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

