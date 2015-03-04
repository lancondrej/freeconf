#!/usr/bin/python

# Freeconf libs
from log import log
from base import *
# Other libs
from src.PackageParser.sax_file import XMLFileReader
from exception import FcParseError


import types as Fc

class GUILabelEnum:
	"""Constants for gui label elements"""
	NOELEMENT = 0
	ROOTELEMENT = 1
	WINDOW = 2
	TITLE = 3
	TAB = 4
	TABNAME = 5
	TABLABEL = 6
	TABDESCRIPTION = 7
	TABSECTION = 8
	TABSECTIONNAME = 9
	TABSECTIONLABEL = 10

class GUILabelFile(XMLFileReader):
	def __init__(self):
		XMLFileReader.__init__(self)
		self.__rootElementOpened = False
		self.__currentTab = None
		self.__sectionStack = []
		self.__currentElement = GUILabelEnum.NOELEMENT

	def startElement(self, name, attrs):
		log.debug("Start element: " + name)
		if not self.__rootElementOpened and name == "freeconf-gui-label":
			self.__rootElementOpened = True
			self.__currentElement = GUILabelEnum.ROOTELEMENT
			return

		if not self.__rootElementOpened:
			log.error("You must enclose the GUI Label File with <freeconf-gui-label> and </freeconf-gui-label>.")
			return
		if name == "window":
			self.__currentElement = GUILabelEnum.WINDOW
			return
		if name == "title":
			self.__currentElement = GUILabelEnum.TITLE
			return
		if name == "tab":
			self.__currentElement = GUILabelEnum.TAB
			self.__sectionStack = []
			self.__currentTab = None
			return
		if name == "name":
			if len(self.__sectionStack) == 0:
				self.__currentElement = GUILabelEnum.TABNAME
				return
			else:
				self.__currentElement = GUILabelEnum.TABSECTIONNAME
				return
			#log.warning("Element <name> is only allowed as the first child element of <tab> or <section> element")
			#return
		if name == "label":
			# there is always one section automatically created after tab name has been processed
			if len(self.__sectionStack) == 1:
				self.__currentElement = GUILabelEnum.TABLABEL
			else:
				self.__currentElement = GUILabelEnum.TABSECTIONLABEL
			return
		if name == "description":
			self.__currentElement = GUILabelEnum.TABDESCRIPTION
			return
		if name == "section":
			if len(self.__sectionStack) == 0:
				log.error("Empty section stack. Cannot parse the label file")
				self.__sectionStack.append(0)
				return
			if not self.__sectionStack[-1]:
				log.warning("Found <section> child element before its parent's section <name>")
				self.__sectionStack.append(0)
				return
			self.__sectionStack.append(0)
			self.__currentElement = GUILabelEnum.TABSECTION
			return


	def characters(self, data):
		if self.__currentElement == GUILabelEnum.TITLE:
			self.__window.title = data
			return

		if self.__currentElement == GUILabelEnum.TABNAME:
			log.debug("setting tab name to " + data)
			self.__currentTab = filter(lambda x:x.name == data, self.__window.entries)
			if self.__currentTab == []:
				log.warning("Tab element " + data + " not found in the GUI tree")
				return
			self.__currentTab = self.__currentTab[0]
			self.__sectionStack.append(self.__currentTab.content)
			return

		if self.__currentElement == GUILabelEnum.TABLABEL:
			if not self.__currentTab:
				return
			log.debug("setting tab label to " + data)
			self.__currentTab.label = data
			return

		if self.__currentElement == GUILabelEnum.TABDESCRIPTION:
			if not self.__currentTab:
				return
			self.__currentTab.description = data
			return

		if self.__currentElement == GUILabelEnum.TABSECTIONNAME:
			if self.__sectionStack[-1]:
				return
			log.debug("setting section name to " + data)
			self.__sectionStack.pop()
			entry = filter(lambda x:x.name == data, self.__sectionStack[-1].entries)
			if not entry:
				log.warning("Section element " + data + " not found in the GUI tree")
				self.__sectionStack.append(0)
				return
			entry = entry[0]
			if isinstance(entry, FcCGSEntry):
				self.__sectionStack.append(entry)
			else:
				log.warning("Element "+ data + " is not a section")
				return
			return
		if self.__currentElement == GUILabelEnum.TABSECTIONLABEL:
			if not self.__sectionStack[-1]:
				return
			log.debug("setting section label to " + data)
			self.__sectionStack[-1].label = data
			return
		return

	def endElement(self, name):
		log.debug("End element: " + name)
		if name == "freeconf-gui-label":
			self.__currentElement = GUILabelEnum.NOELEMENT
			self.__rootElementOpened = False
			return

		if name == "window":
			self.__currentElement = GUILabelEnum.NOELEMENT
			return

		if name == "title":
			if self.__currentElement == GUILabelEnum.TITLE:
				self.__currentElement = GUILabelEnum.NOELEMENT
				return
			else:
				log.error("Wrong location of end element: " + name)
				return
			return

		if name == "tab":
			self.__currentElement = GUILabelEnum.NOELEMENT
			self.__currentTab = None
			return

		if name == "name":
			self.__currentElement = GUILabelEnum.NOELEMENT
			return

		if name == "label":
			self.__currentElement = GUILabelEnum.NOELEMENT

		if name == "description":
			self.__currentElement = GUILabelEnum.NOELEMENT
			return

		if name == "section":
			self.__currentElement = GUILabelEnum.NOELEMENT
			self.__sectionStack.pop()
			return


	def parse(self, file, window):
		self.__rootElementOpened = False
		self.__currentTab = None
		self.__currentElement = GUILabelEnum.NOELEMENT
		self.__sectionStack = []
		#if window == None:
			#log.error("Invalid reference found, expecting existing window object")
			#raise ValueError("Invalid reference found, expecting existing window object")
		self.__window = window
		XMLFileReader.parse(self, file)

