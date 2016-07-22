#!/usr/bin/python3
#

import os

from Controller.GUI import GContainer
from Controller.GUI.gtab import GTab
from View.GUI.gwindow import GWindow

from IO.Input.XMLPackageParser.parser import XMLParser
from Model.constants import Types
from Model.entries.GUI.gentry import GEntry
from Model.package import PackageBase
from Controller.exception_logging.exception import FcPackageLoadError, FcInconsistencyError


class PackageInterface (object):
    """Client's entry point to the package"""
    def __init__(self):
        self._package = None

    def load_package(self, name):
        """Loads the package by name"""
        try:
            self._package = PackageBase(name)
            input_parser = XMLParser(os.path.abspath('packages/' + name))
            self._package.input = input_parser
            self._package.current_language = "en"
            self._package.load_package()
            self._package.load_plugins()
            return True
        except FcPackageLoadError:
            self._package = None
            raise

    def save_configuration (self):
        """Saves all value changes to the output and performs the XSL transformation"""
        if self._package is None: return
        try:
            self._package.writeOutput()
            self._package.transform()
        except FcInconsistencyError:
            raise

    @property
    def window (self):
        """returns the proxy object of the top-level element of the GUI tree"""
        if self._package is None:
            return
        return self._package.gui_tree.proxy

    def showAllActiveWidgets (self, show):
        """Turns showing advanced widgets on or off"""
        self._package.gui_tree.showAll(show)


class FcGUICommunicator(object):
    """Class that handles communication between the library and the client."""

    def __init__ (self, guiEntry):
        self.__guiEntry = guiEntry
        self.__clientEntry = None
        self.__tabs = []
        self.__children = []

    def processSignal (self, signal, value):
        """Signal brigde between the client and the library"""
        if self.__clientEntry != None:
            self.__clientEntry.processSignal(signal, value)

    @property
    def value (self):
        """Returns the corresponding value from the config tree"""
        if self.__guiEntry.type == Types.BOOL:
            return self.__guiEntry.configBuddy.grade
        else:
            return self.__guiEntry.configBuddy.value

    @value.setter
    def value (self, value):
        """Set value of associated config entry. Apllication should not call this metod while processing signal CHANGE_VALUE!"""
        if self.__guiEntry.type == Types.BOOL:
            self.__guiEntry.configBuddy.grade = value
        else:
            self.__guiEntry.configBuddy.value = value

    @property
    def valueRepr (self):
        """Returns string representation of value as it will be written to output file."""
        return self.__guiEntry.configBuddy.valueRepr

    @property
    def list (self):
        """Returns True if the object is a list"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type in (Types.STRING, Types.FUZZY):
            return self.__guiEntry.configBuddy.list
        else:
            return None

    @property
    def grade (self):
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type in (Types.FUZZY, Types.BOOL):
            return self.__guiEntry.configBuddy.grade
        else:
            return None

    def disconnect (self):
        """Disconnects the client object"""
        self.__clientEntry = None

    def connectClient (self, clientEntry):
        """Connects the client object"""
        self.__clientEntry = clientEntry

    @property
    def minWidth (self):
        """Min width of the config window"""
        if isinstance(self.__guiEntry, GWindow):
            return self.__guiEntry.minWidth
        else:
            return None

    @property
    def maxWidth (self):
        """Max width of the config window"""
        if isinstance(self.__guiEntry, GWindow):
            return self.__guiEntry.maxWidth
        else:
            return None

    @property
    def minHeight (self):
        """Min height of the config window"""
        if isinstance(self.__guiEntry, GWindow):
            return self.__guiEntry.minHeight
        else:
            return None

    @property
    def maxHeight (self):
        """Max height of the config window"""
        if isinstance(self.__guiEntry, GWindow):
            return self.__guiEntry.maxHeight
        else:
            return None

    @property
    def tabs (self):
        """Returns a list of tabs' proxies"""
        if isinstance(self.__guiEntry, GWindow):
            if len(self.__tabs) == 0:
                for name, tab in self.__guiEntry.entries.items():
                    self.__tabs.append(tab.proxy)
            return self.__tabs
        else:
            return None

    @property
    def title (self):
        """Returns title of the config window"""
        if isinstance(self.__guiEntry, GWindow):
                return self.__guiEntry.title
        else:
            return None

    @property
    def icon (self):
        """Returns the tab's icon"""
        if isinstance(self.__guiEntry, GTab):
            return self.__guiEntry.icon
        else:
            return None

    @property
    def description (self):
        """Returns the tab's description"""
        if isinstance(self.__guiEntry, GTab):
            return self.__guiEntry.description
        else:
            return None

    @property
    def content (self):
        """Returns the tab's content proxy"""
        if isinstance(self.__guiEntry, GTab):
            return self.__guiEntry.content.proxy
        else:
            return None

    @property
    def empty (self):
        """Returns True if the tab or section is empty"""
        if isinstance(self.__guiEntry, GTab) or isinstance(self.__guiEntry, GContainer):
            return self.__guiEntry.empty
        else:
            return None

    @property
    def name (self):
        """Returns name of the entry"""
        return self.__guiEntry.name

    @property
    def help (self):
        """Returns help of the entry"""
        if isinstance(self.__guiEntry, GEntry):
            return self.__guiEntry.configBuddy.key_help()
        else:
            return None


    @property
    def label (self):
        """Returns label of the entry"""
        if isinstance(self.__guiEntry, GEntry):
            return self.__guiEntry.label
        else:
            return None

    @property
    def children (self):
        """Returns list of section's children proxies"""
        if isinstance(self.__guiEntry, GContainer):
            if len(self.__children) == 0:
                for name, child in self.__guiEntry.entries.items():
                    self.__children.append(child.proxy)
            return self.__children
        else:
            return None

    @property
    def showAllChildren (self):
        """Returns True if show all is enabled"""
        if isinstance(self.__guiEntry, GContainer):
            return self.__guiEntry._showAllChildren
        else:
            return None

    @property
    def type (self):
        """Returns type of the entry"""
        if isinstance(self.__guiEntry, GEntry):
            return self.__guiEntry.type
        else:
            return None

    @property
    def enabled (self):
        """Returns True if the entry is enabled"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.configBuddy is not None:
            return self.__guiEntry.configBuddy.enabled
        else:
            return None

    @property
    def min (self):
        """Returns min of the number entry"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type == Types.NUMBER:
            return self.__guiEntry.configBuddy.min
        else:
            return None

    @property
    def max (self):
        """Returns max of the number entry"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type == Types.NUMBER:
            return self.__guiEntry.configBuddy.max
        else:
            return None

    @property
    def step (self):
        """Returns step of the number entry"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type == Types.NUMBER:
            return self.__guiEntry.configBuddy.step
        else:
            return None

    @property
    def precision (self):
        """Returns precision of the number entry"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type == Types.NUMBER:
            return self.__guiEntry.configBuddy.precision
        else:
            return None

    @property
    def active (self):
        """Returns True if the entry or section is active"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.configBuddy is not None:
            return self.__guiEntry.configBuddy.dynamic_active
        else:
            return None

    @property
    def mandatory (self):
        """Returns True if the entry is mandatory"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.configBuddy is not None:
            return self.__guiEntry.configBuddy.dynamic_mandatory
        else:
            return None

    @property
    def inconsistent (self):
        """Returns True if the entry or the section or the tab or the window is mandatory"""
        if isinstance(self.__guiEntry, GEntry):
            return self.__guiEntry.inconsistent
        else:
            return None

    @property
    def multiple (self):
        """Returns True if entry is multiple."""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type == Types.CONTAINER and self.__guiEntry.configBuddy != None:
            return self.__guiEntry.configBuddy.multiple
        else:
            return None

    @property
    def isMultipleEntryContainer(self):
        """Returns True if the entry is multiple entry container"""
        if isinstance(self.__guiEntry, GEntry) and self.__guiEntry.type == Types.CONTAINER and self.__guiEntry.configBuddy != None:
            return self.__guiEntry.configBuddy.is_multiple_entry_container()
        else:
            return None

    def createEntry(self):
        """Create new entry in multiple entry container."""
        if not self.isMultipleEntryContainer:
            return None

        centry = self.__guiEntry.configBuddy.createEntry()
        guiEntry = self.__guiEntry.appendCEntry(centry)
        self.__children.append(guiEntry.proxy)
        if centry.type == Types.CONTAINER:
            # Fill config entry section
            centry.fill()
            # Fill GUI Entry section
            guiEntry.fill()
        guiEntry.initState() # Initialize state
        return guiEntry.proxy

    def deleteNode(self):
        """Delete instance of multiple config entry."""
        if not self.multiple or self.isMultipleEntryContainer:
            # Entry is not deletable
            return None
        # Remove instance of communicator from parent's client interface
        if self.__guiEntry.parent != None:
            parentComm = self.__guiEntry.parent.proxy
            parentComm.__children.remove(self)
        # Disconnect instance of config entry from GUI tree and config tree
        centry = self.__guiEntry.configBuddy
        self.__guiEntry.parent.disconnect(self.__guiEntry)
        centry.parent.disconnect(centry)
        self.disconnect()

    def moveUp(self):
        """Move config entry one position up in the section."""
        if not self.multiple or self.isMultipleEntryContainer:
            # Entry is not moveable
            return None
        # Move GUI entry
        gentry = self.__guiEntry
        if gentry.parent != None:
            gentry.parent.moveUp(gentry)
        # Move config entry
        centry = self.__guiEntry.configBuddy
        if centry.parent != None:
            centry.parent.moveUp(centry)

    def moveDown(self):
        """Move config entry one position down in the section."""
        if not self.multiple or self.isMultipleEntryContainer:
            # Entry is not moveable
            return None
        # Move GUI entry
        gentry = self.__guiEntry
        if gentry.parent != None:
            gentry.parent.moveDown(gentry)
        # Move config entry
        centry = self.__guiEntry.configBuddy
        if centry.parent != None:
            centry.parent.moveDown(centry)

    @property
    def primaryChild(self):
        """Return communicator of primary child in this section."""
        if self.__guiEntry.type != Types.CONTAINER:
            return None
        primaryChild = self.__guiEntry.primaryChild
        if primaryChild != None:
            return primaryChild.proxy
        else:
            return None


class FcGEntry(object):

    """Base class of all client widgets. The client widget classes must be sub-classes of this class"""

    def __init__ (self, communicator):
        self.communicator = communicator
        if self.communicator != None:
            self.communicator.connectClient(self)

    def __del__ (self):
        if self.communicator != None:
            self.communicator.disconnect()

    def processSignal (self, signal, value):
        raise NotImplementedError("Abstract method was not defined!")

