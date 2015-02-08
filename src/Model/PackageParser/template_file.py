#!/usr/bin/python
#
# template.py
# begin: 8.7.2010 by Jan Ehrenberger
#
# PyFC: Template File SAX Handler
#

# Freeconf libs
from log import log
from base import *
# Other libs
from sax_file import XMLFileReader
from exception import FcParseError


class TemplateEnum:
	"""Constants for template elements"""
	NO_TMP_ELEMENT = 0
	SECTION_NAME = 1
	KEYWORD_NAME = 2
	MULTIPLE = 3
	PROPERTIES = 4
	DEPENDENCIES = 5
	ACTIVE = 6
	MANDATORY = 7
	GROUP = 8
	TARGET = 9

class PropertyEnum:
	"""Constants for property elements"""
	NO_PROP_ELEMENT = 0
	PRECISION = 1
	MIN = 2
	MAX = 3
	STEP = 4
	DATA = 5
	REGEXP = 6
	ZEROS = 7
	SIGN = 8


class TemplateFile(XMLFileReader):
	def __init__(self):
		XMLFileReader.__init__(self)
		# Stack for the Template File sections being created
		self.section_stack = []
		# Current entry
		self.current_entry = None
		# ID of basic XML element
		self.template_enum = TemplateEnum.NO_TMP_ELEMENT
		# ID of property XML element
		self.property_enum = PropertyEnum.NO_PROP_ELEMENT
		# List of available groups
		self.groups = {}
		self.defaultGroup = None # Default group
		# List of available value lists
		self.lists = {}
		# Enclosing tag semaphor
		self.enclosing_tag = False
		# top of the tree
		self.topSection = None
		# Reference to package or plugin where this template file belongs
		self.package = None

	def startElement(self, name, attrs):
		log.debug("Start element: " + name)
		if not self.enclosing_tag and name == "freeconf-template":
			log.debug("freeconf-template tag.")
			self.enclosing_tag = True

		if not self.enclosing_tag:
			log.error("You must enclose the Template File with <freeconf-template> and </freeconf-template>.")
			return

		## Process section
		if name == "section" or name == "freeconf-template":
			section = None
			if name == "freeconf-template":
				if self.topSection == None:
					section = FcTSEntry()
					self.topSection = section
				else:
					# Toplevel section already exists
					section = self.topSection
			elif len(self.section_stack) > 0:
				(i, section) = self.section_stack[-1].findEntry(name)
				if section == None:
					# Section does not exist yet, we have to create new one
					section = FcTSEntry()
					log.debug("Adding new section %s to %s" % (str(section), str(self.section_stack[-1])))
					section.package = self.package # Set package to first package that referenced this section
					self.section_stack[-1].append(section)
			else:
				raise FcParseError("Invalid state.")
			self.section_stack.append(section)
			self.current_entry = section
			return

		if name == "bool":
			log.debug("Adding bool.")
			self.current_entry = FcTKBool()
			self.current_entry.package = self.package
			self.section_stack[-1].append(self.current_entry)
			return

		if name == "fuzzy":
			log.debug("Adding fuzzy.")
			self.current_entry = FcTKFuzzy()
			self.current_entry.package = self.package
			self.section_stack[-1].append(self.current_entry)
			return

		if name == "number":
			log.debug("Adding number.")
			self.current_entry = FcTKNumber()
			self.current_entry.package = self.package
			self.section_stack[-1].append(self.current_entry)
			return

		if name == "string":
			log.debug("Adding string.")
			self.current_entry = FcTKString()
			self.current_entry.package = self.package
			self.section_stack[-1].append(self.current_entry)
			return

		if name == "reference":
			log.debug("Adding reference.")
			self.current_entry = FcTReference()
			self.current_entry.package = self.package
			self.section_stack[-1].append(self.current_entry)
			return

		# at this moment, current_entry must point to an existing entry
		assert self.current_entry

		if name == "section-name":
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				self.template_enum = TemplateEnum.SECTION_NAME
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "entry-name":
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				self.template_enum = TemplateEnum.KEYWORD_NAME
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "active":
			if isinstance(self.current_entry, FcTSEntry):
				log.error("Element <active> can only be set for keys not sections")
				return
				
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				self.template_enum = TemplateEnum.ACTIVE
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "mandatory":
			if isinstance(self.current_entry, FcTSEntry):
				log.error("Element <mandatory> can only be set for keys not sections")
				return
				
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				self.template_enum = TemplateEnum.MANDATORY
			else:
				log.error("Wrong location of element: " + name)
			return
				
		if name == "multiple":
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				# Enable multiple on current entry
				assert self.current_entry != None
				if self.current_entry.type != FcTypes.SECTION:
					log.error("Element <multiple> is allowed only for section!")
					return
				self.current_entry.multiple = True

				self.template_enum = TemplateEnum.MULTIPLE
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "group":
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				self.template_enum = TemplateEnum.GROUP
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "target":
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				self.template_enum = TemplateEnum.TARGET
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "properties":
			if self.template_enum == TemplateEnum.NO_TMP_ELEMENT:
				self.template_enum = TemplateEnum.PROPERTIES
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "precision":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.PRECISION
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "min":
			if self.template_enum in (TemplateEnum.PROPERTIES, TemplateEnum.MULTIPLE) and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.MIN
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "max":
			if self.template_enum in (TemplateEnum.PROPERTIES, TemplateEnum.MULTIPLE) and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.MAX
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "step":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.STEP
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "print-sign":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.SIGN
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "leading-zeros":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.ZEROS
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "data":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.DATA
			else:
				log.error("Wrong location of element: " + name)
			return

		if name == "regexp":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.NO_PROP_ELEMENT:
				self.property_enum = PropertyEnum.REGEXP
			else:
				log.error("Wrong location of element: " + name)
			return

		log.error("Unknown entry type: " + name)

	def endElement(self, name):
		log.debug("End element: " + name)
		if name in ("freeconf-template", "section"):
			section = self.section_stack.pop()
			if section.group == None:
				# If group was not set, use the default group.
				section.group = self.defaultGroup
			self.current_entry = None
			self.control()
			return

		if name in ("bool", "fuzzy", "number", "string", "reference"):
			assert self.current_entry

			if self.current_entry.name == "" or self.current_entry.name == None:
				log.error("Ignoring entry with missing name!")
				# Remove corrupted entry from the stack
				self.section_stack[-1].disconnect(self.current_entry)
				
			# Check for duplicities. If there is already an element with same name, remove the new one.
			(i, entry) = self.section_stack[-1].findEntry(self.current_entry.name)
			if entry != self.current_entry:
				log.error("Ignoring entry. Entry with name %s already exists!" % (self.current_entry.name,))
				# Remove corrupted entry from the stack
				self.section_stack[-1].disconnect(self.current_entry)

			# Check fuzzy entry
			# TODO: ten check by se hodilo nejak centralizovat, napr. zabudovat primo do template typu
			elif name == "fuzzy" and self.current_entry.list == None:
				log.error("Fuzzy entry %s is missing data!" % (self.current_entry.name,))
				# Remove corrupted entry from the stack
				self.section_stack[-1].disconnect(self.current_entry)

			elif self.current_entry.group == None:
				# Take group from parent section if it was not set on this entry
				self.current_entry.group = self.current_entry.parent.group
				if self.current_entry.group == None:
					# If parent section did not have group set, use default group
					self.current_entry.group = self.defaultGroup
				
			self.current_entry = None
			self.control()
			return

		if name == "section-name":
			if self.template_enum == TemplateEnum.SECTION_NAME:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "entry-name":
			if self.template_enum == TemplateEnum.KEYWORD_NAME:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "active":
			if self.template_enum == TemplateEnum.ACTIVE:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "mandatory":
			if self.template_enum == TemplateEnum.MANDATORY:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "multiple":
			if self.template_enum == TemplateEnum.MULTIPLE:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "group":
			if self.template_enum == TemplateEnum.GROUP:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "target":
			if self.template_enum == TemplateEnum.TARGET:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "properties":
			if self.template_enum == TemplateEnum.PROPERTIES:
				self.template_enum = TemplateEnum.NO_TMP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "precision":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.PRECISION:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "min":
			if self.template_enum in (TemplateEnum.PROPERTIES, TemplateEnum.MULTIPLE) and self.property_enum == PropertyEnum.MIN:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "max":
			if self.template_enum in (TemplateEnum.PROPERTIES, TemplateEnum.MULTIPLE) and self.property_enum == PropertyEnum.MAX:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "step":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.STEP:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "print-sign":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.SIGN:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return
			
		if name == "leading-zeros":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.ZEROS:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "data":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.DATA:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		if name == "regexp":
			if self.template_enum == TemplateEnum.PROPERTIES and self.property_enum == PropertyEnum.REGEXP:
				self.property_enum = PropertyEnum.NO_PROP_ELEMENT
			else:
				log.error("Wrong location of end element: " + name)
			return

		log.error("Unknown entry type: " + name)
		return

	def characters(self, data):
		data = data.strip()
		if data == '':
			return # Ignore white space in XML

		# Set name of section or keyword
		if self.template_enum in (TemplateEnum.SECTION_NAME, TemplateEnum.KEYWORD_NAME):
			assert self.current_entry
			log.debug("Setting entry name to " + data)
			self.current_entry.name = data
			# We set the label, just for case that it is missing in help file
			self.current_entry.label = data
			return
		elif self.template_enum == TemplateEnum.ACTIVE:
			assert self.current_entry
			log.debug("Setting entry activity to " + data)
			if data == "yes":
				self.current_entry.statciActive = True
			elif data == "no":
				self.current_entry.staticActive = False
			else:
				log.error("Unknown value \"" + data + "\" in the active element, expecting yes or no")
			return
		elif self.template_enum == TemplateEnum.MANDATORY:
			assert self.current_entry
			log.debug("Setting mandatory to " + data)
			if data == "yes":
				self.current_entry.staticMandatory = True
			elif data == "no":
				self.current_entry.staticMandatory = False
			else:
				log.error("Unknown value \"" + data + "\" in the mandatory element, expecting yes or no")
			return
		elif self.template_enum == TemplateEnum.GROUP:
			assert self.current_entry
			try:
				self.current_entry.group = self.groups[data]
			except KeyError:
				log.error(
					"Group %s was not found while processing entry %s!" %
					(data, self.current_entry.name)
				)
			return
		elif self.template_enum == TemplateEnum.TARGET:
			assert self.current_entry
			# Find target in template tree
			target = self.topSection.recursiveFindTEntry(data)
			if target == None:
				log.error("Target %s was not found in template tree for entry %s!" % (data, str(self.current_entry)))
			else:
				self.current_entry.target = target
			return

		## Process multiple properties
		elif self.template_enum == TemplateEnum.MULTIPLE:
			assert self.current_entry
			if self.property_enum == PropertyEnum.MIN:
				self.current_entry.multipleMin = int(data)
			elif self.property_enum == PropertyEnum.MAX:
				self.current_entry.multipleMax = int(data)

		## Process properties
		elif self.template_enum == TemplateEnum.PROPERTIES:
			assert self.current_entry # Properties are allowed only for existing entries

			if self.property_enum == PropertyEnum.PRECISION:
				if self.current_entry.type != FcTypes.NUMBER:
					log.error("Element <precision> is allowed only for number!")
					return
				log.debug("Setting number precision to " + data)
				try:
					self.current_entry.precision = int(data)
				except (ValueError):
					self.current_entry.precision = 0
					log.warning("Trying to set precision " + data + " which is not a whole number")

			if self.property_enum == PropertyEnum.MIN:
				if self.current_entry.type not in (FcTypes.NUMBER, FcTypes.FUZZY):
					log.error("Element <min> is allowed only for number and fuzzy!")
					return
				log.debug("Setting number min to " + data)
				self.current_entry.min = float(data)

			elif self.property_enum == PropertyEnum.MAX:
				if self.current_entry.type not in (FcTypes.NUMBER, FcTypes.FUZZY):
					log.error("Element <max> is allowed only for number and fuzzy!")
					return
				log.debug("Setting number max to " + data)
				self.current_entry.max = float(data)

			elif self.property_enum == PropertyEnum.STEP:
				if self.current_entry.type != FcTypes.NUMBER:
					log.error("Element <step> is allowed only for number!")
					return
				log.debug("Setting number step to " + data)
				self.current_entry.step = float(data)

			elif self.property_enum == PropertyEnum.SIGN:
				if self.current_entry.type != FcTypes.NUMBER:
					log.error("Element <sign> is allowed only for number!")
					return
				log.debug("Setting number sign format to " + data)
				if data == "yes":
					self.current_entry.printSign = True
				else:
					self.current_entry.printSign = False
					
			elif self.property_enum == PropertyEnum.ZEROS:
				if self.current_entry.type != FcTypes.NUMBER:
					log.error("Element <zeros> is allowed only for number!")
					return
				log.debug("Setting number zeros format to " + data)
				if data == "yes":
					self.current_entry.leadingZeros = True
				else:
					self.current_entry.leadingZeros = False

			elif self.property_enum == PropertyEnum.DATA:
				if self.current_entry.type not in (FcTypes.STRING, FcTypes.FUZZY):
					log.error("Element <data> is allowed only for string and fuzzy!")
					return
				if data not in self.lists:
					log.error("List " + data + " was not found!")
					return
				log.debug("Adding list " + data)
				# TODO: nemela by se tady osetrit neexistence string listu?
				self.current_entry.list = self.lists[data]

			elif self.property_enum == PropertyEnum.REGEXP:
				if self.current_entry.type != FcTypes.STRING:
					log.error("Element <regexp> is allowed only for string!")
					return
				self.current_entry.regExp = data
			return

	def control(self):
		# TODO
		return

	def parse(self, file, tree, groups, lists = {}, package = None):
		self.enclosing_tag = False
		self.section_stack = []
		self.current_entry = None
		self.template_enum = TemplateEnum.NO_TMP_ELEMENT
		self.property_enum = PropertyEnum.NO_PROP_ELEMENT
		self.groups = groups
		self.defaultGroup = groups["default"]
		self.lists = lists
		self.package = package
		# Add top section if any
		self.topSection = tree
		# Parse the XML file
		XMLFileReader.parse(self, file)
		return self.topSection

