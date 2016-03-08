__author__ = 'Ondřej Lanč'



#### GUI Template Classes ####
class FcCGEntry(object):
	"""Base class for GUI entries"""
	def __init__ (self, configBuddy = None, parent = None):
		self.configBuddy = configBuddy
		# Reference to the communicator that handles communication between the library and the client
		self.__proxy = None
		self.parent = parent
		self._label = ""
		self._name = ""
		self._showAll = False

	@property
	def name (self):
		if self._name != "":
			return self._name
		if self.configBuddy != None:
			return self.configBuddy.name
		else:
			return ""

	@name.setter
	def name (self, name):
		self._name = name
		# implicit fallback to key name
		if self._label == "":
			self._label = name

	@property
	def type (self):
		if self.configBuddy != None:
			return self.configBuddy.type
		return FcTypes.UNKNOWNENTRY

	@property
	def inconsistent (self):
		"""GUI entry is inconsistent if the matching config entry is inconsistent"""
		if self.configBuddy != None:
			return self.configBuddy.inconsistent
		else:
			return None

	@property
	def label (self, language = ""):
		if self.configBuddy != None:
			label = self.configBuddy.templateBuddy.keyLabel(language)
			if label == "":
				return self.configBuddy.templateBuddy.name
			else:
				return label
		return self._label

	@label.setter
	def label (self, label):
		self._label = label


	@property
	def proxy (self):
		"""Returns proxy object of this entry"""
		if self.__proxy == None:
			self.__proxy = FcGUICommunicator(self)
		return self.__proxy

	def callWidget (self, signal, arg):
		"""Sends a signal to the client widget through the client interface"""
		if self.__proxy != None:
			self.__proxy.processSignal(signal, arg)

	def initState (self):
		"""Counts states of all objects in the GUI tree. Number of active and mandatory keys is stored."""
		pass

	def showAll (self, value):
		"""Show all non-mandatory entries when "show advanced" button has been toggled"""
		if self.configBuddy == None or self.configBuddy.templateBuddy.dynamicActive == False: return
		if value == True:
			self.callWidget(FcSignals.CHANGE_SHOW_ALL, True)
		elif value == False and self.configBuddy.templateBuddy.dynamicMandatory == False:
			self.callWidget(FcSignals.CHANGE_SHOW_ALL, False)


class FcCGSEntry(FcCGEntry, FcSEntry, FcSInconsistency):
	"""GUI container class"""
	def __init__ (self, configBuddy = None, parent = None):
		FcCGEntry.__init__(self, configBuddy, parent)
		FcSEntry.__init__(self)
		FcSInconsistency.__init__(self)
		self._activeShown = 0
		self._mandatoryShown = 0
		self._sectionShown = 0
		self.empty = None
		self._showAllChildren = False
		if parent != None and isinstance(parent, FcCGSEntry):
			self._showAllChildren = parent._showAllChildren
		# Primary child reference
		if configBuddy != None and configBuddy.templateBuddy.multiple:
			if configBuddy.isMultipleEntryContainer():
				# This section is multiple entry container
				self._primaryChildName = None
			else:
				# This section is instance of multiple section
				self._primaryChild = None

	@pGroperty
	def type (self):
		return FcTypes.SECTION

	@property
	def inconsistent (self):
		return FcSInconsistency.inconsistent.fget(self)

	@property
	def showAllChildren(self):
		return self._showAllChildren

	@property
	def primaryChildName(self):
		raise AttributeError("Property primaryChildName is write only!")

	@primaryChildName.setter
	def primaryChildName(self, name):
		self._primaryChildName = name
		self._primaryChild = None

	@property
	def primaryChild(self):
		if self.parent == None or self.parent.configBuddy == None or \
		   self.configBuddy == None or not self.configBuddy.templateBuddy.multiple:
			return None
		if self.parent._primaryChildName == None and self._primaryChild == None:
			if len(self._entries) == 0:
				return None
			self._primaryChild = self._entries[0]
		if self._primaryChild == None:
			(index, self._primaryChild) = self.findEntry(self.parent._primaryChildName)
		return self._primaryChild

	def append (self, entry):
		"""Reimplementation of append(). Must count inconsistency of newly added entry"""
		super(FcCGSEntry, self).append(entry)
		if entry != None:
			if entry.inconsistent == True:
				self.changeInconsistency(True)

	def disconnect (self, entry):
		"""Reimplementation of disconnect(). Must count inconsistency of removed entry"""
		result = super(FcCGSEntry, self).disconnect (entry)
		if result == False:
			log.error("removing a non-existing child from the children list")
			return

		if entry.inconsistent == True:
			self.changeInconsistency(False)

	def changeActive (self, value):
		"""Counts active children in the container"""
		if value == True:
			self._activeShown += 1
		else:
			self._activeShown -= 1
		self.evaluateEmptiness()

	def changeMandatory (self, value):
		"""Counts mandatory children in the container"""
		if value == True:
			self._mandatoryShown += 1
		else:
			self._mandatoryShown -= 1
		self.evaluateEmptiness()

	def changeEmptiness (self, value):
		"""Counts empty children in the container"""
		if value == True:
			self._sectionShown -= 1
		else:
			self._sectionShown += 1
		self.evaluateEmptiness()

	def _isEmpty(self):
		"""Evaluates emptiness of the entry."""
		if( # There is section inside, that should be displayed
		    (self._sectionShown > 0) or
		    # OR ShowAllChildren is on. We display all active entries.
		    (self._showAllChildren == True and self._activeShown > 0) or
		    # OR ShowAllChildren is off. We display only mandatory entries.
		    (self._showAllChildren == False and self._activeShown > 0 and self._mandatoryShown > 0)
		  ):
			return False
		# TODO: Je tady nasledujici podminka vubec potreba? Nestacilo by else?
		elif (self._mandatoryShown == 0 and self._sectionShown == 0) or \
		     (self._activeShown == 0 and self._sectionShown == 0):
			return True
		return None

	def evaluateEmptiness (self):
		"""Evaluates emptiness of the entry. If the entry is empty a signal is sent to the client and parent is notified"""
		# Evaluate emptiness
		e = self._isEmpty()
		if e == False and (self.empty == True or self.empty == None):
			# Emptiness changed to False
			self.callWidget(FcSignals.CHANGE_EMPTINESS, False)
			self.empty = False
			self.parent.changeEmptiness(False)
		elif e == True and (self.empty == False or self.empty == None):
			# Emptiness changed to True
			self.callWidget(FcSignals.CHANGE_EMPTINESS, True)
			self.empty = True
			self.parent.changeEmptiness(True)

	def _initMultipleContainerState(self):
		"""Special init method for multiple section containers. We have to initialize number of active
		   and mandatory keys from template tree, because GUI objects might not exist yet."""
		if len(self.entries) > 0:
			# If multiple section container is not empty, it will behave as normal section.
			self.initState()
			return

		# Multiple section container is empty.
		# Recursively browse template tree to count active and mandatory keys.
		def browseTemplateTree(tentry):
			if tentry.type == FcTypes.SECTION and not tentry.isReference():
				for e in tentry.entries:
					browseTemplateTree(e)
			elif tentry.dynamicActive == True:
				self._activeShown += 1
			elif tentry.dynamicMandatory == True:
				self._mandatoryShown += 1
		browseTemplateTree(self.configBuddy.templateBuddy)
		self.evaluateEmptiness()

	def initState (self):
		"""Counts states of all objects in the GUI tree. Number of active and mandatory keys is stored."""
		needEvaluation = False
		for entry in self._entries:
			if entry.type == FcTypes.SECTION:
				self._sectionShown += 1
				if entry.configBuddy and entry.configBuddy.isMultipleEntryContainer():
					entry._initMultipleContainerState()
				else:
					entry.initState()
			else:
				needEvaluation = True
				if entry.configBuddy != None:
					if entry.configBuddy.templateBuddy.dynamicActive == True:
						self._activeShown += 1
					if entry.configBuddy.templateBuddy.dynamicMandatory == True:
						self._mandatoryShown += 1
		if needEvaluation == True:
			self.evaluateEmptiness()

	def notifyParent (self, value):
		"""Notifies parent about the change of inconsistency"""
		self.callWidget(FcSignals.CHANGE_INCONSISTENCY, value)
		if self.parent != None:
			self.parent.changeInconsistency(value)

	def showAll (self, value):
		"""Shows all entries if the "show advanced" button has been toggled"""
		self._showAllChildren = value
		for entry in self._entries:
			entry.showAll(value)
		self.evaluateEmptiness()

	def appendCEntry(self, centry):
		"""Create GUI entry for given config entry and append it to GUI tree."""
		newEntry = None
		if centry.type == FcTypes.SECTION:
			newEntry = FcCGSEntry(centry, self)
		else:
			newEntry = FcCGEntry(centry, self)
		centry.guiBuddy = newEntry
		self.append(newEntry)
		# Fill new entry
		if centry.type == FcTypes.SECTION:
			newEntry.fill()
		return newEntry

	def fill (self, centry = None):
		"""Fill section with config entries."""
		log.debug("Filling GUI section " + self.name)

		if centry != None:
			# Set config entry if specified
			if self.configBuddy != None:
				# Remove link to old config buddy
				self.configBuddy.guiBuddy = None
			self.configBuddy = centry
			centry.guiBuddy = self

		if self.configBuddy == None:
			return None

		log.debug("Config buddy: " + str(self.configBuddy))
		log.debug("Filling with config buddy entries: " + str(self.configBuddy.entries))

		# Fill section
		for entry in self.configBuddy.entries:
			gui_entry = self.findEntry(entry.name)[1]
			#if gui_entry == None:
			log.debug("Appending centry " + entry.name + " to GUI section " + self.name)
			self.appendCEntry(entry)
			#elif gui_entry.type == FcTypes.SECTION:
			#	gui_entry.fill()


class FcGWindow(FcCGEntry, FcSEntry, FcSInconsistency):
	"""Class that represents the top-level dialogue window"""
	def __init__ (self):
		FcCGEntry.__init__(self)
		FcSEntry.__init__(self)
		FcSInconsistency.__init__(self)
		self._minWidth = 0
		self._minHeight = 0
		self._maxWidth = 0
		self._maxHeight = 0
		self.title = "Freeconf generated config dialog"

	@property
	def minHeight (self):
		return self._minHeight

	@minHeight.setter
	def minHeight (self, height):
		self._minHeight = height
		if self._minHeight > self._maxHeight and self._maxHeight != 0:
			self._maxHeight = self._minHeight

	@property
	def minWidth (self):
		return self._minWidth

	@minWidth.setter
	def minWidth (self, width):
		self._minWidth = width
		if self._minWidth > self._maxWidth and self._maxWidth != 0:
			self._maxWidth = self._minWidth

	@property
	def maxHeight (self):
		return self._maxHeight

	@maxHeight.setter
	def maxHeight (self, height):
		self._maxHeight = height
		if self._maxHeight < self._minHeight and self._minHeight != 0:
			self._minHeight = self._maxHeight

	@property
	def maxWidth (self):
		return self._maxWidth

	@maxWidth.setter
	def maxWidth (self, width):
		self._maxWidth = width
		if self._maxWidth < self._minWidth and self._minWidth != 0:
			self._minWidth = self._maxWidth

	@property
	def inconsistent (self):
		return FcSInconsistency.inconsistent.fget(self)

	def initState (self):
		"""Counts states of all the objects in the GUI tree. Number of active and mandatory keys is stored."""
		for tab in self.entries:
			tab.initState()

	def showAll (self, value):
		for tab in self.entries:
			tab.showAll(value)

	def notifyParent(self, value):
		self.callWidget(FcSignals.CHANGE_INCONSISTENCY, value)


class FcGTab(FcCGEntry, FcInconsistency):
	"""GUI tab representation class"""
	def __init__ (self, name = "", label = "", description = "", parent = None):
		FcCGEntry.__init__(self, None, parent)
		FcInconsistency.__init__(self, False)
		self.name = name
		self._label = label
		self._empty = None
		self.description = description
		self.icon = "mimetypes/unknown"
		self._content = None

	@property
	def label (self):
		if not self._label:
			return self.name
		return self._label

	@label.setter
	def label (self, label):
		self._label = label

	@property
	def content (self):
		return self._content

	@content.setter
	def content (self, content):
		if self._content == content: return
		if self._content != None:
			self._content.parent = None
		self._content = content
		self._content.parent = self

	def initState (self):
		"""Counts states of all objects in the GUI tree. Number of active and mandatory keys is stored."""
		if self.content != None:
			self.content.initState()

	@property
	def empty (self):
		return self._empty

	@property
	def inconsistent (self):
		return FcInconsistency.inconsistent.fget(self)

	def changeEmptiness (self, value):
		"""Change emptiness of the tab. If the tab is empty a signal is sent to the client and parent is notified"""
		if value == False and (self._empty == True or self._empty == None):
			self._empty = False
			self.callWidget(FcSignals.CHANGE_EMPTINESS, False)
		elif value == True and (self._empty == False or self._empty == None):
			self._empty = True
			self.callWidget(FcSignals.CHANGE_EMPTINESS, True)

	def notifyParent (self, value):
		"""Notify parent about the change of inconsistency"""
		self.callWidget(FcSignals.CHANGE_INCONSISTENCY, value)
		if self.parent != None:
			self.parent.changeInconsistency(value)

	def showAll (self, value):
		if self.content != None:
			self.content.showAll(value)
