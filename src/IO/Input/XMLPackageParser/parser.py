#!/usr/bin/python3
#
import os
import re

from Model.group import FcGroup
from Model.package import Plugin
from IO.Input.XMLPackageParser.config_file import ConfigFileReader
from IO.Input.XMLPackageParser.default_file import DefaultFile
from IO.Input.XMLPackageParser.dependencies_file import DependenciesFile
from IO.Input.XMLPackageParser.header_file import HeaderFileReader
from IO.Input.XMLPackageParser.help_file import HelpFile
from IO.Input.XMLPackageParser.list_file import ListFile
from IO.Input.XMLPackageParser.list_help_file import ListHelpFile
from IO.Input.XMLPackageParser.template_file import TemplateFile
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
        val = None
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

    def __init__(self, paths):
        super().__init__()
        self._paths = paths

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

    def _load_header_file(self):
        log.info("Parsing header file " + self._paths.header_file_full_path)
        header_file_parser = HeaderFileReader()
        if self._package.is_plugin:
            header_file_parser.parse(self._paths.header_file_full_path, self)
        else:
            header_file_parser.parse(self._paths.header_file_full_path)
        headerStructure = header_file_parser.headerStructure

        # Path to template file
        self._paths.templateFile = headerStructure.templateFile
        self._paths.templateFile.fullPath = os.path.join(self._paths.main_dir, headerStructure.templateFile.name)
        # Path to dependencies file
        if headerStructure.dependenciesFile:
            self._paths.dependenciesFile = headerStructure.dependenciesFile
            self._paths.dependenciesFile.fullPath = os.path.join(self._paths.main_dir,
                                                                 headerStructure.dependenciesFile.name)
        # Path to gui template file
        if headerStructure.guiTemplateFile:
            self._paths.guiTemplateFile = headerStructure.guiTemplateFile
            self._paths.guiTemplateFile.fullPath = os.path.join(self._paths.main_dir,
                                                                headerStructure.guiTemplateFile.name)
        # Path to output file
        if headerStructure.outputFile:
            self._paths.outputFile = headerStructure.outputFile
            self._paths.outputFile.fullPath = self._expand_file_name(headerStructure.outputFile.name)

        self._paths.helpFile = headerStructure.helpFile
        self._paths.guiLabelFile = headerStructure.guiLabelFile
        self._paths.defaultValuesFile = headerStructure.defaultValuesFile

        # Process groups
        for group in headerStructure.groups.values():
            if group.native_output.name:
                group.native_output.fullPath = self._expand_file_name(group.native_output.name)
            if group.transform.name:
                group.transform.fullPath = os.path.join(self._paths.main_dir, group.transform.name)
        for group in self._package.available_groups.values():
            for i in group.include_transform:
                i.fullPath = os.path.join(self._paths.main_dir, i.name)
        self._package.groups = headerStructure.groups
        # Create default group if there was no in the header file
        if len(self._package.groups) == 0:
            log.warning("No group defined in header file. Creating default group.")
            group = FcGroup("default")
            self._package.groups[group.name] = group

        # Fill map of listFiles.
        for f in headerStructure.listFiles:
            # We do not know path to list file, so it is empty for now.
            self._paths.listFiles[f] = None

    def _find_help_file(self):
        """Find path to help file."""
        if not self._paths.helpFile:
            return

        for lang in self._package.availableLanguages:
            self._paths.helpDirs[lang] = self._paths.main_dir + "/L10n/" + lang
        if self._package.current_language in self._package.availableLanguages:
            self._paths.helpFile.fullPath = os.path.join(self._paths.helpDirs[self._package.current_language],
                                                         self._paths.helpFile.name)
        else:
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

    def _load_help_file(self):
        """Load help file. Must be called after _findHelpFile."""
        # Parse the file
        log.info('Parsing help file ' + self._paths.helpFile.fullPath)
        help_file_parser = HelpFile()
        help_file_parser.parse(
            self._paths.helpFile.fullPath,
            self._package.tree,
            self._package.current_language
        )

    def _load_template_file(self):
        """Load template file. Support function for loadPackage."""
        log.info('Parsing template file ' + self._paths.templateFile.fullPath)
        template_file_parser = TemplateFile()
        self._package.tree = template_file_parser.parse(
            self._paths.templateFile.fullPath,
            self._package.tree,
            self._package.available_groups,
            self._package.available_lists,
            self
        )

    def _load_dependencies_file(self):
        if not os.access(self._paths.dependenciesFile.fullPath, os.R_OK):
            log.warning("Dependencies file " + self._paths.dependenciesFile.fullPath + " is missing.")
            return
        log.info('Parsing dependencies file ' + self._paths.dependenciesFile.fullPath)
        dependencies_file_parser = DependenciesFile()
        # Parse the dependency file first
        self._package.dependencies = dependencies_file_parser.parse(self._paths.dependenciesFile.fullPath)

    def _load_default_values_file(self):
        """Load default values file. Support function for loadPackage."""
        file = None
        for dir in self._paths.defaultValuesDirs:
            file = os.path.join(dir, self._paths.defaultValuesFile.name)
            if os.access(file, os.R_OK):
                break
        else:
            log.error(
                'Unable to find default values file ' +
                self._paths.defaultValuesFile.name + '!'
            )
            return
        # Parse the file
        log.info("Parsing default values file " + file)
        self._paths.defaultValuesFile.fullPath = file
        default_file_parser = DefaultFile()
        default_file_parser.parse(file, self._package.tree)

    def _load_list_help(self, fileName, loadAllLanguages):
        """Load list help file for given list file.
         Labels and descriptions will be stored in self.data.lists"""
        assert not loadAllLanguages  # Loading of all languages is not supported yet for list help files.
        file_path = self._paths.listFiles[fileName]
        assert file_path is not None
        # Get directory from full path
        dir = os.path.dirname(file_path)
        # path to help file for current language
        f = os.path.join(dir, 'L10n', self._package.current_language, fileName)
        # TODO: pokud nenajdeme current language, nacteme alespon nejaky jiny pokud je dostupny
        if not os.access(f, os.R_OK):
            # Failed to find list help file
            log.warn('Unable to find help file for list ' + fileName)
            return

        # Parse the file
        log.info('Parsing list help file ' + f)
        help_parser = ListHelpFile()
        help_parser.parse(f, self._package.lists)

    def _load_lists(self, loadAllLanguages):
        """Load list files."""
        # Build list of possible list locations
        # Find list files and parse them
        for fileName in self._paths.listFiles:
            if self._paths.listFiles[fileName] is not None:
                # Skip already loaded lists
                continue
            file = None  # Full path to list file
            for dir in self._paths.listDirs:  # TODO: Docasne rozsirit list dirs?
                file = os.path.join(dir, fileName)
                if os.access(file, os.R_OK):
                    break
            else:
                log.error('Unable to find list file ' + fileName + '!')
                continue

            # Parse list file
            log.info('Parsing list file ' + file)
            list_parser = ListFile()
            list_parser.parse(file, self._package.lists)
            # Assign full path to list file name
            self._paths.listFiles[fileName] = file

            # Load help
            self._load_list_help(fileName, loadAllLanguages)

    def _load_config_file(self):
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
        config_file_parser.parse(self._paths.outputFile.fullPath, self._package.tree)

    def load_package(self, loadAllLanguages):
        """Base function for package load."""
        self._load_header_file()
        self._find_help_file(loadAllLanguages)
        # Load list files
        self._load_lists(loadAllLanguages)
        # Template file
        self._load_template_file()
        # Help file
        if self._paths.helpFile.fullPath:
            self._load_help_file()
        # Default config file
        if self._paths.defaultValuesFile:
            self._load_default_values_file()
        # Load config file
        self._load_config_file()
        # Dependencies file
        # We have to load it when config tree is filled
        if self._paths.dependenciesFile:
            self._load_dependencies_file()

    def load_plugins(self, loadAllLanguages):
        """Load all plugins found in plugin directory."""
        # Search plugin directory
        dirs = []
        try:
            dirs = os.listdir(os.path.join(self._paths.packageDir, 'plugins'))
        except OSError:
            log.warning("Directory plugins does not exist!")
            return
        # Process plugins
        for p in dirs:
            path = os.path.join(self._paths.packageDir, 'plugins', p)  # Path to plugin directory
            log.info("Loading plugin " + os.path.join(path, 'header.xml'))
            if not os.access(os.path.join(path, 'header.xml'), os.R_OK):
                # Skip directories with no header file.
                log.warning("No header file found for plugin %s!" % (p,))
                continue
            # Create plugin and load it
            plugin = Plugin(p, self)
            plugin.load_package(loadAllLanguages)
            self._package.plugin.append(plugin)


