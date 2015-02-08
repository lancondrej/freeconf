#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

from src.Model.exception_logging.log import log
from src.Model.PackageParser.sax_file import XMLFileReader
from src.Model.exception_logging.exception import FcParseError


class ConfigEnum:
    """Constants for XML elements"""
    NO_ELEMENT = 0
    VALUE = 1
    HELP = 2

class ConfigFileReader (XMLFileReader):
    """Config file SAX handler"""
    def __init__ (self):
        XMLFileReader.__init__(self)
        self.sectionStack = []
        self.state = ConfigEnum.NO_ELEMENT
        self.currentElement = None
        self.helpBuffer = ""


    def startElementSection(self, attrs):
        section = self.sectionStack[-1]
        try:
            name = attrs['name']
            if section.name == name and len(self.sectionStack) <= 1:
                self.currentElement = section
            else:
                entry = section.findCEntry(name)
                if entry == None:
                    # There is no config entry yet, try to find it in template tree
                    tentry = section.templateBuddy.findTEntry(name)
                else:
                    tentry = entry.templateBuddy

                if tentry == None:
                    log.error("No section with name " + name + " in template file.")
                    raise FcParseError("No section with name " + name + " in template file.")
                if not tentry.isSection():
                    log.error("Entry " + name + " is not a section.")
                    raise FcParseError("Entry " + name + " is not a section.")

                if entry == None:
                    self.currentElement = tentry.createCEntry(section)
                else:
                    self.currentElement = entry

            if self.currentElement.isMultipleEntryContainer():
                self.sectionStack.append(self.currentElement)
                # Insert section into multiple entry container
                self.currentElement = self.currentElement.templateBuddy.createCEntry(self.currentElement)
                # TODO: Pozor na vraceni sekci do stacku,tady by mohl byt problem!

            self.sectionStack.append(self.currentElement)
        except KeyError:
            log.error("Attribute name was not found!")


    def startElementEntry(self, attrs):
        section = self.sectionStack[-1]
        try:
            name = attrs['name']
            log.debug(name)
            tentry = section.templateBuddy.findTEntry(name)
            if tentry == None:
                log.error("No entry with name " + name + " in template file section " + section.name)
                raise FcParseError("No entry with name " + name + " in template file section " + section.name)
            self.currentElement = tentry.createCEntry(section)
        except KeyError:
            log.error("Attribute name was not found!")


    def startElement(self, name, attrs):
        log.debug("Start element: " + name)

        if name == "section":
            self.startElementSection(attrs)
        elif name == "entry":
            self.startElementEntry(attrs)
        else:
            assert self.currentElement != None
            if name == "value":
                self.state = ConfigEnum.VALUE
            elif name == "help":
                self.state = ConfigEnum.HELP
                self.helpBuffer = ""
            else:
                log.error("Unknown entry type: " + name)
                raise FcParseError("Unknown entry type: " + name)


    def characters(self, data):
        if data.isspace():
            return # Ignore white space in XML

        if self.state == ConfigEnum.VALUE:
            assert self.currentElement != None
            log.debug("Setting value for entry " + self.currentElement.name + " to " + data + ".")
            type = self.currentElement.templateBuddy.type
            value = data.strip()
            if type in (FcTypes.STRING, FcTypes.FUZZY, FcTypes.BOOL):
                # TODO: nebude potreba u BOOL a FUZZY kontrolovat jestli je hodnota v seznamu?
                self.currentElement.value = value
            elif type == FcTypes.NUMBER:
                self.currentElement.value = float(value)
            else:
                log.error("Unknown entry type " + str(type) + " for " + self.currentElement.name + "!")

        elif self.state == ConfigEnum.HELP:
            pass

    def endElement(self, name):
        log.debug("End element: " + name)

        if name == "entry":
            self.currentElement = None
        elif name == "section":
            self.currentElement = None
            self.sectionStack.pop()
            if len(self.sectionStack) > 0 and self.sectionStack[-1].isMultipleEntryContainer():
                self.sectionStack.pop()
        elif name == "value":
            self.state = ConfigEnum.NO_ELEMENT
        elif name == "help":
            self.state = ConfigEnum.NO_ELEMENT
        else:
            log.error("Unknown entry type: " + name)
        return


    def parse(self, file, configTree):
        self.sectionStack = [configTree]
        self.currentElement = None
        # Parse the XML file
        XMLFileReader.parse(self, file)


class ConfigFileWriter(FcVisitor):
    # TODO
    def write():
        pass

