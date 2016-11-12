from src.Model.Package.entries.GUI.gsection import GSection

__author__ = 'Ondřej Lanč'


class GWindow(GSection):
    """Class that represents the top-level dialogue window"""
    def __init__ (self):
        GSection.__init__(self)
        self.title = "Freeconf generated config dialog"

    def show_all (self, value):
        for tab in self.entries:
            tab.show_all(value)

