from src.Model.Package.entries.GUI.gtab import GTab

__author__ = 'Ondřej Lanč'


class GWindow(GTab):
    """Class that represents the top-level dialogue window"""
    def __init__ (self):
        GTab.__init__(self)
        self.title = "Freeconf generated config dialog"

    # def show_all (self, value):
    #     for tab in self.entries:
    #         tab.show_all(value)

    def get_tab(self, name):
        """Find tab with given name."""
        return self.get_section(name)
