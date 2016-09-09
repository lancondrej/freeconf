#!/usr/bin/python3
#
from src.IO.XMLPackageParser.sax_file import XMLFileReader
from src.IO.exception_logging.log import log
from src.Model.constants import Types

__author__ = 'Ondřej Lanč'


class ElementEnum:
    """Constants for list elements"""
    NO_ELEMENT = 0
    STRING_LIST = 1
    FUZZY_LIST = 2
    ENTRY = 3
    VALUE = 4
    HELP = 5
    LABEL = 6


class ListHelpFile(XMLFileReader):
    def __init__(self):
        XMLFileReader.__init__(self)
        self.__reset()

    def __reset(self):
        """Reset state of object."""
        # List of value lists
        self.lists = None
        # Current string list (list of StringEntry instances)
        self.current_list = None

        # Actual data for current string
        self.current_value = None
        self.current_label = None
        self.current_help = None

        # Current List Entry
        self.current_entry = None
        # ID of current XML element
        self.xml_element = ElementEnum.NO_ELEMENT

    def startElement(self, name, attrs):
        log.debug("Start element: " + name)
        if not self.enclosing_tag and name == "freeconf-lists-help":
            log.debug("freeconf-lists-help tag.")
            self.enclosing_tag = True
            return

        if not self.enclosing_tag:
            log.error("You must enclose the List Help File with <freeconf-lists-help> and </freeconf-lists-help>.")
            return

        if name == "string-list":
            try:
                attr_name = attrs['name']
            except(KeyError):
                log.error("Attribute name is missing for <string-list>!")
                return

            try:
                self.current_list = self.lists[attr_name]
            except(KeyError):
                log.error("Failed to find string list " + attr_name + "!")
                return
            if self.current_list.type != Types.STRING:
                log.error("Expected string list '%s' in list help file!" % (attr_name,))
                self.current_list = None
            self.xml_element = ElementEnum.STRING_LIST

        elif name == "fuzzy-list":
            try:
                attr_name = attrs['name']
            except(KeyError):
                log.error("Attribute name is missing for <fuzzy-list>!")
                return

            try:
                self.current_list = self.lists[attr_name]
            except(KeyError):
                log.error("Failed to find fuzzy list " + attr_name + "!")
                return
            if self.current_list.type != Types.FUZZY:
                log.error("Expected fuzzy list '%s' in list help file!" % (attr_name,))
                self.current_list = None
            self.xml_element = ElementEnum.FUZZY_LIST

        elif name == "entry":
            self.xml_element = ElementEnum.ENTRY
        elif name == "value":
            self.xml_element = ElementEnum.VALUE
        elif name == "help":
            self.xml_element = ElementEnum.HELP
        elif name == "label":
            self.xml_element = ElementEnum.LABEL
        else:
            log.error("Unknown entry type: " + name)

    def endElement(self, name):
        log.debug("End element: " + name)

        if name in ("string-list", "fuzzy-list"):
            assert self.current_list != None
            self.current_list = None

        elif name == "entry":
            # Find current entry
            for e in self.current_list.entries:
                if e.value == self.current_value:
                    self.current_entry = e
                    break
            else:
                log.error("Failed to find value " + self.current_value + " in list " + self.current_list.name + "!")
                return

            self.current_entry.label = self.current_label
            self.current_entry.help = self.current_help

            assert self.current_entry != None
            self.current_entry = None

        self.xml_element = ElementEnum.NO_ELEMENT

    def characters(self, data):
        if self.xml_element == ElementEnum.VALUE:
            self.current_value = data
        elif self.xml_element == ElementEnum.LABEL:
            self.current_label = data
        elif self.xml_element == ElementEnum.HELP:
            self.current_help = data

    def parse(self, file, lists):
        """Parse given list help file."""
        assert type(lists) == dict
        self.__reset()
        self.lists = lists
        XMLFileReader.parse(self, file)
