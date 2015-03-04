#!/usr/bin/python
#
# help_file.py
# begin: 22.8.2010 by Jan Ehrenberger
#
# PyFC: Help File SAX Handler
#

# Freeconf libs
from log import log
from base import *
# Other libs
from src.PackageParser.sax_file import XMLFileReader
from exception import FcParseError


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
		# Section stack
		self.sectionStack = []
		self.ignoreEntry = 0 # Counter of ingonred section depth
		# ID of current XML element
		self.xml_element = HelpEnum.NO_ELEMENT
		self.language = None
		self.helpBuffer = ""

	def startElementSection(self, attrs):
		section = self.sectionStack[-1]
		try:
			name = attrs['name']
			if section.name == name:
				self.currentElement = section
			else:
				self.currentElement = section.findTEntry(name)
				if self.currentElement == None:
					log.error("No section with name " + name + " in template file.")
					self.ignoreEntry += 1
					return
				if not self.currentElement.isSection():
					log.error("Entry " + name + " is not a section.")
					self.ignoreEntry += 1
					return
			self.sectionStack.append(self.currentElement)
		except KeyError:
			log.error("Attribute name was not found!")

	def startElementEntry(self, attrs):
		section = self.sectionStack[-1]
		try:
			name = attrs['name']
			log.debug(name)
			self.currentElement = section.findTEntry(name)
			if self.currentElement == None:
				log.error("No entry with name " + name + " in template file section " + section.name)
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

		if name == "section":
			if self.ignoreEntry > 0:
				log.warning("Ignoring section help in ignored section.")
				self.ignoreEntry += 1
			else:
				self.startElementSection(attrs)
			return

		if self.ignoreEntry > 0:
			#log.warning("Ignoring entry help in ignored section.")
			return

		if name == "entry":
			self.startElementEntry(attrs)
		else:
			assert self.currentElement != None
			if name == "label":
				self.xml_element = HelpEnum.LABEL
			elif name == "help":
				self.xml_element = HelpEnum.HELP
				self.helpBuffer = ""
			else:
				log.error("Unknown entry type: " + name)

	def endElement(self, name):
		log.debug("End element: " + name)

		if name == "section":
			if self.ignoreEntry > 0:
				self.ignoreEntry -= 1
			self.currentElement = None
			self.sectionStack.pop()
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
			self.currentElement.setKeyHelp(self.language, self.helpBuffer);
			self.xml_element = HelpEnum.NO_ELEMENT
		elif name != "freeconf-help":
			log.error("Unknown entry type: " + name)
		return

	def characters(self, data):
		if data.isspace() or self.ignoreEntry > 0:
			return # Ignore white space in XML and ingored entries

		if self.xml_element == HelpEnum.LABEL:
			assert self.currentElement != None
			log.debug("Setting label for entry " + self.currentElement.name + " to " + data + ".")
			self.currentElement.setKeyLabel(self.language, data)
		elif self.xml_element == HelpEnum.HELP:
			assert self.currentElement != None
			log.debug("Setting help for entry " + self.currentElement.name + " to " + data + ".")
			self.helpBuffer += data

	def parse(self, file, top_section, language):
		self.enclosing_tag = False
		self.currentElement = None
		self.sectionStack = [top_section]
		self.language = language
		self.xml_element = HelpEnum.NO_ELEMENT
		# Parse the XML file
		XMLFileReader.parse(self, file)


