from src.Model.entries.GUI.gsection import GSection

__author__ = 'Ondřej Lanč'


class GTab(GSection):
    """GUI tab representation class"""

    def __init__(self, name="", label="", description="", parent=None):
        self.name = name
        self._label = label
        self.description = description
        self.icon = "mimetypes/unknown"
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

