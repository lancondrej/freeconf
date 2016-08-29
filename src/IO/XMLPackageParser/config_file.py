#!/usr/bin/python3
#
from copy import deepcopy

from IO.exception_logging.log import log

from IO.XMLPackageParser.sax_file import XMLFileReader
from IO.exception_logging.exception import ParseError
from Model.constants import Types

# from lxml.etree import Element, ElementTree
from xml.etree.ElementTree import Element, ElementTree

__author__ = 'Ondřej Lanč'


class ConfigEnum:
    """Constants for XML elements"""
    NO_ELEMENT = 0
    VALUE = 1
    HELP = 2


class ConfigFileReader (XMLFileReader):
    """Config file SAX handler"""
    def __init__(self):
        XMLFileReader.__init__(self)
        self.container_stack = []
        self.state = ConfigEnum.NO_ELEMENT
        self.currentElement = None
        self.helpBuffer = ""

    def start_element_container(self, attrs):
        container = self.container_stack[-1]
        try:
            name = attrs['name']
            if container.name == name and len(self.container_stack) <= 1:
                self.currentElement = container
            else:
                entry = container.get_entry(name)
                if entry is None:
                    log.error("No container with name " + name + " in template file.")
                    raise ParseError("No container with name " + name + " in template file.")
                if not entry.is_container():
                    log.error("Entry " + name + " is not a container.")
                    raise ParseError("Entry " + name + " is not a container.")
                if entry.is_multiple_entry_container():
                    entry = entry.append()
                self.currentElement = entry
            self.container_stack.append(self.currentElement)
        except KeyError:
            log.error("Attribute name was not found!")

    def startElementEntry(self, attrs):
        container = self.container_stack[-1]
        try:
            name = attrs['name']
            log.debug(name)
            entry = container.get_entry(name)
            if entry is None:
                log.error("No entry with name " + name + " in template file container " + container.name)
                raise ParseError("No entry with name " + name + " in template file container " + container.name)
            if entry.is_multiple_entry_container():
                entry = entry.append(deepcopy(entry.template))
            self.currentElement = entry
        except KeyError:
            log.error("Attribute name was not found!")

    def startElement(self, name, attrs):
        log.debug("Start element: " + name)

        if name == "container":
            self.start_element_container(attrs)
        elif name == "entry":
            self.startElementEntry(attrs)
        else:
            assert self.currentElement is not None
            if name == "value":
                self.state = ConfigEnum.VALUE
            elif name == "help":
                self.state = ConfigEnum.HELP
                self.helpBuffer = ""
            else:
                log.error("Unknown entry type: " + name)
                raise ParseError("Unknown entry type: " + name)

    def characters(self, data):
        if data.isspace():
            return # Ignore white space in XML

        if self.state == ConfigEnum.VALUE:
            assert self.currentElement is not None
            log.debug("Setting value for entry " + self.currentElement.name + " to " + data + ".")
            type = self.currentElement.type
            value = data.strip()
            if type in (Types.STRING, Types.FUZZY, Types.BOOL):
                # TODO: nebude potreba u BOOL a FUZZY kontrolovat jestli je hodnota v seznamu?
                self.currentElement.value = value
            elif type == Types.NUMBER:
                self.currentElement.value = float(value)
            else:
                log.error("Unknown entry type " + str(type) + " for " + self.currentElement.name + "!")

        elif self.state == ConfigEnum.HELP:
            pass

    def endElement(self, name):
        log.debug("End element: " + name)

        if name == "entry":
            self.currentElement = None
        elif name == "container":
            self.currentElement = None
            self.container_stack.pop()
            if len(self.container_stack) > 0 and self.container_stack[-1].is_multiple_entry_container():
                self.container_stack.pop()
        elif name == "value":
            self.state = ConfigEnum.NO_ELEMENT
        elif name == "help":
            self.state = ConfigEnum.NO_ELEMENT
        else:
            log.error("Unknown entry type: " + name)
        return

    def parse(self, file, tree):
        self.container_stack = [tree]
        self.currentElement = None
        # Parse the XML file
        XMLFileReader.parse(self, file)

class ConfigFileWriter (object):
    def __init__(self, file, root):
        self.render = {
            'Container': self.render_container,
            'Fuzzy': self.render_key_word,
            'Bool': self.render_key_word,
            'Number': self.render_key_word,
            'String': self.render_key_word,
            'MultipleContainer': self.render_multiple,
            'MultipleKeyWord': self.render_multiple,
        }
        self._file = file
        self._root = root

    def write_config(self):
        root = self.render_entry(self._root)[0]
        config_tree = ElementTree(root)
        config_tree.write("output.xml", encoding="UTF-8", xml_declaration=True)

    def render_entry(self, entry):
        try:
            return self.render[type(entry).__name__](entry)
        except:
            pass

    def render_container(self, container):
        element = Element('container')
        element.set('name', container.name)
        for entry in container.entries.values():
            sub=self.render_entry(entry)
            element.extend(self.render_entry(entry))
        return [element]

    def render_key_word(self, entry):
        element = Element('entry')
        element.set('name', entry.name)
        element.set('group', entry.group.name)
        value=Element('value')
        value.text = str(entry.value)
        element.append(value)
        return [element]

    def render_multiple(self, mult):
        return [self.render_entry(entry)[0] for entry in mult.entries]