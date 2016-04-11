from Model.GUI.gentry import GEntry
from Model.container import Container

__author__ = 'Ondřej Lanč'


class GWindow(GEntry, Container):
    """Class that represents the top-level dialogue window"""
    def __init__ (self):
        GEntry.__init__(self)
        Container.__init__(self)
        self._minWidth = 0
        self._minHeight = 0
        self._maxWidth = 0
        self._maxHeight = 0
        self.title = "Freeconf generated config dialog"

    @property
    def minHeight (self):
        return self._minHeight

    @minHeight.setter
    def minHeight (self, height):
        self._minHeight = height
        if self._minHeight > self._maxHeight and self._maxHeight != 0:
            self._maxHeight = self._minHeight

    @property
    def minWidth (self):
        return self._minWidth

    @minWidth.setter
    def minWidth (self, width):
        self._minWidth = width
        if self._minWidth > self._maxWidth and self._maxWidth != 0:
            self._maxWidth = self._minWidth

    @property
    def maxHeight (self):
        return self._maxHeight

    @maxHeight.setter
    def maxHeight (self, height):
        self._maxHeight = height
        if self._maxHeight < self._minHeight and self._minHeight != 0:
            self._minHeight = self._maxHeight

    @property
    def maxWidth (self):
        return self._maxWidth

    @maxWidth.setter
    def maxWidth (self, width):
        self._maxWidth = width
        if self._maxWidth < self._minWidth and self._minWidth != 0:
            self._minWidth = self._maxWidth

    def initState (self):
        """Counts states of all the objects in the GUI tree. Number of active and mandatory keys is stored."""
        for tab in self.entries:
            tab.initState()

    def showAll (self, value):
        for tab in self.entries:
            tab.showAll(value)

