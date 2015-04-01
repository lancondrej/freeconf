#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

from IO.Input.exception_logging.log import log
from IO.Input.XMLPackageParser.sax_file import XMLFileReader
from IO.Input.exception_logging.exception import ParseError
from IO.file import *
from src.Model.group import FcGroup


class HeaderStructure:
    """This structure contains file names for template file, help files, files with default values etc. which
    should be parsed to get all necessary information."""

    def __init__(self):
        # Initialize properties
        # Package name is necessary for constructing file name paths
        self.packageName = ""
        # Freeconf template file name
        self.templateFile = FcFileLocation()
        # Dependency file
        self.dependenciesFile = FcFileLocation()
        # Freeconf gui template file name
        self.guiTemplateFile = FcFileLocation()
        # Help file
        self.helpFile = FcFileLocation()
        # GUI label file
        self.guiLabelFile = FcFileLocation()
        # File with default values
        self.defaultValuesFile = FcFileLocation()
        # List of files with lists
        self.listFiles = []
        # Output file in freeconf format
        self.outputFile = FcFileLocation()
        # List of groups
        self.groups = {}

    def add_group(self, group):
        self.groups[group.name] = group

    def init_defaults(self, name):
        """Initialize header structure with default values for given package name."""
        # TODO: podpora pluginu
        self.packageName = name
        self.templateFile = FcFileLocation(name + "_template.xml")
        self.defaultValuesFile = FcFileLocation(name + "_default.xml")
        self.helpFile = FcFileLocation(name + "_help.xml")
        self.outputFile = FcFileLocation("${PACKAGE}/" + name + ".xml")
        # self.guiTemplateFile = name + "_gui_template.xml"
        # self.guiLabelFile = FcFileLocation(name + "_gui_label.xml")
        # Generate default group
        default_group = FcGroup("default")
        default_group.transform = FcFileLocation(name + "_transform.xml")
        default_group.native_output = FcFileLocation("${PACKAGE}/" + name + ".conf")
        default_group.output_defaults = True
        self.add_group(default_group)

    def __repr__(self):
        return "class(HeaderStructure):" + "\n" + \
               "  Package name: " + str(self.packageName) + "\n" + \
               "  Template file: " + str(self.templateFile) + "\n" + \
               "  GUI Template file: " + str(self.guiTemplateFile) + "\n" + \
               "  Dependency file: " + str(self.dependenciesFile) + "\n" + \
               "  Help file: " + str(self.helpFile) + "\n" + \
               "  GUI label file: " + str(self.guiLabelFile) + "\n" + \
               "  Default values file: " + str(self.defaultValuesFile) + "\n" + \
               "  List files: " + str(self.listFiles) + "\n" + \
               "  Output file: " + str(self.outputFile) + "\n"


class ElementEnum:
    """Constants for header elements"""
    NO_ELEMENT = 0
    TEMPLATE_FILE = 1
    GUI_TEMPLATE_FILE = 2
    DEPENDENCY_FILE = 3
    LISTS_FILE = 4
    HELP_FILE = 5
    GUI_LABEL_FILE = 6
    DEFAULT_VALUES_FILE = 7
    TRANSFORM_FILE = 8
    ADD_TRANSFORM_FILE = 9
    OUTPUT_FILE = 10
    NATIVE_OUTPUT_FILE = 11
    CONTENT = 12
    OUTPUT_DEFAULTS = 14
    GROUP = 15
    CHANGE_GROUP = 16


class HeaderFileReader(XMLFileReader):
    def __init__(self):
        XMLFileReader.__init__(self)
        self.__reset()
        # Pointer to plugin this header file belongs to.
        self.plugin = None
        self.parent_element = None
        self.activeGroup = None
        self.xml_element = None

    def __reset(self):
        self.enclosing_tag = None
        self.headerStructure = HeaderStructure()
        # ID of current XML element
        self.xml_element = ElementEnum.NO_ELEMENT
        self.activeGroup = None
        # ID of parent element
        self.parent_element = ElementEnum.NO_ELEMENT

    def startElement(self, name, attrs):
        log.debug("Start element: " + name)
        if not self.enclosing_tag and name == "freeconf-header":
            log.debug("freeconf-header tag.")
            self.enclosing_tag = True
            return

        if not self.enclosing_tag:
            log.error("You must enclose the Header File with <freeconf-header> and </freeconf-header>.")
            return

        if name == "content":
            self.parent_element = self.xml_element = ElementEnum.CONTENT

        elif name == "entry-group":  # Definition of new group
            self.parent_element = self.xml_element = ElementEnum.GROUP
            # Get name attribute
            try:
                group_name = attrs['name']
            except KeyError:
                log.debug("Missing entry group name, setting to 'default'.")
                group_name = "default"
            # Check if group does not already exist
            if group_name in self.headerStructure.groups or (self.plugin and group_name in self.plugin.availableGroups):
                raise ParseError("Entry group %s is already defined!" % (group_name,))
            # Create new group
            self.activeGroup = FcGroup(group_name)

        elif name == "change-group":  # Redefinition of existing group
            if self.plugin is None:
                raise ParseError("Element <" + name + "> can be defined only in plugin header file!")
            self.parent_element = self.xml_element = ElementEnum.CHANGE_GROUP
            # Get name attribute
            try:
                group_name = attrs['name']
            except KeyError:
                log.debug("Missing entry group name, setting to 'default'.")
                group_name = "default"
            # Get the group to change
            try:
                self.activeGroup = self.plugin.availableGroups[group_name]
            except KeyError:
                raise ParseError("Group %dsn does not exist!" % (group_name,))

        elif name == "template":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.TEMPLATE_FILE
        elif name == "gui-template":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.GUI_TEMPLATE_FILE
        elif name == "dependencies":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.DEPENDENCY_FILE
        elif name == "help":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.HELP_FILE
        elif name == "gui-label":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.GUI_LABEL_FILE
        elif name == "lists":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.LISTS_FILE
        elif name == "default-values":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.DEFAULT_VALUES_FILE
        elif name == "output":
            if self.parent_element != ElementEnum.CONTENT:
                raise ParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.OUTPUT_FILE

        # Elements in entry group
        # TODO: Rozlisit entry-group a change-group
        elif name == "native-output":
            if self.parent_element != ElementEnum.GROUP:
                raise ParseError("Element <" + name + "> must be inside of <entry-group> element!")
            self.xml_element = ElementEnum.NATIVE_OUTPUT_FILE
        elif name == "transform":
            if self.parent_element != ElementEnum.GROUP:
                raise ParseError("Element <" + name + "> must be inside of <entry-group> element!")
            self.xml_element = ElementEnum.TRANSFORM_FILE
        elif name == "add-transform":
            if self.parent_element != ElementEnum.CHANGE_GROUP:
                raise ParseError("Element <" + name + "> must be inside of <change-group> element!")
            self.xml_element = ElementEnum.ADD_TRANSFORM_FILE
        elif name == "output-defaults":
            if self.parent_element != ElementEnum.GROUP:
                raise ParseError("Element <" + name + "> must be inside of <entry-group> element!")
            self.xml_element = ElementEnum.OUTPUT_DEFAULTS

        else:
            log.error("Unknown header element: " + name)
            self.xml_element = ElementEnum.NO_ELEMENT

    def endElement(self, name):
        log.debug("End element: " + name)
        if name == "entry-group":
            self.headerStructure.add_group(self.activeGroup)
            self.activeGroup = None
            self.parent_element = ElementEnum.NO_ELEMENT
        elif name == "change-group":
            self.activeGroup = None
            self.parent_element = ElementEnum.NO_ELEMENT
        elif name == "content":
            self.parent_element = ElementEnum.NO_ELEMENT
        self.xml_element = ElementEnum.NO_ELEMENT

    def characters(self, data):
        data = data.strip()
        if data == '':
            return  # Ignore white space in XML

        if self.xml_element == ElementEnum.TEMPLATE_FILE:
            self.headerStructure.templateFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.GUI_TEMPLATE_FILE:
            self.headerStructure.guiTemplateFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.DEPENDENCY_FILE:
            self.headerStructure.dependenciesFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.LISTS_FILE:
            self.headerStructure.listFiles.append(data)
        elif self.xml_element == ElementEnum.HELP_FILE:
            self.headerStructure.helpFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.GUI_LABEL_FILE:
            self.headerStructure.guiLabelFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.DEFAULT_VALUES_FILE:
            self.headerStructure.defaultValuesFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.OUTPUT_FILE:
            self.headerStructure.outputFile = FcFileLocation(data)
        # Group entries
        elif self.xml_element == ElementEnum.TRANSFORM_FILE:
            self.activeGroup.transform = FcFileLocation(data)
        elif self.xml_element == ElementEnum.ADD_TRANSFORM_FILE:
            file_location = FcIncludeFileLocation(self.plugin, data)
            self.activeGroup.include_transform(file_location)
        elif self.xml_element == ElementEnum.NATIVE_OUTPUT_FILE:
            self.activeGroup.native_output = FcFileLocation(data)
        elif self.xml_element == ElementEnum.OUTPUT_DEFAULTS:
            if data == "yes":
                self.activeGroup.outputDefaults = True
            elif data == "no":
                self.activeGroup.outputDefaults = False
            else:
                log.error("wrong value of element <output-defaults>, must be either yes or no.")

    def parse(self, f, plugin=None):
        self.__reset()
        self.plugin = plugin
        XMLFileReader.parse(self, f)
