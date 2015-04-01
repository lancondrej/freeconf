#!/usr/bin/python3
#
import os
import re

from Model.group import FcGroup
from IO.Input.XMLPackageParser.header_file import HeaderFileReader
from IO.file import FcFileLocation
from IO.Input.input import Input
from src.Model.exception_logging.exception import *


__author__ = 'Ondřej Lanč'


def get_env(var):
    """Get environment variable."""
    try:
        return os.environ[var]
    except KeyError:
        log.warning(
            'Unable to get the value of ' + var +
            ' environment variable!'
        )
        return None


def expand_variables(string, variables=None):
    """Expand references to environment variables and variables in given hash list."""
    if not variables:
        variables = {}
    for match in re.finditer(r"\$\{?(\w*)\}?", string):
        var = match.group(1)
        if var in variables:
            val = variables[var]
        else:
            val = get_env(var)
        if val is None:
            # If variable is not found, replace it's occurence with empty string
            val = ""
        string = string.replace(match.group(0), val)
    return string


class XMLParser(Input):

    class Paths(object):
        """Structure containing paths used in package."""

        def __init__(self):
            self.homeDir = ""
            self.packageDir = ""
            self.helpDirs = {}
            self.listDirs = []
            self.defaultValuesDirs = []
            self.listFiles = {}

            self.templateFile = FcFileLocation()
            self.dependenciesFile = FcFileLocation()
            self.guiTemplateFile = FcFileLocation()
            self.helpFile = FcFileLocation()
            self.guiLabelFile = ""
            self.defaultValuesFile = FcFileLocation()
            self.outputFile = FcFileLocation()

        @property
        def main_dir(self):
            """Return location of main package or plugin directory."""
            return self.packageDir

        @property
        def header_file_full_path(self):
            return os.path.join(self.main_dir, 'header.xml')

    def __init__(self, main_dir):
        super().__init__()
        self._paths = XMLParser.Paths()
        self._paths.packageDir = main_dir

    def _expand_file_name(self, filename):
        """Expand file name. Filename can contain references to environment variables
        in form $VAR or ${VAR}."""
        return expand_variables(filename,
                                {
                                    "HOME": self._paths.homeDir,
                                    "PACKAGE": self._paths.packageDir,
                                    "PLUGIN": self._paths.main_dir
                                }
                                )

    def _load_header_file(self, package):
        log.info("Parsing header file " + self._paths.header_file_full_path)
        header_file_parser = HeaderFileReader()
        if package.is_plugin:
            header_file_parser.parse(self._paths.header_file_full_path, self)
        else:
            header_file_parser.parse(self._paths.header_file_full_path)
        header_structure = header_file_parser.headerStructure

        # Path to template file
        self._paths.templateFile = header_structure.templateFile
        self._paths.templateFile.fullPath = os.path.join(self._paths.main_dir, header_structure.templateFile.name)
        # Path to dependencies file
        if header_structure.dependenciesFile:
            self._paths.dependenciesFile = header_structure.dependenciesFile
            self._paths.dependenciesFile.fullPath = os.path.join(self._paths.main_dir,
                                                                 header_structure.dependenciesFile.name)
        # Path to gui template file
        if header_structure.guiTemplateFile:
            self._paths.guiTemplateFile = header_structure.guiTemplateFile
            self._paths.guiTemplateFile.fullPath = os.path.join(self._paths.main_dir,
                                                                header_structure.guiTemplateFile.name)
        # Path to output file
        if header_structure.outputFile:
            self._paths.outputFile = header_structure.outputFile
            self._paths.outputFile.fullPath = self._expand_file_name(header_structure.outputFile.name)

        self._paths.helpFile = header_structure.helpFile
        self._paths.guiLabelFile = header_structure.guiLabelFile
        self._paths.defaultValuesFile = header_structure.defaultValuesFile

        # Process groups
        for group in header_structure.groups.values():
            if group.native_output.name:
                group.native_output.fullPath = self._expand_file_name(group.native_output.name)
            if group.transform.name:
                group.transform.fullPath = os.path.join(self._paths.main_dir, group.transform.name)
        for group in package.available_groups.values():
            for i in group.include_transform:
                i.fullPath = os.path.join(self._paths.main_dir, i.name)
        package.groups = header_structure.groups
        # Create default group if there was no in the header file
        if len(package.groups) == 0:
            log.warning("No group defined in header file. Creating default group.")
            group = FcGroup("default")
            package.groups[group.name] = group

        # Fill map of listFiles.
        for f in header_structure.listFiles:
            # We do not know path to list file, so it is empty for now.
            self._paths.listFiles[f] = None

    def load_package(self, package, load_languages):
        """Base function for package load."""
        self._load_header_file(package)

    def config(self):
        pass

    def input(self):
        pass

    def load_config_file(self, package):
        pass

    def load_plugins(self, package, load_languages):
        pass