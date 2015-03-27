#!/usr/bin/python
#
# configFile.py
# begin: 23.11.2010 by David Fabian
#
# PyFC: Config File SAX Handler
#

from log import log
from base import *
from sax_file import XMLFileReader
from exception import FcParseError

#class ConfigEnum:
	#"""Constants for config elements"""
	#NOELEMENT = 0
	#ELEMENTOPENED = 1
	##self.firstWrite = False


class DefaultFile (XMLFileReader):
	"""Config file SAX handler"""
	def __init__ (self):
		XMLFileReader.__init__(self)
		self.sectionStack = []
		#self.state = ConfigEnum.NOELEMENT
		self.currentElement = None


	def startElementSection(self, attrs):
		section = self.sectionStack[-1]
		try:
			name = attrs['name']
			if section.name == name:
				self.currentElement = section
			else:
				tentry = section.findTEntry(name)
				if tentry == None:
					log.error("No section with name " + name + " in template file.")
					raise FcParseError("No section with name " + name + " in template file.")
				if not tentry.isSection():
					log.error("Entry " + name + " is not a section.")
					raise FcParseError("Entry " + name + " is not a section.")
				self.currentElement = tentry
			self.sectionStack.append(self.currentElement)
		except KeyError:
			log.error("Attribute name was not found!")


	def startElementEntry(self, attrs):
		section = self.sectionStack[-1]
		try:
			name = attrs['name']
			log.debug(name)
			tentry = section.findTEntry(name)
			if tentry == None:
				log.error("No entry with name " + name + " in template file section " + section.name)
				raise FcParseError("No entry with name " + name + " in template file section " + section.name)
				return
			self.currentElement = tentry
			# empty tag is skipped during parsing, characters() is not called, and thus the default value is not set
			# this ensures that even the empty strings would be treated as consistent
			if self.currentElement.type == FcTypes.STRING:
				self.currentElement.defaultValue = ""

		except KeyError:
			log.error("Attribute name was not found!")


	def startElement(self, name, attrs):
		log.debug("Start element: " + name)

		if name == "section":
			self.startElementSection(attrs)
		elif name == "entry":
			self.startElementEntry(attrs)
		else:
			log.error("Unknown entry type: " + name)
			raise FcParseError("Unknown entry type: " + name)
			

	def characters(self, data):
		if data.isspace():
			return # Ignore white space in XML

		type = self.currentElement.type
		value = data.strip()
		if type in (FcTypes.STRING, FcTypes.FUZZY, FcTypes.BOOL):
			# TODO: nebude potreba u BOOL a FUZZY kontrolovat jestli je hodnota v seznamu?
			self.currentElement.defaultValue = value
		elif type == FcTypes.NUMBER:
			self.currentElement.defaultValue = float(value)
		else:
			log.error("Unknown entry type " + str(type) + " for " + self.currentElement.name + "!")


	def endElement(self, name):
		log.debug("End element: " + name)
		if name == "entry":
			self.currentElement = None
		elif name == "section":
			self.currentElement = None
			self.sectionStack.pop()
		else:
			log.error("Unknown entry type: " + name)
			raise FcParseError("Unknown entry type: " + name)


	def parse(self, file, templateTree):
		self.sectionStack = [templateTree]
		self.currentElement = None
		# Parse the XML file
		XMLFileReader.parse(self, file)

