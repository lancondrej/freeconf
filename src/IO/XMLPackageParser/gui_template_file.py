#!/usr/bin/python3

# Freeconf libs
from src.IO.XMLPackageParser.sax_file import XMLFileReader
from src.IO.exception_logging.log import log
from src.Model.constants import Types
from src.Model.entries.GUI.gsection import GSection
from src.Model.entries.GUI.gtab import GTab


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
    IMPORTENTRY = 12
    IMPORTCONTAINER = 13


class GUITemplateFile(XMLFileReader):
    def __init__(self):
        XMLFileReader.__init__(self)
        self._rootElementOpened = False
        self._tabElement = None
        self._sectionElement = None
        self._currentElement = GUITemplateEnum.NOELEMENT

    def startElement(self, name, attrs):
        log.debug("Start element: " + name)

        if name == "freeconf-gui-template" and not self._rootElementOpened:
            self._rootElementOpened = True
            self._currentElement = GUITemplateEnum.ROOTELEMENT
            return
        if not self._rootElementOpened:
            log.error("You must enclose the GUI Template File with <freeconf-gui-template> and </freeconf-gui-template>.")
            return
        if name == "window":
            self._currentElement = GUITemplateEnum.WINDOW
            return
        if name == "min-width":
            self._currentElement = GUITemplateEnum.MINWIDTH
            return
        if name == "min-height":
            self._currentElement = GUITemplateEnum.MINHEIGHT
            return
        if name == "max-width":
            self._currentElement = GUITemplateEnum.MAXWIDTH
            return
        if name == "max-height":
            self._currentElement = GUITemplateEnum.MAXHEIGHT
            return
        if name == "tab":
            log.debug("Start processing tab element")
            self._section_stack = []
            self._tabElement = GTab()
            self._currentElement = GUITemplateEnum.TAB
            # Creation of tab is postpoed to end of element tab-name
            return
        if name == "tab-name":
            if not self._tabElement or self._currentElement != GUITemplateEnum.TAB:
                log.error("Element <tab-name> is only allowed as first child of the <tab> element")
                return
            self._currentElement = GUITemplateEnum.TABNAME
            return
        if name == "tab-icon":
            if not self._tabElement:
                log.error("Element <tab-icon> is only allowed inside the <tab> element")
                return
            self._currentElement = GUITemplateEnum.TABICON
            return
        if name == "tab-section":
            if not self._tabElement:
                log.error("Element <tab-section> is only allowed inside the <tab> element")
                return
            log.debug("Start processing tab-section element")
            self._currentElement = GUITemplateEnum.TABSECTION
            #there is always at least the root section on the stack
            parent = self._section_stack[-1]
            self._sectionElement = GSection(parent)
            #parent.append(self._sectionElement)
            self._section_stack.append(self._sectionElement)
            return
        if name == "tab-section-name":
            if not self._sectionElement or self._currentElement != GUITemplateEnum.TABSECTION:
                log.error("Element <tab-section-name> is only allowed inside the <section> element")
                return
            self._currentElement = GUITemplateEnum.TABSECTIONNAME
            return
        if name == "import-entry":
            if not self._sectionElement and not self._tabElement:
                log.error("Element <import-template-entry> is only allowed inside the <section> or <tab> element")
                return
            self._currentElement = GUITemplateEnum.IMPORTENTRY
            return

        if name == "import-container":
            if not self._sectionElement and not self._tabElement:
                log.error("Element <import-template-container> is only allowed inside the <section> or <tab> element")
                return
            # Extract attribute "primary"
            self._primary_child = None
            try:
                self._primary_child = attrs['primary']
            except(KeyError):
                pass

            self._currentElement = GUITemplateEnum.IMPORTCONTAINER
            return

        return

    def characters(self, data):
        if self._currentElement == GUITemplateEnum.MINWIDTH:
            try:
                self.__window.minWidth = int(data)
            except ValueError:
                log.warning("wrong minimum width, must be an integer")
            return
        if self._currentElement == GUITemplateEnum.MINHEIGHT:
            try:
                self.__window.minHeight = int(data)
            except ValueError:
                log.warning("wrong minimum height, must be an integer")
            return
        if self._currentElement == GUITemplateEnum.MAXWIDTH:
            try:
                self.__window.maxWidth = int(data)
            except ValueError:
                log.warning("wrong maximum width, must be an integer")
            return
        if self._currentElement == GUITemplateEnum.MAXHEIGHT:
            try:
                self.__window.maxHeight = int(data)
            except ValueError:
                log.warning("wrong maximum height, must be an integer")
            return
        if self._currentElement == GUITemplateEnum.TABNAME:
            self._tabElement.name = data
            return
        if self._currentElement == GUITemplateEnum.TABICON:
            # self.__window.entries[-1].icon = data
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

        if self._currentElement == GUITemplateEnum.TABSECTIONNAME:
            self._sectionElement.name = data
            return

        if self._currentElement == GUITemplateEnum.IMPORTENTRY:
            entry = self.__data_tree.find_entry(data)
            if not entry:
                log.warning("Entry at '" + data + "' not found")
                return
            self._section_stack[-1].append(entry)
            return

        if self._currentElement == GUITemplateEnum.IMPORTCONTAINER:
            entry = self.__data_tree.find_entry(data)
            if not entry or entry.type != Types.CONTAINER:
                log.warning("Container at '" + data + "' not found")
                return
            parent = self._section_stack[-1] # Gui entry's parent
            parent.append(entry)
            # Fill new section with entries form config tree
            #gui_entry.fill()
            if self._primary_child is not None:
                if not entry.is_multiple_entry_container:
                    log.error(
                        "You can set primary child only on multiple section. %s is not multiple!" %
                        (entry.name,)
                    )
                    return
                # Check if primary child exists in section
                child = entry.template.get_entry(self._primary_child)
                if child is None:
                    log.error(
                        "Failed to find primary child %s in section %s!" %
                        (self._primary_child, entry.name)
                    )
                    return
                entry.primaryChildName = self._primary_child
            return
        return

    def endElement(self, name):
        log.debug("End element: " + name)

        if name == "freeconf-gui-template":
            self._currentElement = GUITemplateEnum.NOELEMENT
            self._rootElementOpened = False
            return

        if name == "window":
            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "min-width":
            if self._currentElement != GUITemplateEnum.MINWIDTH:
                log.error("Wrong location of end element: " + name)
                return

            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "min-height":
            if self._currentElement != GUITemplateEnum.MINHEIGHT:
                log.error("Wrong location of end element: " + name)
                return

            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "max-width":
            if self._currentElement != GUITemplateEnum.MAXWIDTH:
                log.error("Wrong location of end element: " + name)
                return

            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "max-height":
            if self._currentElement != GUITemplateEnum.MAXHEIGHT:
                log.error("Wrong location of end element: " + name)
                return

            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "tab":
            if self._tabElement.name is None:
                log.error("Current GUI tab has no name set! It will be ignored.")
            self._currentElement = GUITemplateEnum.NOELEMENT
            self._tabElement = None
            return

        if name == "tab-name":
            if self._currentElement != GUITemplateEnum.TABNAME:
                log.error("Wrong location of end element: " + name)
                return

            # Create Tab if it does not exist
            # - We finally know name of the tab, so we can do it
            tab = self.__window.get_entry(self._tabElement.name)
            if tab is None:
                self.__window.append(self._tabElement)
                # Create root section for tab
                rootSection = GSection()
                rootSection.name = "rootSection"
                self._tabElement.content = rootSection
            else:
                # Tab already exists
                self._tabElement = tab

            self._section_stack.append(self._tabElement.content)
            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "tab-icon":
            if self._currentElement != GUITemplateEnum.TABICON:
                log.error("Wrong location of end element: " + name)
                return

            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "tab-section":
            if self._sectionElement is not None:
                if self._sectionElement.name is None:
                    log.error("Current GUI tab has no name set! It will be ignored.")
            self._sectionElement.parent.append(self._sectionElement)
            self._currentElement = GUITemplateEnum.NOELEMENT
            self._section_stack.pop()
            if len(self._section_stack) == 0:
                self._sectionElement = None
            return

        if name == "tab-section-name":
            if self._currentElement != GUITemplateEnum.TABSECTIONNAME:
                log.error("Wrong location of end element: " + name)
                return

            # Check if there is not more sections of same name
            #section = self._sectionElement.parent.find_entry(self._sectionElement.name)
            #if section != self._sectionElement:
                # Section with same name already existed
                # -> We delete the new section
            #	self._sectionElement.parent.disconnect(self._sectionElement)
            #	self.__sectionStack.pop()
            #	self.__sectionStack.append(section)
            #	self._sectionElement = section

            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "import-entry":
            if self._currentElement != GUITemplateEnum.IMPORTENTRY:
                log.error("Wrong location of end element: " + name)
                return
            self._currentElement = GUITemplateEnum.NOELEMENT
            return

        if name == "import-container":
            if self._currentElement != GUITemplateEnum.IMPORTCONTAINER:
                log.error("Wrong location of end element: " + name)
                return
            self._currentElement = GUITemplateEnum.NOELEMENT
            return

    def parse(self, file, data_tree, window):
        self._rootElementOpened = False
        self._tabElement = None
        self._sectionElement = False
        self._currentElement = GUITemplateEnum.NOELEMENT
        self._section_stack = []

        #if window == None:
            #log.error("Invalid reference found, expecting existing window object")
            #raise ValueError("Invalid reference found, expecting existing window object")

        #if configTree == None:
            #log.error("Invalid reference found, expecting existing config tree object")
            #raise ValueError("Invalid reference found, expecting existing config tree object")
        #if window is None:
        #    window=GWindow()
        self.__window = window
        self.__data_tree = data_tree
        # Parse the XML file
        XMLFileReader.parse(self, file)


