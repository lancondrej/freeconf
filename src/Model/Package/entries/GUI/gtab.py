from src.Model.Package.entries.GUI.gsection import GSection

__author__ = 'Ondřej Lanč'


class GTab(GSection):
    """GUI tab representation class"""

    def __init__(self, package):
        GSection.__init__(self, package)
        self.description = None
        self.icon = "mimetypes/unknown"

    @property
    def sections(self):
        return self._entries

    def get_section(self, name):
        """Find entry with given name."""
        return self.get_entry(name)

