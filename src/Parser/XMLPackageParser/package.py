#!/usr/bin/python3
#
import os
import re

from src.Model.exception_logging.exception import *
from Parser.file import FcFileLocation


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


def expand_variables(string, variables={}):
    """Expand references to environment variables and variables in given hash list."""
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


class PackageBase(object):
    """Base class for package and plugin classes."""

    class Paths(object):
        """Structure containing paths used in package."""

        def __init__(self):
            self.homeDir = ""
            self.packageName = ""
            self.packageDir = ""
            self.helpDirs = {}
            self.listDirs = []
            self.freeconfDirs = []
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

    class Data(object):
        def __init__(self):
            # Package data
            self.lists = {}
            self.groups = {}
            self.availableLanguages = []
            self.dependencies = []

        def fill(self, mainDir):
            try:
                self.availableLanguages = os.listdir(mainDir + '/L10n/')
            except OSError:
                self.availableLanguages = []

    def __init__(self, tree, data, paths, parser):
        self.trees = tree
        self.data = data
        self.paths = paths
        self.parser = parser

    @property
    def is_plugin(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @property
    def current_language(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @property
    def available_lists(self):
        """Return list of available value lists."""
        return self.data.lists

    @property
    def available_groups(self):
        """Return list of available groups."""
        return self.data.groups

    def add_group(self, group):
        if group.name in self.data.groups:
            raise AlreadyExistsError("Group with name %s already exists!" % (group.name,))
        self.data.groups[group.name] = group

    def remove_group(self, name):
        if name not in self.data.groups:
            raise NotExistsError("Group with name %s does not exist!" % (name,))
        del self.data.groups[name]

    def expand_file_name(self, filename):
        """Expand file name. Filename can contain references to environment variables
        in form $VAR or ${VAR}."""
        return expand_variables(filename,
                                {
                                    "HOME": self.paths.homeDir,
                                    "PACKAGE": self.paths.packageDir,
                                    "PLUGIN": self.paths.main_dir
                                }
        )

    def _loadHeaderFile(self):
        log.info("Parsing header file " + self.paths.header_file_full_path)
        headerFileParser = HeaderFileReader()
        if self.is_plugin:
            headerFileParser.parse(self.paths.header_file_full_path, self)
        else:
            headerFileParser.parse(self.paths.header_file_full_path)
        headerStructure = headerFileParser.headerStructure

        # Path to template file
        self.paths.templateFile = headerStructure.templateFile
        self.paths.templateFile.fullPath = os.path.join(self.paths.main_dir, headerStructure.templateFile.name)
        # Path to dependencies file
        if headerStructure.dependenciesFile:
            self.paths.dependenciesFile = headerStructure.dependenciesFile
            self.paths.dependenciesFile.fullPath = os.path.join(self.paths.main_dir,
                                                                headerStructure.dependenciesFile.name)
        # Path to gui template file
        if headerStructure.guiTemplateFile:
            self.paths.guiTemplateFile = headerStructure.guiTemplateFile
            self.paths.guiTemplateFile.fullPath = os.path.join(self.paths.main_dir,
                                                               headerStructure.guiTemplateFile.name)
        # Path to output file
        if headerStructure.outputFile:
            self.paths.outputFile = headerStructure.outputFile
            self.paths.outputFile.fullPath = self.expand_file_name(headerStructure.outputFile.name)

        self.paths.helpFile = headerStructure.helpFile
        self.paths.guiLabelFile = headerStructure.guiLabelFile
        self.paths.defaultValuesFile = headerStructure.defaultValuesFile

        # Process groups
        for group in headerStructure.groups.values():
            if group.nativeFile.name:
                group.nativeFile.fullPath = self.expand_file_name(group.nativeFile.name)
            if group.transformFile.name:
                group.transformFile.fullPath = os.path.join(self.paths.main_dir, group.transformFile.name)
        for group in self.available_groups.values():
            for i in group.includedTransformFiles:
                i.fullPath = os.path.join(self.paths.main_dir, i.name)
        self.data.groups = headerStructure.groups
        # Create default group if there was no in the header file
        if len(self.data.groups) == 0:
            log.warning("No group defined in header file. Creating default group.")
            group = FcGroup("default")
            self.data.groups[group.name] = group

        # Fill map of listFiles.
        for f in headerStructure.listFiles:
            # We do not know path to list file, so it is empty for now.
            self.paths.listFiles[f] = None

    def writeHeaderFile(self):
        """Save header file."""
        log.info("Saving header file " + self.paths.header_file_full_path)
        ## Create and fill header structure
        headerStructure = HeaderStructure()
        headerStructure.packageName = self.paths.packageName
        headerStructure.templateFile = self.paths.templateFile
        headerStructure.dependenciesFile = self.paths.dependenciesFile
        headerStructure.guiTemplateFile = self.paths.guiTemplateFile
        headerStructure.helpFile = self.paths.helpFile
        headerStructure.guiLabelFile = self.paths.guiLabelFile
        headerStructure.defaultValuesFile = self.paths.defaultValuesFile
        headerStructure.listFiles = self.paths.listFiles.keys()
        headerStructure.outputFile = self.paths.outputFile
        headerStructure.groups = self.data.groups
        # Create writer and save header file
        writer = HeaderFileWriter(headerStructure)
        writer.write(self.paths.header_file_full_path)

    def _findHelpFile(self, loadAllLanguages):
        """Find path to help file."""
        if not self.paths.helpFile:
            return

        for lang in self.data.availableLanguages:
            self.paths.helpDirs[lang] = self.paths.main_dir + "/L10n/" + lang
        if self.current_language in self.data.availableLanguages:
            self.paths.helpFile.fullPath = os.path.join(self.paths.helpDirs[self.current_language],
                                                        self.paths.helpFile.name)
        else:
            # Try to find any help file
            for lang, path in self.paths.helpDirs.items():
                f = os.path.join(path, self.paths.helpFile.name)
                if os.access(f, os.R_OK):
                    self.currentLanguage = lang
                    self.paths.helpFile.fullPath = f
                    break
            else:
                log.error('Unable to find help file ' + self.paths.helpFile.name)
                return

    def _loadHelpFile(self):
        """Load help file. Must be called after _findHelpFile."""
        # Parse the file
        log.info('Parsing help file ' + self.paths.helpFile.fullPath)
        helpFileParser = HelpFile()
        helpFileParser.parse(
            self.paths.helpFile.fullPath,
            self.trees.templateTree,
            self.current_language
        )

    def _loadTemplateFile(self):
        """Load template file. Support function for loadPackage."""
        log.info('Parsing template file ' + self.paths.templateFile.fullPath)
        templateFileParser = TemplateFile()
        self.trees.templateTree = templateFileParser.parse(
            self.paths.templateFile.fullPath,
            self.trees.templateTree,
            self.available_groups,
            self.available_lists,
            self
        )

    def _loadDependenciesFile(self):
        if not os.access(self.paths.dependenciesFile.fullPath, os.R_OK):
            log.warning("Dependencies file " + self.paths.dependenciesFile.fullPath + " is missing.")
            return
        log.info('Parsing dependencies file ' + self.paths.dependenciesFile.fullPath)
        dependenciesFileParser = DependenciesFile()
        # Parse the dependency file first
        self.data.dependencies = dependenciesFileParser.parse(self.paths.dependenciesFile.fullPath)

    def _loadDefaultValuesFile(self):
        """Load default values file. Support function for loadPackage."""
        file = None
        for dir in self.paths.defaultValuesDirs:
            file = os.path.join(dir, self.paths.defaultValuesFile.name)
            if os.access(file, os.R_OK):
                break
        else:
            log.error(
                'Unable to find default values file ' +
                self.paths.defaultValuesFile.name + '!'
            )
            return
        # Parse the file
        log.info("Parsing default values file " + file)
        self.paths.defaultValuesFile.fullPath = file
        defaultFileParser = DefaultFile()
        defaultFileParser.parse(file, self.trees.templateTree)

    # TODO: handle error

    def _loadGUITemplateFile(self, buildDefault=True):
        """Load GUI template file. Support function for loadPackage."""
        error = False
        if not self.paths.guiTemplateFile:
            log.warning("GUI template file was not defined!")
            error = True
        elif not os.access(self.paths.guiTemplateFile.fullPath, os.R_OK):
            log.warning("GUI template file %s is missing." % (self.paths.guiTemplateFile.name,))
            error = True;

        if error == False:
            log.info("Parsing gui template file " + self.paths.guiTemplateFile.fullPath)
            guiParser = GUITemplateFile()
            # try:
            guiParser.parse(self.paths.guiTemplateFile.fullPath, self.trees.configTree, self.trees.guiTree)
            return False
        # except:
        # log.error("Cannot parse the GUI template file")
        # error = True
        elif buildDefault:
            # TODO: Tenhle default kod bude mozna lepsi prehodit nekam jinam
            log.info("Unable to parse gui template file, reverting to fallback!")
            if len(self.trees.guiTree.entries) == 0:
                self.trees.guiTree = FcGWindow()
                self.trees.guiTree.title = "freeconf generated config dialog"

            # Create Tab for all settings
            all_tab = self.trees.guiTree.findEntry("all-tab")[1]
            if all_tab == None:
                all_tab = FcGTab()
                all_tab.name = "all-tab"
                all_tab.label = "All"
                all_tab.description = "General fallback tab"
                self.trees.guiTree.append(all_tab)
            if all_tab.content == None:
                # Create top level GUI Section entry
                rootSection = FcCGSEntry()
                # rootSection.configBuddy = self.trees.configTree
                #self.trees.configTree = rootSection
                rootSection.name = "rootSection"
                all_tab.content = rootSection
                all_tab.content.configBuddy = self.trees.configTree
            # Fill the tab
            all_tab.content.fill(self.trees.configTree)
            return True
        return False

    def _loadListHelp(self, fileName, loadAllLanguages):
        """Load list help file for given list file.
		   Labels and descriptions will be stored in self.data.lists"""

        assert loadAllLanguages == False  # Loading of all languages is not supported yet for list help files.

        filePath = self.paths.listFiles[fileName]
        assert filePath != None

        # Get directory from full path
        dir = os.path.dirname(filePath)
        # path to help file for current language
        f = os.path.join(dir, 'L10n', self.current_language, fileName)
        # TODO: pokud nenajdeme current language, nacteme alespon nejaky jiny pokud je dostupny
        if not os.access(f, os.R_OK):
            # Failed to find list help file
            log.warn('Unable to find help file for list ' + fileName)
            return

        # Parse the file
        log.info('Parsing list help file ' + f)
        helpParser = ListHelpFile()
        helpParser.parse(f, self.data.lists)

    def _loadLists(self, loadAllLanguages):
        """Load list files."""
        # Build list of possible list locations
        # Find list files and parse them
        for fileName in self.paths.listFiles:
            if self.paths.listFiles[fileName] != None:
                # Skip already loaded lists
                continue
            file = None  # Full path to list file
            for dir in self.paths.listDirs:  # TODO: Docasne rozsirit list dirs?
                file = os.path.join(dir, fileName)
                if os.access(file, os.R_OK):
                    break
            else:
                log.error('Unable to find list file ' + fileName + '!')
                continue

            # Parse list file
            log.info('Parsing list file ' + file)
            listParser = ListFile()
            listParser.parse(file, self.data.lists)
            # Assign full path to list file name
            self.paths.listFiles[fileName] = file

            # Load help
            self._loadListHelp(fileName, loadAllLanguages)

    def _loadConfigFile(self):
        """Load config file."""
        if not os.access(self.paths.outputFile.fullPath, os.R_OK):
            log.warning(
                "Configuration file " + self.paths.outputFile.fullPath +
                " is missing. Probably running for the first time."
            )
            ## Touch the configuration file
            # self.data.configFile.touch(self.paths.outputFile.fullPath, self.templateTree)
            return
        if not os.access(self.paths.outputFile.fullPath, os.W_OK):
            log.error(
                "Configuration file " + self.paths.outputFile.fullPath + " is not writable!"
            )
            return
        # Parse the file
        log.info("Parsing configuration file " + self.paths.outputFile.fullPath)
        configFileParser = ConfigFileReader()
        configFileParser.parse(self.paths.outputFile.fullPath, self.trees.configTree)

    # TODO: handle error

    def loadPackageBase(self, loadAllLanguages):
        """Base function for package load."""
        self._loadHeaderFile()

        self._findHelpFile(loadAllLanguages)

        ## Load list files
        self._loadLists(loadAllLanguages)

        ## Template file
        self._loadTemplateFile()

        ## Help file
        if self.paths.helpFile.fullPath:
            self._loadHelpFile()

        ## Initialize config structure
        if self.trees.configTree == None:
            self.trees.configTree = self.trees.templateTree.createCEntry(None)

        # Default config file
        if self.paths.defaultValuesFile:
            self._loadDefaultValuesFile()

        ## Load config file
        self._loadConfigFile()

        # Fill the rest of the config tree
        self.trees.configTree.fill()

        self.trees.configTree.initInconsistency()

        ## Dependencies file
        # We have to load it when config tree is filled
        if self.paths.dependenciesFile:
            self._loadDependenciesFile()

        ## GUI file
        error = self._loadGUITemplateFile()

        # GUI label file
        if error == False and self.paths.guiTemplateFile and self.paths.guiLabelFile:
            self._loadGUILabelFile(loadAllLanguages)


    def transform(self, groupName="default"):
        """Write native config files for all groups."""
        for group in self.data.groups.values():
            group.write_native(self.trees.configTree)

    def executeDependencies(self):
        # Resolve all loaded dependencies using root_entry as configuration tree. Call this function after parse.
        for dep in self.data.dependencies[:]:
            # Dependency resolved -> execute it
            dep.execute()

    def writeOutput(self):
        # Write output file
        if self.paths.outputFile.fullPath == "":
            # TODO: Spadnout tady nebo ne?
            log.error("Can't write output XML file! Path was not set.")
            return

        log.info("Writing output file " + self.paths.outputFile.fullPath)
        with open(self.paths.outputFile.fullPath, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n")
            f.write(self.trees.configTree.output(package=self, writeHelp=False, writeType=False))

    def writeDefault(self):
        if not self.paths.defaultValuesFile.fullPath:
            self.paths.defaultValuesFile.fullPath = os.path.join(self.paths.main_dir, self.paths.defaultValuesFile.name)
        log.info("Writing default values file " + self.paths.defaultValuesFile.fullPath)
        with open(self.paths.defaultValuesFile.fullPath, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n")
            f.write(self.trees.templateTree.outputDefault(self))


class Plugin(PackageBase):
    """Class representing plugin."""

    class Paths(PackageBase.Paths):
        """Structure containing paths used in package."""

        def __init__(self, paths):
            PackageBase.Paths.__init__(self)
            # Initialize needed paths from object of type FcPackageBase.Paths
            self.homeDir = paths.homeDir
            self.packageName = paths.packageName
            self.packageDir = paths.packageDir
            self.listDirs = paths.listDirs
            self.freeconfDirs = paths.freeconfDirs
            self.defaultValuesDirs = self.defaultValuesDirs
            # Path to plugin directory
            self.pluginDir = ""

        @property
        def main_dir(self):
            """Return location of main package or plugin directory."""
            return self.pluginDir

        def fill(self, path):
            # Fill plugin path
            self.pluginDir = path

            # Extend list of possible value lists locations
            self.listDirs.insert(0, os.path.join(self.pluginDir, 'lists'))

            # Extend in list of possible default values locations
            self.defaultValuesDirs.insert(0, self.pluginDir)


    def __init__(self, name, package):
        self.name = name  # Name of plugin
        self.trees = package.trees
        self.data = PackageBase.Data()  # Plugin has local data
        self.paths = self.Paths(package.paths)
        self.package = package  # Reference to main package

    @property
    def is_plugin(self):
        return True

    @property
    def current_language(self):
        """Return current language of the package."""
        return self.package.current_language

    @property
    def available_lists(self):
        """Return list of available value lists."""
        tmp = dict(self.package.data.lists)
        tmp.update(self.data.lists)
        return tmp

    @property
    def available_groups(self):
        """Return list of available groups."""
        tmp = dict(self.data.groups)
        tmp.update(self.package.data.groups)
        return tmp

    def load(self, path, loadAllLanguages):
        """Load the plugin in given path."""
        # Gather information about paths in plugin
        self.paths.fill(path)
        self.data.fill(self.paths.main_dir)
        # Load plugin's files
        self.loadPackageBase(loadAllLanguages)


class Package(PackageBase):
    class Paths(PackageBase.Paths):
        def __init__(self):
            PackageBase.Paths.__init__(self)

        def fill(self, packageName):
            self.homeDir = get_env('HOME')
            # Initialize freeconf dirs -> tohle by melo byt v konfiguraku
            self.freeconfDirs = [
                self.homeDir + '/.freeconf',
                '/usr/local/share/freeconf',
                '/usr/share/freeconf'  # 'D:\Skola\workspace\FreeConf'
            ]

            # Find package with existing header file
            if packageName[0] == os.sep:
                # Package name is full path
                if not os.access(packageName, os.R_OK):
                    raise FcPackageLoadError("Cannot find package " + packageName)
                self.packageDir = packageName
                (tmp, self.packageName) = os.path.split(packageName)
                # Check header file location
                if not os.access(self.header_file_full_path, os.R_OK):
                    raise FcPackageLoadError("Cannot find header file for package " + packageName)
            else:
                # Build list of possible locations for our package
                packageDirs = [
                    os.path.join(d, 'packages', packageName)
                    for d in self.freeconfDirs
                ]
                for d in packageDirs:
                    f = os.path.join(d, 'header.xml')
                    if os.access(f, os.R_OK):
                        # Package with header file found!
                        self.packageDir = d
                        self.packageName = packageName
                        break
                else:
                    raise FcPackageLoadError("Cannot find package " + packageName)

            # Fill in list of possible value lists locations
            self.listDirs = [
                os.path.join(dir, 'lists')
                for dir in [self.packageDir] + self.freeconfDirs
            ]

            # Fill in list of possible default values locations
            self.defaultValuesDirs = [
                self.packageDir,
                self.homeDir + '/.freeconf/default'  # 'D:\Skola\workspace\FreeConf\default'
            ]


    def __init__(self):
        PackageBase.__init__(
            self,
            self.Trees(),
            self.Data(),
            self.Paths()
        )
        # Get current language
        # self.currentLanguage = getEnv('LANG').split('.')[0]
        self.currentLanguage = locale.getdefaultlocale('LANG')
        # List of loaded plugins
        self.plugins = []

    @property
    def is_plugin(self):
        return False

    @property
    def current_language(self):
        """Return current language of the package."""
        return self._currentLanguage

    @current_language.setter
    def currentLanguage(self, lang):
        """Current language settter."""
        self._currentLanguage = lang

    def _loadGUILabelFile(self, loadAllLanguages):
        """Load GUI label file. Support function for loadPackage."""
        f = None
        for key, dir in self.paths.helpDirs.items():
            f = os.path.join(dir, self.paths.guiLabelFile.name)
            if os.access(f, os.R_OK):
                break
        else:
            log.info("GUI label file " + self.paths.guiLabelFile.name + " is missing.")
            return

        self.paths.guiLabelFile.fullPath = f

        log.info("Parsing the GUI label file " + self.paths.guiLabelFile.fullPath)
        labelParser = GUILabelFile()
        # try:
        labelParser.parse(self.paths.guiLabelFile.fullPath, self.trees.guiTree)

    # except:
    # log.error("Cannot parse the GUI label file")


    def _loadPlugins(self, loadAllLanguages):
        """Load all plugins found in plugin directory."""
        ## Search plugin directory
        dirs = []
        try:
            dirs = os.listdir(os.path.join(self.paths.packageDir, 'plugins'))
        except OSError:
            log.warning("Directory plugins does not exist!")
            return
        # Process plugins
        for p in dirs:
            path = os.path.join(self.paths.packageDir, 'plugins', p)  # Path to plugin directory
            log.info("Loading plugin " + os.path.join(path, 'header.xml'))
            if not os.access(os.path.join(path, 'header.xml'), os.R_OK):
                # Skip directories with no header file.
                log.warning("No header file found for plugin %s!" % (p,))
                continue
            # Create plugin and load it
            plugin = Plugin(p, self)
            plugin.load(path, loadAllLanguages)
            self.plugins.append(plugin)


    def loadPackage(self, name, loadAllLanguages=False, executeDependencies=True):
        # Gather information about package and paths in package.
        self.paths.fill(name)
        self.data.fill(self.paths.main_dir)

        # Load package files
        self.loadPackageBase(loadAllLanguages)

        ## Load Plugins
        self._loadPlugins(loadAllLanguages)

        ## Process dependencies
        # Delete all invalid dependencies
        for dep in self.data.dependencies[:]:
            if dep.resolve(self.trees.configTree, self.data.lists) == False:
                # Failed to resolve dependency -> Delete it from list of dependencies
                dep.unlink()
                self.data.dependencies.remove(dep)

        # update visibility of GUI widgets
        # must be before executing dependencies
        self.trees.guiTree.initState()

        if executeDependencies == True:
            self.executeDependencies()


    def writePackage(self):
        self.writeHeaderFile()
        self.writeTemplate()
        self.writeDefault()
        self.writeHelp()
        self.writeOutput()

    # TODO: Write plugins

    def writeTemplate(self):
        log.info("Writing template file " + self.paths.templateFile.fullPath)
        with open(self.paths.templateFile.fullPath, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<freeconf-template>\n")
            f.write("<section-name>" + self.trees.templateTree.name + "</section-name>\n")
            for node in self.trees.templateTree.entries:
                f.write(node.output())
            f.write("</freeconf-template>\n")

    def writeHelp(self, language="en"):
        path = ""
        if language not in self.paths.helpDirs.keys():
            try:
                path = os.path.join(self.paths.packageDir, "L10n", language)
                os.mkdir(path)
            except OSError:
                log.warning("Cannot create a new help directory " + language + \
                            " in the package, maybe the directory already exists.")
        else:
            path = self.paths.helpDirs[language]

        path += os.sep + self.paths.helpFile.name
        log.info("Writing help file " + path)
        with open(path, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<freeconf-help>\n")
            f.write(self.trees.templateTree.outputHelp(language))
            f.write("</freeconf-help>\n")

    def writeDefault(self):
        # Write default file for main package
        super(Package, self).writeDefault()
        # Write default files for all plugins
        for plugin in self.plugins:
            plugin.write_default()

    def writeOutput(self):
        """Redefinition of writeOutput. Write main output file and plugin output files."""
        if self.trees.guiTree.inconsistent == True:
            raise FcInconsistencyError("The package is in inconsistent state. Configuration XML file cannot be saved")

        # Write main output file - call original method
        super(Package, self).writeOutput()

        # Write config files of loaded plugins
        for plugin in self.plugins:
            plugin.write_output()
