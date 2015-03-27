#!/usr/bin/python
#
# script_file.py
# begin: 20.11.2011 by Jan Ehrenberger
#
# PyFC: Script File SAX Handler
#

# Freeconf libs
from log import log
from base import *
from group import FcFileLocation
from script import *
# Other libs
from sax_file import XMLFileReader
from exception import FcParseError


class ElementEnum:
	"""Constants for XML elements"""
	NO_ELEMENT = 0
	PATH = 1
	ARGUMENT = 2
	ON_LOAD = 3

	
class ScriptFile(XMLFileReader):

	def __init__(self):
		XMLFileReader.__init__(self)
		self.__reset()

	def __reset(self):
		self.script = None
	
	def startElement(self, name, attrs):
		log.debug("Start element: " + name)
		if not self.enclosing_tag and name == "freeconf-script":
			log.debug(name + " tag.")
			self.enclosing_tag = True
			# Create script object
			self.script = FcScript()
			return

		if not self.enclosing_tag:
			log.error("You must enclose the Script File with <freeconf-script> and </freeconf-script>.")
			return

		if name == "path":
			self.xml_element = ElementEnum.PATH
		elif name == "argument":
			self.xml_element = ElementEnum.ARGUMENT
		elif name == "on-load":
			self.script.setTrigger(FcOnLoadTrigger())
			self.xml_element = ElementEnum.ON_LOAD
		else:
			log.error("Unknown XML element: " + name)
			self.xml_element = ElementEnum.NO_ELEMENT

	def endElement(self, name):
		log.debug("End element: " + name)
		self.xml_element = ElementEnum.NO_ELEMENT

	def characters(self, data):
		data = data.strip()
		if data == '':
			return # Ignore white space in XML

		if self.xml_element == ElementEnum.PATH:
			self.script.path.name = data
		elif self.xml_element == ElementEnum.ARGUMENT:
			self.script.arguments.append(data)

	def parse(self, f):
		self.__reset()
		XMLFileReader.parse(self, f)

