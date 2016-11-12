from src.Model.Package.constants import Types

__author__ = 'Ondřej Lanč'


class GEntry(object):
    """Base class for GUI entries"""
    def __init__ (self):
        self._name = None
        # self._parent = None
        self._label = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    # @property
    # def parent(self):
    #     return self._parent
    #
    # @parent.setter
    # def parent(self, parent):
    #     self._parent = parent

    @property
    def type (self):
        return Types.UNKNOWN_ENTRY

    @property
    def label(self):
        """Returns the correct mutation of the entry's label"""
        return self._label or self.name

    @label.setter
    def label(self, label):
        self._label = label


