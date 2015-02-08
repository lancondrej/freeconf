#!/usr/bin/python

# Freeconf libs
from log import log
from base import *
# Other libs
from sax_file import XMLFileReader
from exception import FcParseError


class GUITemplateEnum:
	"""Constants for gui template elements"""
	NOELEMENT = 0
	ROOTELEMENT = 1
	WINDOW = 2
	MINWIDTH = 3
	MINHEIGHT = 4
	MAXWIDTH = 5
	MAXHEIGHT = 6
	TAB = 7
	TABNAME = 8
	TABICON = 9
	TABSECTION = 10
	TABSECTIONNAME = 11
	IMPORTTEMPLATEENTRY = 12
	IMPORTTEMPLATESECTION = 13

class GUITemplateFile(XMLFileReader):
	def __init__(self):
		XMLFileReader.__init__(self)
		self.__rootElementOpened = False
		self.__tabElement = None
		self.__sectionElement = None
		self.__curentElement = GUITemplateEnum.NOELEMENT

	def startElement(self, name, attrs):
		log.debug("Start element: " + name)

		if name == "freeconf-gui-template" and not self.__rootElementOpened:
			self.__rootElementOpened = True
			self.__curentElement = GUITemplateEnum.ROOTELEMENT
			return

		if not self.__rootElementOpened:
			log.error("You must enclose the GUI Template File with <freeconf-gui-template> and </freeconf-gui-template>.")
			return

		if name == "window":
			self.__curentElement = GUITemplateEnum.WINDOW
			return

		if name == "min-width":
			self.__curentElement = GUITemplateEnum.MINWIDTH
			return

		if name == "min-height":
			self.__curentElement = GUITemplateEnum.MINHEIGHT
			return

		if name == "max-width":
			self.__curentElement = GUITemplateEnum.MAXWIDTH
			return

		if name == "max-height":
			self.__curentElement = GUITemplateEnum.MAXHEIGHT
			return

		if name == "tab":
			log.debug("Start processing tab element")
			self.__sectionStack = []
			self.__tabElement = FcGTab()
			self.__curentElement = GUITemplateEnum.TAB
			# Creation of tab is postpoed to end of element tab-name
			return

		if name == "tab-name":
			if not self.__tabElement or self.__curentElement != GUITemplateEnum.TAB:
				log.error("Element <tab-name> is only allowed as first child of the <tab> element")
				return

			self.__curentElement = GUITemplateEnum.TABNAME
			return

		if name == "tab-icon":
			if not self.__tabElement:
				log.error("Element <tab-icon> is only allowed inside the <tab> element")
				return

			self.__curentElement = GUITemplateEnum.TABICON
			return

		if name == "tab-section":
			if not self.__tabElement:
				log.error("Element <tab-section> is only allowed inside the <tab> element")
				return

			log.debug("Start processing tab-section element")
			self.__curentElement = GUITemplateEnum.TABSECTION
			#there is always at least the root section on the stack
			parent = self.__sectionStack[-1]
			self.__sectionElement = FcCGSEntry(None, parent)
			parent.append(self.__sectionElement)
			self.__sectionStack.append(self.__sectionElement)
			return

		if name == "tab-section-name":
			if not self.__sectionElement or self.__curentElement != GUITemplateEnum.TABSECTION:
				log.error("Element <tab-section-name> is only allowed inside the <section> element")
				return

			self.__curentElement = GUITemplateEnum.TABSECTIONNAME
			return

		if name == "import-template-entry":
			if not self.__sectionElement or not self.__tabElement:
				log.error("Element <import-template-entry> is only allowed inside the <section> or <tab> element")
				return

			self.__curentElement = GUITemplateEnum.IMPORTTEMPLATEENTRY
			return

		if name == "import-template-section":
			if not self.__sectionElement or not self.__tabElement:
				log.error("Element <import-template-section> is only allowed inside the <section> or <tab> element")
				return

			# Extract attribute "primary"
			self.__primaryChild = None
			try:
				self.__primaryChild = attrs['primary']
			except(KeyError):
				pass

			self.__curentElement = GUITemplateEnum.IMPORTTEMPLATESECTION
			return

		return



	def characters(self, data):
		if self.__curentElement == GUITemplateEnum.MINWIDTH:
			try:
				self.__window.minWidth = int(data)
			except (ValueError):
				log.warning("wrong minimum width, must be an integer")
			return

		if self.__curentElement == GUITemplateEnum.MINHEIGHT:
			try:
				self.__window.minHeight = int(data)
			except:
				log.warning("wrong minimum height, must be an integer")
			return

		if self.__curentElement == GUITemplateEnum.MAXWIDTH:
			try:
				self.__window.maxWidth = int(data)
			except:
				log.warning("wrong maximum width, must be an integer")
			return

		if self.__curentElement == GUITemplateEnum.MAXHEIGHT:
			try:
				self.__window.maxHeight = int(data)
			except:
				log.warning("wrong maximum height, must be an integer")
			return

		if self.__curentElement == GUITemplateEnum.TABNAME:
			self.__tabElement.name = data
			return

		if self.__curentElement == GUITemplateEnum.TABICON:
			self.__window.entries[-1].icon = data
			#if data == "FC::NOICON":
				#self.__window.tabs[-1].icon = FcTypes.NOICON
			#elif data == "FC::SECURITY":
				#self.__window.tabs[-1].icon = FcTypes.SECURITY
			#elif data == "FC::PASSWORD":
				#self.__window.tabs[-1].icon = FcTypes.PASSWORD
			#elif data == "FC::NETWORK":
				#self.__window.tabs[-1].icon = FcTypes.NETWORK
			#elif data == "FC::TERMINAL":
				#self.__window.tabs[-1].icon = FcTypes.TERMINAL
			#elif data == "FC::USER":
				#self.__window.tabs[-1].icon = FcTypes.USER
			#elif data == "FC::TOOLS":
				#self.__window.tabs[-1].icon = FcTypes.TOOLS
			#elif data == "FC::DISPLAY":
				#self.__window.tabs[-1].icon = FcTypes.DISPLAY
			#elif data == "FC::PACKAGE":
				#self.__window.tabs[-1].icon = FcTypes.PACKAGE
			#elif data == "FC::FILE":
				#self.__window.tabs[-1].icon = FcTypes.FILE
			#elif data == "FC::DIRECTORY":
				#self.__window.tabs[-1].icon = FcTypes.DIRECTORY
			#else:
				#log.warning("Unknown icon type '" + data + "'")
			return

		if self.__curentElement == GUITemplateEnum.TABSECTIONNAME:
			self.__sectionElement.name = data
			return

		if self.__curentElement == GUITemplateEnum.IMPORTTEMPLATEENTRY:
			entry = self.__configTree.recursiveFindCEntry(data)
			if not entry:
				log.warning("Template entry at '" + data + "' not found")
				return

			if entry.guiBuddy != None:
				GUIEntry = entry.guiBuddy;
				GUIEntry.parent.disconnect(GUIEntry)

			tmpEntry = FcCGEntry(entry)
			entry.guiBuddy = tmpEntry
			self.__sectionStack[-1].append(tmpEntry)
			return

		if self.__curentElement == GUITemplateEnum.IMPORTTEMPLATESECTION:
			entry = self.__configTree.recursiveFindCEntry(data)
			if not entry or entry.type != FcTypes.SECTION:
				log.warning("Template section at '" + data + "' not found")
				return

			if entry.guiBuddy != None:
				GUIEntry = entry.guiBuddy;
				GUIEntry.parent.disconnect(GUIEntry)

			parent = self.__sectionStack[-1] # Gui entry's parent
			tmpEntry = FcCGSEntry(entry, parent)
			entry.guiBuddy = tmpEntry
			parent.append(tmpEntry)
			# Fill new section with entries form config tree
			tmpEntry.fill()
			if self.__primaryChild != None:
				if not entry.templateBuddy.multiple:
					log.error(
						"You can set primary child only on multiple section. %s is not multiple!" %
						(entry.name,)
					)
					return
				# Check if primary child exists in section
				(index, child) = entry.templateBuddy.findEntry(self.__primaryChild)
				if child == None:
					log.error(
						"Failed to find primary child %s in section %s!" %
						(self.__primaryChild, entry.name)
					)
					return
				tmpEntry.primaryChildName = self.__primaryChild
			return


		return

	def endElement(self, name):
		log.debug("End element: " + name)

		if name == "freeconf-gui-template":
			self.__curentElement = GUITemplateEnum.NOELEMENT
			self.__rootElementOpened = False
			return

		if name == "window":
			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "min-width":
			if self.__curentElement != GUITemplateEnum.MINWIDTH:
				log.error("Wrong location of end element: " + name)
				return

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "min-height":
			if self.__curentElement != GUITemplateEnum.MINHEIGHT:
				log.error("Wrong location of end element: " + name)
				return

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "max-width":
			if self.__curentElement != GUITemplateEnum.MAXWIDTH:
				log.error("Wrong location of end element: " + name)
				return

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "max-height":
			if self.__curentElement != GUITemplateEnum.MAXHEIGHT:
				log.error("Wrong location of end element: " + name)
				return

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "tab":
			if self.__tabElement.name == None:
				log.error("Current GUI tab has no name set! It will be ignored.")
			self.__curentElement = GUITemplateEnum.NOELEMENT
			self.__tabElement = None
			return

		if name == "tab-name":
			if self.__curentElement != GUITemplateEnum.TABNAME:
				log.error("Wrong location of end element: " + name)
				return

			# Create Tab if it does not exist
			# - We finally know name of the tab, so we can do it
			tab = self.__window.findEntry(self.__tabElement.name)[1]
			if tab == None:
				self.__window.append(self.__tabElement)
				# Create root section for tab
				rootSection = FcCGSEntry()
				rootSection.name = "rootSection"
				self.__tabElement.content = rootSection
			else:
				# Tab already exists
				self.__tabElement = tab

			self.__sectionStack.append(self.__tabElement.content)
			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "tab-icon":
			if self.__curentElement != GUITemplateEnum.TABICON:
				log.error("Wrong location of end element: " + name)
				return

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "tab-section":
			if self.__sectionElement.name == None:
				log.error("Current GUI tab has no name set! It will be ignored.")
			self.__curentElement = GUITemplateEnum.NOELEMENT
			self.__sectionStack.pop()
			if len(self.__sectionStack) == 0:
				self.__sectionElement = None
			return

		if name == "tab-section-name":
			if self.__curentElement != GUITemplateEnum.TABSECTIONNAME:
				log.error("Wrong location of end element: " + name)
				return

			# Check if there is not more sections of same name
			section = self.__sectionElement.parent.findEntry(self.__sectionElement.name)[1]
			if section != self.__sectionElement:	
				# Section with same name already existed
				# -> We delete the new section
				self.__sectionElement.parent.disconnect(self.__sectionElement)
				self.__sectionStack.pop()
				self.__sectionStack.append(section)
				self.__sectionElement = section

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "import-template-entry":
			if self.__curentElement != GUITemplateEnum.IMPORTTEMPLATEENTRY:
				log.error("Wrong location of end element: " + name)
				return

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

		if name == "import-template-section":
			if self.__curentElement != GUITemplateEnum.IMPORTTEMPLATESECTION:
				log.error("Wrong location of end element: " + name)
				return

			self.__curentElement = GUITemplateEnum.NOELEMENT
			return

	def parse(self, file, configTree, window):
		self.__rootElementOpened = False
		self.__tabElement = None
		self.__sectionElement = False
		self.__curentElement = GUITemplateEnum.NOELEMENT
		self.__sectionStack = []

		#if window == None:
			#log.error("Invalid reference found, expecting existing window object")
			#raise ValueError("Invalid reference found, expecting existing window object")

		#if configTree == None:
			#log.error("Invalid reference found, expecting existing config tree object")
			#raise ValueError("Invalid reference found, expecting existing config tree object")

		self.__window = window
		self.__configTree = configTree
		# Parse the XML file
		XMLFileReader.parse(self, file)


