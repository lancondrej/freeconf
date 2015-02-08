#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class PackageBase (object):
    """Base class for package and plugin classes."""

    class Paths (object):
        """Structure containing paths used in package."""
        def __init__(self):
            self.home_dir = ""
            self.package_name = ""
            self.package_dir = ""
            self.help_dirs = {}
            self.list_dirs = []
            self.freeconf_dirs = []
            self.default_values_dirs = []
            self.list_files = {}

        @property
        def main_dir(self):
            """Return location of main package or plugin directory."""
            return self.package_dir

    def __init__(self, paths):
        self._entries = None
        self.paths = paths

    @property
    def is_plugin(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def _load_header_file (self):
        """Load header file."""

    def _load_help_file(self):
        """Load help file."""

    def _load_template_file(self):
        """Load template file."""

    def _load_dependencies_file(self):
        """Load dependencies file."""

    def _load_default_values_file(self):
        """Load default values file. Support function for loadPackage."""

    def _load_list_help(self):
        """Load list help file."""

    def _load_lists(self):
        """Load list files."""

    def _load_config_file(self):
        """Load config file."""

    def load_package(self):
        """Base function for package load."""

    def write_output(self):
        """Write configuration output file."""

    def write_native_output(self):
        """Write native config files for all groups."""
