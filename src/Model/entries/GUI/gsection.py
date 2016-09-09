from src.Model.constants import Types
from src.Model.entries.GUI.gentry import GEntry

__author__ = 'Ondřej Lanč'


class GSection(GEntry):
    """GUI container class"""
    def __init__(self, parent=None):
        GEntry.__init__(self, parent)
        self._activeShown = 0
        self._mandatoryShown = 0
        self._sectionShown = 0
        self.empty = None
        self._showAllChildren = False
        self._entries = []

    @property
    def type (self):
        return Types.SECTION

    @property
    def entries (self):
        return self._entries

    @property
    def showAllChildren(self):
        return self._showAllChildren

    @property
    def primaryChildName(self):
        raise AttributeError("Property primaryChildName is write only!")

    @primaryChildName.setter
    def primaryChildName(self, name):
        self._primaryChildName = name
        self._primaryChild = None

    def append(self, entry):
        self._entries.append(entry)

    def get_entry(self, name):
        """Find entry with given name."""
        indices = [i for i, x in enumerate(self._entries) if x.name == name]
        if len(indices) == 0:
            return None
        else:
            return self._entries[indices[0]]
