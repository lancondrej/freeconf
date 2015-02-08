#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

import logging

from src.Model.PackageParser.sax_file import XMLFileReader
from src.Model.exception_logging.exception import FcParseError


class HeaderStructure:
    """This structure contains file names for template file, help files, files with default values etc. which should be parsed to get all necesary information."""

    def __init__(self):
        ## Initialize properties
        # Package name is necesary for constructing file name paths
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

    def addGroup(self, group):
        self.groups[group.name] = group

    def initDefaults(self, name):
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
        default_group.transformFile = FcFileLocation(name + "_transform.xml")
        default_group.nativeFile = FcFileLocation("${PACKAGE}/" + name + ".conf")
        default_group.outputDefaults = True
        self.addGroup(default_group)

    def __repr__(self):
        return "class(HeaderStructure):" + "\n" + \
               "  Package name: " + str(self.packageName) + "\n" + \
               "  Template file: " + str(self.templateFile) + "\n" + \
               "  GUI Template file: " + str(self.guiTemplateFile) + "\n" + \
               "  Dependecy file: " + str(self.dependenciesFile) + "\n" + \
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

    def __reset(self):
        self.enclosing_tag = None
        self.headerStructure = HeaderStructure()
        # ID of current XML element
        self.xml_element = ElementEnum.NO_ELEMENT
        self.activeGroup = None
        # ID of parent element
        self.parent_element = ElementEnum.NO_ELEMENT

    def startElement(self, name, attrs):
        logging.debug("Start element: " + name)
        if not self.enclosing_tag and name == "freeconf-header":
            logging.debug("freeconf-header tag.")
            self.enclosing_tag = True
            return

        if not self.enclosing_tag:
            logging.error("You must enclose the Header File with <freeconf-header> and </freeconf-header>.")
            return

        if name == "content":
            self.parent_element = self.xml_element = ElementEnum.CONTENT

        elif name == "entry-group":  # Definition of new group
            self.parent_element = self.xml_element = ElementEnum.GROUP
            # Get name attribute
            group_name = None
            try:
                group_name = attrs['name']
            except(KeyError):
                logging.debug("Missing entry group name, setting to 'default'.")
                group_name = "default"
            # Check if group does not already exist
            if group_name in self.headerStructure.groups or (self.plugin and group_name in self.plugin.availableGroups):
                raise FcParseError("Entry group %s is already defined!" % (group_name,))
            # Create new group
            self.activeGroup = FcGroup(group_name)

        elif name == "change-group":  # Redefinition of existing group
            if self.plugin == None:
                raise FcParseError("Element <" + name + "> can be defined only in plugin header file!")
            self.parent_element = self.xml_element = ElementEnum.CHANGE_GROUP
            # Get name attribute
            group_name = None
            try:
                group_name = attrs['name']
            except(KeyError):
                logging.debug("Missing entry group name, setting to 'default'.")
                group_name = "default"
            # Get the group to change
            try:
                self.activeGroup = self.plugin.availableGroups[group_name]
            except(KeyError):
                raise FcParseError("Group %n does not exist!" % (group_name,))

        elif name == "template":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.TEMPLATE_FILE
        elif name == "gui-template":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.GUI_TEMPLATE_FILE
        elif name == "dependencies":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.DEPENDENCY_FILE
        elif name == "help":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.HELP_FILE
        elif name == "gui-label":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.GUI_LABEL_FILE
        elif name == "lists":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.LISTS_FILE
        elif name == "default-values":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.DEFAULT_VALUES_FILE
        elif name == "output":
            if self.parent_element != ElementEnum.CONTENT:
                raise FcParseError("Element <" + name + "> must be inside of <content> element!")
            self.xml_element = ElementEnum.OUTPUT_FILE

        # Elements in entry group
        # TODO: Rozlisit entry-group a change-group
        elif name == "native-output":
            if self.parent_element != ElementEnum.GROUP:
                raise FcParseError("Element <" + name + "> must be inside of <entry-group> element!")
            self.xml_element = ElementEnum.NATIVE_OUTPUT_FILE
        elif name == "transform":
            if self.parent_element != ElementEnum.GROUP:
                raise FcParseError("Element <" + name + "> must be inside of <entry-group> element!")
            self.xml_element = ElementEnum.TRANSFORM_FILE
        elif name == "add-transform":
            if self.parent_element != ElementEnum.CHANGE_GROUP:
                raise FcParseError("Element <" + name + "> must be inside of <change-group> element!")
            self.xml_element = ElementEnum.ADD_TRANSFORM_FILE
        elif name == "output-defaults":
            if self.parent_element != ElementEnum.GROUP:
                raise FcParseError("Element <" + name + "> must be inside of <entry-group> element!")
            self.xml_element = ElementEnum.OUTPUT_DEFAULTS

        else:
            logging.error("Unknown header element: " + name)
            self.xml_element = ElementEnum.NO_ELEMENT

    def endElement(self, name):
        logging.debug("End element: " + name)
        if name == "entry-group":
            self.headerStructure.addGroup(self.activeGroup)
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
            self.activeGroup.transformFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.ADD_TRANSFORM_FILE:
            fileloc = FcIncludeFileLocation(self.plugin, data)
            self.activeGroup.includeTransform(fileloc)
        elif self.xml_element == ElementEnum.NATIVE_OUTPUT_FILE:
            self.activeGroup.nativeFile = FcFileLocation(data)
        elif self.xml_element == ElementEnum.OUTPUT_DEFAULTS:
            if data == "yes":
                self.activeGroup.outputDefaults = True
            elif data == "no":
                self.activeGroup.outputDefaults = False
            else:
                logging.error("wrong value of element <output-defaults>, must be either yes or no.")


    def parse(self, f, plugin=None):
        self.__reset()
        self.plugin = plugin
        XMLFileReader.parse(self, f)


class HeaderFileWriter:
    def __init__(self, header_structure):
        assert isinstance(header_structure, HeaderStructure)
        self.headerStructure = header_structure

    def generate(self):
        """Return string with header file's content."""

        def gen_xml_elt(name, value, indent=""):
            """Help function. Generate XML code for element name with given value. If value is empty, result will be empty string."""
            if value == "" or value == None:
                return ""
            return "%s<%s>%s</%s>\n" % (indent, name, value, name)

        s = '<?xml version="1.0" encoding="UTF-8"?>\n'
        s += '<freeconf-header>\n'  # Resulting string
        ## Write main content
        s += "<content>\n"
        s += gen_xml_elt("template", self.headerStructure.templateFile.name, "  ")
        s += gen_xml_elt("default-values", self.headerStructure.defaultValuesFile.name, "  ")
        s += gen_xml_elt("help", self.headerStructure.helpFile.name, "  ")
        s += gen_xml_elt("output", self.headerStructure.outputFile.name, "  ")
        s += gen_xml_elt("dependencies", self.headerStructure.dependenciesFile.name, "  ")
        s += gen_xml_elt("gui-template", self.headerStructure.guiTemplateFile.name, "  ")
        s += gen_xml_elt("gui-label", self.headerStructure.guiLabelFile.name, "  ")
        for l in self.headerStructure.listFiles:
            s += gen_xml_elt("lists", l, "  ")
        s += "</content>\n"
        ## Write groups
        # TODO: Podpora pluginu, podpora change-group
        for g in self.headerStructure.groups.values():
            s += '<entry-group name="%s">\n' % (g.name,)
            s += gen_xml_elt("transform", g.transformFile.name, "  ")
            s += gen_xml_elt("native-output", g.nativeFile.name, "  ")
            if g.outputDefaults:
                s += gen_xml_elt("output-defaults", "yes", "  ")
            else:
                s += gen_xml_elt("output-defaults", "no", "  ")
            s += '</entry-group>\n'

        s += "</freeconf-header>\n"
        return s

    def write(self, filename):
        """Write header file to given file."""
        f = open(filename, 'w')
        f.write(self.generate())

