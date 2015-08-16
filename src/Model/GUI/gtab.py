from Model.GUI.gentry import GEntry
from Model.constants import Signals
from Model.inconsistency import Inconsistency


class FcGTab(GEntry, Inconsistency):
	"""GUI tab representation class"""
	def __init__ (self, name = "", label = "", description = "", parent = None):
		GEntry.__init__(self, None, parent)
		Inconsistency.__init__(self, False)
		self.name = name
		self._label = label
		self._empty = None
		self.description = description
		self.icon = "mimetypes/unknown"
		self._content = None

	@property
	def label (self, language=""):
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
		return Inconsistency.inconsistent.fget(self)

	def changeEmptiness (self, value):
		"""Change emptiness of the tab. If the tab is empty a signal is sent to the client and parent is notified"""
		if value == False and (self._empty == True or self._empty == None):
			self._empty = False
			self.callWidget(Signals.CHANGE_EMPTINESS, False)
		elif value == True and (self._empty == False or self._empty == None):
			self._empty = True
			self.callWidget(Signals.CHANGE_EMPTINESS, True)
			
	def notifyParent (self, value):
		"""Notify parent about the change of inconsistency"""
		self.callWidget(Signals.CHANGE_INCONSISTENCY, value)
		if self.parent != None:
			self.parent.changeInconsistency(value)
			
	def showAll (self, value):
		if self.content != None:
			self.content.showAll(value)
