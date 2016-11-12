from src.Model.Package.entries.GUI.gentry import GEntry
from src.Model.Package.entries.GUI.gsection import GSection

__author__ = 'Ondřej Lanč'


class GTab(GEntry):
    """GUI tab representation class"""

    def __init__(self):
        GEntry.__init__(self)
        self.description = None
        self.icon = "mimetypes/unknown"
        self._content = []

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    def append(self, entry):
        self._content.append(entry)

    def get_section(self, name):
        """Find entry with given name."""
        indices = [i for i, x in enumerate(self._content) if x.name == name]
        if len(indices) == 0:
            return None
        else:
            return self._content[indices[0]]
