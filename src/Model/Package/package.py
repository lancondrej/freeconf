#!/usr/bin/python3
#
from src.Model.Package.entries.GUI.gsection import GSection
from src.Model.Package.entries.GUI.gtab import GTab
from src.Model.Package.entries.GUI.gwindow import GWindow
from src.Model.Package.exception_logging.exception import NotExistsError, AlreadyExistsError

__author__ = 'Ondřej Lanč'


class Package(object):
    """Base class for package and plugin classes."""

    def __init__(self, name):
        self.tree = None
        self.plugins = []
        self._language = None
        self._default_language = 'en'
        self.package_name = name
        # self.freeconfDirs = []
        self.lists = {}
        self.groups = {}
        self.dependencies = []
        self._gui_tree = None

    @property
    def gui_tree(self):
        return self._gui_tree or self.build_gui_tree()

    @gui_tree.setter
    def gui_tree(self, gui_tree):
        self._gui_tree=gui_tree

    def build_gui_tree(self):
        self._gui_tree=GWindow()
        tab=GTab()
        tab.name="all"
        tab.label="All entries"
        tab.description="Generated gui Tree"
        section=GSection()
        section.append(self.tree)
        tab.content.append(section)
        self._gui_tree.append(tab)
        return self._gui_tree


    @property
    def is_plugin(self):
        return False

    @property
    def language(self):
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
    def available_groups(self):
        """Return list of available groups."""
        return self.groups

    @available_groups.setter
    def available_groups(self, group):
        """Return list of available groups."""
        self.groups = group

    def add_group(self, group):
        if group.name in self.groups:
            raise AlreadyExistsError("Group with name %s already exists!" % (group.name,))
        self.groups[group.name] = group

    def remove_group(self, name):
        if name not in self.groups:
            raise NotExistsError("Group with name %s does not exist!" % (name,))
        del self.groups[name]

    def transform(self, groupName="default"):
        """Write native config files for all groups."""
        for group in self.groups.values():
            group.write_native(self.tree)

    def execute_dependencies(self):
        # Resolve all loaded dependencies using root_entry as configuration tree. Call this function after parse.
        for dep in self.dependencies[:]:
            # Dependency resolved -> execute it
            dep.execute()

    def inconsistent(self):
        return self.tree.inconsistent


class Plugin(Package):
    """Class representing plugin."""

    def __init__(self, name, package):
        Package.__init__(self, name)
        self.available_groups = package.available_groups
        self.package = package  # Reference to main package
        self.tree = package.tree
        self.gui_tree = package.gui_tree

    @property
    def is_plugin(self):
        return True




