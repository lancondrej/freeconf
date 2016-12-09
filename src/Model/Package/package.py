from src.Model.Config.group import default
from src.Model.Package.entries.GUI.gsection import GSection
from src.Model.Package.entries.GUI.gtab import GTab
from src.Model.Package.entries.GUI.gwindow import GWindow
from blinker import signal

from src.Model.Package.entries.container import Container

__author__ = 'Ondřej Lanč'


class Package(object):
    """Base class for package and plugin classes.
    :param name: name of package
    """

    def __init__(self, name):
        self._tree = None
        self.plugins = []
        self._language = None
        self._default_language = 'en'
        self.name = name
        # self.freeconfDirs = []
        self.lists = {}
        self.dependencies = []
        self._gui_tree = None

    def __repr__(self):
        return self.__class__.__name__ + '(' + self.name + ')'

    @property
    def tree(self):
        """tree getter if no one available create default.
        :return Container"""
        return self._tree or self._build_tree()

    @tree.setter
    def tree(self, tree):
        """tree setter
        :param gui_tree: Container object"""
        self._tree = tree

    def _build_tree(self):
        """"build default tree"""
        self._tree = Container('root', None)
        self._tree.group = default
        return self._tree

    @property
    def gui_tree(self):
        """gui tree getter if no one available create default.
        :return GWindow"""
        return self._gui_tree or self._build_gui_tree()

    @gui_tree.setter
    def gui_tree(self, gui_tree):
        """gui tree setter
        :param gui_tree: GWindow object"""
        self._gui_tree = gui_tree

    def _build_gui_tree(self):
        """"build default gui_tree"""
        self._gui_tree = GWindow(self.name, self)

        all = GTab("all", self)
        all.parent = self._gui_tree
        all.label = "All uncontainered entries"
        all.description = "Generated gui Tree"
        all_section = GSection("all", self)
        all_section.parent = all


        from src.Model.Package.entries.container import Container
        for entry in self.tree.entries.values():
            if isinstance(entry, Container):
                cont_tab = GTab(entry.name, self)
                cont_tab.parent = self._gui_tree
                cont_tab.label = entry.label
                cont_tab.description = "Generated tab"
                cont_section = GSection(entry.name, self)
                cont_section.parent = cont_tab
                cont_section.append(entry)
                cont_tab.append(cont_section)
                self._gui_tree.append(cont_tab)
            else:
                all_section.append(entry)

        all.append(all_section)
        self._gui_tree.append(all)


        return self._gui_tree

    @property
    def language(self):
        """language getter get current language or default language
        :return language code"""
        return self._language or self._default_language

    @language.setter
    def language(self, lang):
        """Current language setter."""
        self._language = lang

    @property
    def available_lists(self):
        """Return list of available value lists."""
        return self.lists

    @property
    def inconsistent(self):
        """inconsistency getter"""
        return self.tree.inconsistent

    def inconsistency_signal(self, entry):
        """send inconsistency signal sending is from Inconsistency class"""
        signal('inconsistency_change').send(self, entry=entry)


class Plugin(Package):
    """Class representing plugin."""

    def __init__(self, name, package):
        Package.__init__(self, name)
        self.package = package  # Reference to main package
        self.tree = package.tree
        self.gui_tree = package.gui_tree
