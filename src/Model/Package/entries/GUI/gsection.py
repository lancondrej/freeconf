from src.Model.Package.constants import Types
from src.Model.Package.inconsistency import ContainerInconsistency

__author__ = 'Ondřej Lanč'


class GSection(ContainerInconsistency):
    """GUI container class"""
    def __init__(self):
        self._name = None
        # self._parent = None
        self._label = None

        ContainerInconsistency.__init__(self)
        # self._active_shown = 0
        # self._mandatory_shown = 0
        # self._section_shown = 0
        # self.empty = None
        # self._show_all_children = False
        self._entries = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def label(self):
        """Returns the correct mutation of the entry's label"""
        return self._label or self.name

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def type(self):
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
