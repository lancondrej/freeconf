#!/usr/bin/python3
#
import os
import re
from IO.Input.XMLPackageParser.config_file import ConfigFileReader
from IO.Input.XMLPackageParser.default_file import DefaultFile
from IO.Input.XMLPackageParser.help_file import HelpFile
from IO.Input.XMLPackageParser.list_file import ListFile
from IO.Input.XMLPackageParser.list_help_file import ListHelpFile
from IO.Input.XMLPackageParser.template_file import TemplateFile
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
            self.listDir = ""
            self.defaultValuesDir = ""
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

        @main_dir.setter
        def main_dir(self, dir):
            self.packageDir=dir
            self.listDir = os.path.join(self.packageDir, 'lists')
            self.defaultValuesDir = self.packageDir

        @property
        def header_file_full_path(self):
            return os.path.join(self.main_dir, 'header.xml')

    def __init__(self, main_dir):
        super().__init__()
        self._paths = XMLParser.Paths()
        self._paths.main_dir = main_dir

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

    def _load_template_file(self, package):
        """Load template file. Support function for loadPackage."""
        log.info('Parsing template file ' + self._paths.templateFile.fullPath)
        template_file_parser = TemplateFile()
        package.tree = template_file_parser.parse(
            self._paths.templateFile.fullPath,
            package.tree,
            package.available_groups,
            package.available_lists,
            self
        )

    def _find_help_file(self, package):
        """Find path to help file."""
        try:
            package.availableLanguages = os.listdir(self._paths.main_dir + '/L10n/')
        except OSError:
            package.availableLanguages = []
        if not self._paths.helpFile:
            return  # TODO nějaká rozumná chyba
        for lang in package.availableLanguages:
            self._paths.helpDirs[lang] = self._paths.main_dir + "/L10n/" + lang
        if package.current_language in package.availableLanguages:
            self._paths.helpFile.fullPath = os.path.join(self._paths.helpDirs[package.current_language],
                                                         self._paths.helpFile.name)
        else:
            # TODO udělat nahrání podle pořadí pref jazyků
            # Try to find any help file
            for lang, path in self._paths.helpDirs.items():
                f = os.path.join(path, self._paths.helpFile.name)
                if os.access(f, os.R_OK):
                    self.currentLanguage = lang
                    self._paths.helpFile.fullPath = f
                    break
            else:
                log.error('Unable to find help file ' + self._paths.helpFile.name)
                return

    def _load_lists(self, package):
        """Load list files."""
        # Build list of possible list locations
        # Find list files and parse them
        for fileName in self._paths.listFiles:
            if self._paths.listFiles[fileName] is not None:
                # Skip already loaded lists
                continue
            file = None  # Full path to list file
            file = os.path.join(self._paths.listDir, fileName)
            if not os.access(file, os.R_OK):
                log.error('Unable to find list file ' + fileName + '!')

            # Parse list file
            log.info('Parsing list file ' + file)
            list_parser = ListFile()
            list_parser.parse(file, package.lists)
            # Assign full path to list file name
            self._paths.listFiles[fileName] = file

            # Load help
            self._load_list_help(fileName, package)

    def _load_list_help(self, fileName, package):
        """Load list help file for given list file.
         Labels and descriptions will be stored in self.data.lists"""
        file_path = self._paths.listFiles[fileName]
        assert file_path is not None
        # Get directory from full path
        dir = os.path.dirname(file_path)
        # path to help file for current language
        f = os.path.join(dir, 'L10n', package.current_language, fileName)
        # TODO: pokud nenajdeme current language, nacteme alespon nejaky jiny pokud je dostupny
        if not os.access(f, os.R_OK):
            # Failed to find list help file
            log.warn('Unable to find help file for list ' + fileName)
            return

        # Parse the file
        log.info('Parsing list help file ' + f)
        help_parser = ListHelpFile()
        help_parser.parse(f, package.lists)

    def _load_help_file(self, package):
        """Load help file. Must be called after _findHelpFile."""
        # Parse the file
        log.info('Parsing help file ' + self._paths.helpFile.fullPath)
        help_file_parser = HelpFile()
        help_file_parser.parse(
            self._paths.helpFile.fullPath,
            package.tree,
            package.current_language
        )

    def _load_default_values_file(self, package):
        """Load default values file. Support function for loadPackage."""
        file = None
        file = os.path.join(self._paths.defaultValuesDir, self._paths.defaultValuesFile.name)
        if not os.access(file, os.R_OK):
            log.error(
                'Unable to find default values file ' +
                self._paths.defaultValuesFile.name + '!'
            )
            return
        # Parse the file
        log.info("Parsing default values file " + file)
        self._paths.defaultValuesFile.fullPath = file
        default_file_parser = DefaultFile()
        default_file_parser.parse(file, package.tree)

    def _load_config_file(self, package):
        """Load config file."""
        if not os.access(self._paths.outputFile.fullPath, os.R_OK):
            log.warning(
                "Configuration file " + self._paths.outputFile.fullPath +
                " is missing. Probably running for the first time."
            )
            # Touch the configuration file
            # self.data.configFile.touch(self.paths.outputFile.fullPath, self.templateTree)
            return
        if not os.access(self._paths.outputFile.fullPath, os.W_OK):
            log.error(
                "Configuration file " + self._paths.outputFile.fullPath + " is not writable!"
            )
            return
        # Parse the file
        log.info("Parsing configuration file " + self._paths.outputFile.fullPath)
        config_file_parser = ConfigFileReader()
        config_file_parser.parse(self._paths.outputFile.fullPath, package.tree)

    def load_package(self, package):
        """Base function for package load."""
        self._load_header_file(package)
        self._find_help_file(package)
        # Load list files
        self._load_lists(package)
        self._load_template_file(package)
        if self._paths.helpFile.fullPath:
            self._load_help_file(package)
        # Default config file
        if self._paths.defaultValuesFile:
            self._load_default_values_file(package)
        self._load_config_file(package)

    def input(self):
        pass

    def load_config_file(self, file, package):
        self._load_config_file(package)

    def load_plugins(self, package):
        pass