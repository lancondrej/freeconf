#!/usr/bin/python3
#
from IO.Input.XMLPackageParser.sax_file import XMLFileReader
from IO.Input.exception_logging.log import log


__author__ = 'Ondřej Lanč'


class HelpEnum:
    """Constants for XML elements"""
    NO_ELEMENT = 0
    LABEL = 1
    HELP = 2


class HelpFile(XMLFileReader):
    def __init__(self):
        XMLFileReader.__init__(self)
        # Current entry
        self.currentElement = None
        # container stack
        self.container_stack = []
        self.ignoreEntry = 0  # Counter of ingonred container depth
        # ID of current XML element
        self.xml_element = HelpEnum.NO_ELEMENT
        self.language = None
        self.helpBuffer = ""

    def start_element_container(self, attrs):
        container = self.container_stack[-1]
        try:
            name = attrs['name']
            if container.name == name:
                self.currentElement = container
            else:
                self.currentElement = container.get_entry(name)
                if self.currentElement is None:
                    log.error("No container with name " + name + " in template file.")
                    self.ignoreEntry += 1
                    return
                if not self.currentElement.is_container():
                    log.error("Entry " + name + " is not a container.")
                    self.ignoreEntry += 1
                    return
            self.container_stack.append(self.currentElement)
        except KeyError:
            log.error("Attribute name was not found!")

    def startElementEntry(self, attrs):
        container = self.container_stack[-1]
        try:
            name = attrs['name']
            log.debug(name)
            self.currentElement = container.get_entry(name)
            if self.currentElement is None:
                log.error("No entry with name " + name + " in template file container " + container.name)
                self.ignoreEntry += 1
                return
        except KeyError:
            log.error("Attribute name was not found!")

    def startElement(self, name, attrs):
        log.debug("Start element: " + name)
        if not self.enclosing_tag and name == "freeconf-help":
            log.debug("freeconf-help tag.")
            self.enclosing_tag = True
            return

        if not self.enclosing_tag:
            # TODO: vyhodit nejakou vyjimku
            log.error("You must enclose the Help File with <freeconf-help> and </freeconf-help>.")
            return

        if name == "container":
            if self.ignoreEntry > 0:
                log.warning("Ignoring container help in ignored container.")
                self.ignoreEntry += 1
            else:
                self.start_element_container(attrs)
            return

        if self.ignoreEntry > 0:
            # log.warning("Ignoring entry help in ignored container.")
            return

        if name == "entry":
            self.startElementEntry(attrs)
        else:
            assert self.currentElement is not None
            if name == "label":
                self.xml_element = HelpEnum.LABEL
            elif name == "help":
                self.xml_element = HelpEnum.HELP
                self.helpBuffer = ""
            else:
                log.error("Unknown entry type: " + name)

    def endElement(self, name):
        log.debug("End element: " + name)

        if name == "container":
            if self.ignoreEntry > 0:
                self.ignoreEntry -= 1
            self.currentElement = None
            self.container_stack.pop()
            return

        if name == "entry":
            if self.ignoreEntry > 0:
                self.ignoreEntry -= 1
            self.currentElement = None
            return

        if self.ignoreEntry > 0:
            return

        elif name == "label":
            self.xml_element = HelpEnum.NO_ELEMENT
        elif name == "help":
            self.currentElement.set_key_help(self.language, self.helpBuffer)
            self.xml_element = HelpEnum.NO_ELEMENT
        elif name != "freeconf-help":
            log.error("Unknown entry type: " + name)
        return

    def characters(self, data):
        if data.isspace() or self.ignoreEntry > 0:
            return  # Ignore white space in XML and ingored entries

        if self.xml_element == HelpEnum.LABEL:
            assert self.currentElement is not None
            log.debug("Setting label for entry " + self.currentElement.name + " to " + data + ".")
            self.currentElement.set_label(self.language, data)
        elif self.xml_element == HelpEnum.HELP:
            assert self.currentElement is not None
            log.debug("Setting help for entry " + self.currentElement.name + " to " + data + ".")
            self.helpBuffer += data

    def parse(self, file, top_container, language):
        self.enclosing_tag = False
        self.currentElement = None
        self.container_stack = [top_container]
        self.language = language
        self.xml_element = HelpEnum.NO_ELEMENT
        # Parse the XML file
        XMLFileReader.parse(self, file)


