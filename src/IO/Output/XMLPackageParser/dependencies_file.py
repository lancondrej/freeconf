#!/usr/bin/python
#
# dependencies_file.py
# begin: 16.10.2010 by Jan Ehrenberger
#
# PyFC: Dependecies File SAX Handler
#

# Freeconf libs
from log import log
from base import *
from dependencies import FcDependency, FcActionSet
from sax_file import XMLFileReader
from exception import FcParseError


class ElementEnum:
	"""Constants for template elements"""
	NO_ELEMENT = 0
	IF = 1
	CONDITION = 2
	THEN = 3
	ELSE = 4
	SET = 5
	ELEMENT = 6
	VALUE = 7


class DependenciesFile(XMLFileReader):
	def __init__(self):
		XMLFileReader.__init__(self)
		self.__reset()

	def __reset(self):
		# List of dependencies
		self.dependencies = []
		# Current dependency
		self.current_dep = None
		# Current list of set actions
		self.current_set_list = None
		# Current set action
		self.current_set = None
		# ID of basic XML element
		self.xml_element = ElementEnum.NO_ELEMENT

	def startElement(self, name, attrs):
		log.debug("Start element: " + name)
		# TODO: Udelat base tridu, se zpracovanim enclosing tagu
		if not self.enclosing_tag and name == "freeconf-dependencies":
			log.debug("freeconf-dependencies tag.")
			self.enclosing_tag = True
			return

		if not self.enclosing_tag:
			log.error("You must enclose the Template File with <freeconf-dependencies> and </freeconf-dependencies>.")
			return

		## Process dependency
		if name == "if":
			assert self.xml_element == ElementEnum.NO_ELEMENT
			self.current_dep = FcDependency()
			self.xml_element = ElementEnum.IF

		elif name == "condition":
			assert self.current_dep != None
			self.xml_element = ElementEnum.CONDITION

		elif name == "then":
			assert self.current_dep != None
			self.current_set_list = self.current_dep.thenActions
			self.xml_element = ElementEnum.THEN

		elif name == "else":
			assert self.current_dep != None
			self.current_set_list = self.current_dep.elseActions
			self.xml_element = ElementEnum.ELSE

		elif name == "set":
			assert self.current_set_list != None

			# Process property attribute
			prop = None
			try:
				prop = attrs['property']
			except(KeyError):
				log.error("Set action is missing property attribute!")
				return

			self.xml_element = ElementEnum.SET
			self.current_set = FcActionSet(prop)

		elif name == "element":
			assert self.current_set != None
			self.xml_element = ElementEnum.ELEMENT

		elif name == "value":
			assert self.current_set != None

			# Process value-type attribute
			value_type = "constant" # Default value type
			try:
				value_type = attrs['value-type']
			except(KeyError):
				pass
			self.current_set.valueType = value_type

			self.xml_element = ElementEnum.VALUE

		else:
			log.error("Unknown entry type: " + name)

	def endElement(self, name):
		log.debug("End element: " + name)

		if name == "if"	:
			assert self.current_dep != None
			self.dependencies.append(self.current_dep)

		elif name in ("then", "else"):
			self.current_set_list = None

		elif name == "set":
			self.current_set_list.append(self.current_set)
			self.current_set = None

		self.xml_element = ElementEnum.NO_ELEMENT

	def characters(self, data):
		if self.xml_element == ElementEnum.CONDITION:
			assert self.current_dep != None
			self.current_dep.conditionText = data

		elif self.xml_element == ElementEnum.ELEMENT:
			assert self.current_set != None
			self.current_set.elementsText.append(data)

		elif self.xml_element == ElementEnum.VALUE:
			assert self.current_set != None
			self.current_set.value = data

	def parse(self, file):
		self.__reset()
		# Parse the XML file
		XMLFileReader.parse(self, file)
		return self.dependencies
