from src.Model.Package.inconsistency import ContainerInconsistency

__author__ = 'Ondřej Lanč'


class GSection(ContainerInconsistency):
    """GUI container class"""
    def __init__(self, package):
        self._name = None
        self._inc_parents = set()
        self._label = None
        self._package = package
        self.parent = None

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
        self._name = str(name)


    def __repr__(self):
        return self.__class__.__name__ + '(' + self.name + ')'


    @property
    def label(self):
        """Returns the correct mutation of the entry's label"""
        return self._label or self.name

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def inc_parents(self):
        return self._inc_parents

    @property
    def entries(self):
        return self._entries

    @property
    def package(self):
        """get package"""
        return self._package

    @package.setter
    def package(self, package):
        """set package"""
        self._package = package

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
        entry.inc_parents.add(self)
        self._entries.append(entry)

    def get_entry(self, name):
        """Find entry with given name."""
        indices = [i for i, x in enumerate(self._entries) if x.name == name]
        if len(indices) == 0:
            return None
        else:
            return self._entries[indices[0]]


    @property
    def full_name(self):
        """Return full path in current tree in form of: /a/b/c/..."""
        path = "/" + self.name
        if self.parent:
            path = self.parent.full_name + path
        return path
