#!/usr/bin/python3
#
from src.Model.exception_logging.exception import *

__author__ = 'Ondřej Lanč'


class PackageBase(object):
    """Base class for package and plugin classes."""

    def __init__(self, name):
        self.tree = None
        self.input = None
        self.output = None
        self.plugins = []
        self._currentLanguage = ""
        self.packageName = name
        # self.freeconfDirs = []
        self.lists = {}
        self.groups = {}
        self.availableLanguages = []
        self.dependencies = []


    @property
    def is_plugin(self):
        return False

    @property
    def current_language(self):
        return self._currentLanguage

    @current_language.setter
    def current_language(self, lang):
        """Current language setter."""
        self._currentLanguage = lang

    @property
    def available_lists(self):
        """Return list of available value lists."""
        return self.lists

    @property
    def available_groups(self):
        """Return list of available groups."""
        return self.groups

    def add_group(self, group):
        if group.name in self.groups:
            raise AlreadyExistsError("Group with name %s already exists!" % (group.name,))
        self.groups[group.name] = group

    def remove_group(self, name):
        if name not in self.groups:
            raise NotExistsError("Group with name %s does not exist!" % (name,))
        del self.groups[name]

    def load_plugins(self):
        self.input.load_plugin(self)

    def load_config(self):
        """Load config file."""
        self.input.load_config(self)

    def load_package(self, loadAllLanguages):
        """Base function for package load."""
        self.input.load_package(self, loadAllLanguages)

    def transform(self, groupName="default"):
        """Write native config files for all groups."""
        for group in self.groups.values():
            group.write_native(self.tree)

    def execute_dependencies(self):
        # Resolve all loaded dependencies using root_entry as configuration tree. Call this function after parse.
        for dep in self.dependencies[:]:
            # Dependency resolved -> execute it
            dep.execute()

    def write_output(self):
        if self.inconsistent:
            raise InconsistencyError("The package is in inconsistent state. Configuration file cannot be saved")
        self.output.write_output()

    def write_package(self):
        if self.inconsistent:
            raise InconsistencyError("The package is in inconsistent state. Configuration file cannot be saved")
        self.output.write_package()

    def inconsistent(self):
        return self.tree.inconsistent


class Plugin(PackageBase):
    """Class representing plugin."""

    def __init__(self, name, package):
        PackageBase.__init__(self, name, package.parser)
        self.package = package  # Reference to main package

    @property
    def is_plugin(self):
        return True




