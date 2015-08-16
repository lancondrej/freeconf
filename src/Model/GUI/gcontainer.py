#!/usr/bin/python
#
# base.py
# begin: 2.5.2010 by Jan Ehrenberger
#
# Freeconf base classes
#

from Model.GUI.gentry import GEntry
from Model.constants import Types, Signals
from Model.container import Container
from Model.exception_logging.log import log
from Model.inconsistency import ContainerInconsistency


#### Multiple sections ####
#### GUI Template Classes ####


class FcCGSEntry(GEntry, Container, ContainerInconsistency):
	"""GUI container class"""
	def __init__ (self, config_buddy = None, parent = None):
		GEntry.__init__(self, config_buddy, parent)
		Container.__init__(self)
		ContainerInconsistency.__init__(self)
		self._activeShown = 0
		self._mandatoryShown = 0
		self._sectionShown = 0
		self.empty = None
		self.parent = parent
		self._showAllChildren = False
		if parent is not None and isinstance(parent, FcCGSEntry):
			self._showAllChildren = parent._showAllChildren
		# Primary child reference
		if config_buddy is not None and config_buddy.templateBuddy.multiple:
			if config_buddy.isMultipleEntryContainer():
				# This section is multiple entry container
				self._primaryChildName = None
			else:
				# This section is instance of multiple section
				self._primaryChild = None

	@property
	def type (self):
		return Types.CONTAINER

	@property
	def inconsistent (self):
		return ContainerInconsistency.inconsistent.fget(self)
	
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
			(index, self._primaryChild) = self.find_entry(self.parent._primaryChildName)
		return self._primaryChild

	def append (self, entry):
		"""Reimplementation of append(). Must count inconsistency of newly added entry"""
		super(FcCGSEntry, self).add_entry(entry)
		if entry is not None:
			if entry.inconsistent:
				self.change_inconsistency(True)
	
	def disconnect (self, entry):
		"""Reimplementation of disconnect(). Must count inconsistency of removed entry"""
		result = super(FcCGSEntry, self).disconnect (entry)
		if not result:
			log.error("removing a non-existing child from the children list")
			return 
	
		if entry.inconsistent:
			self.change_inconsistency(False)

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
			self.callWidget(Signals.CHANGE_EMPTINESS, False)
			self.empty = False
			self.parent.changeEmptiness(False)
		elif e == True and (self.empty == False or self.empty == None):
			# Emptiness changed to True
			self.callWidget(Signals.CHANGE_EMPTINESS, True)
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
			if tentry.type == Types.CONTAINER and not tentry.isReference():
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
			if entry.type == Types.CONTAINER:
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
		self.callWidget(Signals.CHANGE_INCONSISTENCY, value)
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
		if centry.type == Types.CONTAINER:
			newEntry = FcCGSEntry(centry, self)
		else:
			newEntry = GEntry(centry, self)
		centry.guiBuddy = newEntry
		self.append(newEntry)
		# Fill new entry
		if centry.type == Types.CONTAINER:
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
			gui_entry = self.find_entry(entry.name)[1]
			#if gui_entry == None:
			log.debug("Appending centry " + entry.name + " to GUI section " + self.name)
			self.appendCEntry(entry)
			#elif gui_entry.type == FcTypes.SECTION:
			#	gui_entry.fill()
		

