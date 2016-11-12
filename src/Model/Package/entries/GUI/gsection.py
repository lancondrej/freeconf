from src.Model.Package.constants import Types
from src.Model.Package.entries.GUI.gentry import GEntry

__author__ = 'Ondřej Lanč'


class GSection(GEntry):
    """GUI container class"""
    def __init__(self):
        GEntry.__init__(self)
        # self._active_shown = 0
        # self._mandatory_shown = 0
        # self._section_shown = 0
        # self.empty = None
        # self._show_all_children = False
        self._entries = []

    @property
    def type (self):
        return Types.SECTION

    @property
    def entries(self):
        return self._entries
    #
    # @property
    # def show_all_children(self):
    #     return self._show_all_children

    # @property
    # def primaryChildName(self):
    #     raise AttributeError("Property primaryChildName is write only!")
    #
    # @primaryChildName.setter
    # def primaryChildName(self, name):
    #     self._primaryChildName = name
    #     self._primaryChild = None

    def append(self, entry):
        self._entries.append(entry)

    def get_entry(self, name):
        """Find entry with given name."""
        indices = [i for i, x in enumerate(self._entries) if x.name == name]
        if len(indices) == 0:
            return None
        else:
            return self._entries[indices[0]]
