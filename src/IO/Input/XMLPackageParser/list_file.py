#!/usr/bin/python3
#
from src.IO.Input.XMLPackageParser.sax_file import XMLFileReader
from src.Model.lists import StringList, FuzzyList
from src.IO.Input.exception_logging.log import log
from src.Model.constants import Types


__author__ = 'Ondřej Lanč'


class ElementEnum:
    """Constants for string list elements"""
    NO_ELEMENT = 0
    STRING_LIST = 1
    FUZZY_LIST = 2
    VALUE = 3


class ListFile(XMLFileReader):
    def __init__(self):
        XMLFileReader.__init__(self)
        # List of lists
        self.lists = {}
        # Current list
        self.current_list = None
        # Current Entry
        self.current_entry = None
        # ID of current XML element
        self.xml_element = ElementEnum.NO_ELEMENT

    def startElement(self, name, attrs):
        log.debug("Start element: " + name)
        if not self.enclosing_tag and name == "freeconf-lists":
            log.debug("freeconf-lists tag.")
            self.enclosing_tag = True
            return

        if not self.enclosing_tag:
            log.error("You must enclose the List File with <freeconf-lists> and </freeconf-lists>.")
            return

        if name == "string-list":
            try:
                self.current_list = StringList(attrs['name'])
                self.lists[self.current_list.name] = self.current_list
            except KeyError:
                log.error("Attribute 'name' is missing for <string-list>!")
                return
            self.xml_element = ElementEnum.STRING_LIST

        elif name == "fuzzy-list":
            try:
                self.current_list = FuzzyList(attrs['name'])
                self.lists[self.current_list.name] = self.current_list
            except KeyError:
                log.error("Attribute 'name' is missing for <fuzzy-list>!")
                return
            self.xml_element = ElementEnum.FUZZY_LIST

        elif name == "value":
            if self.current_list.type == Types.STRING:
                self.current_entry = StringList.Entry()
            elif self.current_list.type == Types.FUZZY:
                grade = None
                try:
                    grade = float(attrs['grade'])
                except KeyError:
                    log.error("Attribute 'grade' is missing for fuzzy value!")
                    return
                if grade < 0 or grade > 1:
                    log.error("Attribute grade=%f is out of range for fuzzy value!", grade)
                    return
                self.current_entry = FuzzyList.Entry(grade)
            self.xml_element = ElementEnum.VALUE
        else:
            log.error("Unknown entry type: " + name)

    def endElement(self, name):
        log.debug("End element: " + name)
        if self.xml_element in (ElementEnum.STRING_LIST, ElementEnum.FUZZY_LIST):
            assert self.current_list is not None
            self.current_list = None
        elif self.xml_element == ElementEnum.VALUE:
            assert self.current_list is not None
            self.current_list.append(self.current_entry)
            self.current_entry = None
        self.xml_element = ElementEnum.NO_ELEMENT

    def characters(self, data):
        if self.xml_element == ElementEnum.VALUE:
            self.current_entry.value = data

    def parse(self, file, lists={}):
        assert type(lists) == dict
        self.lists = lists
        self.current_list = None
        self.enclosing_tag = None
        XMLFileReader.parse(self, file)
