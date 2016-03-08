from src.Model.GUI.gentry import GEntry

__author__ = 'Ondřej Lanč'


class GTab(GEntry):
    """GUI tab representation class"""

    def __init__(self, name="", label="", description="", parent=None):
        GEntry.__init__(self, None, parent)
        self.name = name
        self._label = label
        self.description = description
        self.icon = "mimetypes/unknown"
        self._content = None

    @property
    def label(self):
        if not self._label:
            return self.name
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if self._content == content:
            return
        if self._content is not None:
            self._content.parent = None
        self._content = content
        self._content.parent = self
