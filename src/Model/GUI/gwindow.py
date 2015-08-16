#!/usr/bin/python3
#
from Model.GUI.gentry import GEntry
from Model.constants import Signals
from Model.container import Container
from Model.inconsistency import Inconsistency, ContainerInconsistency


class FcGWindow(GEntry, Container, Inconsistency):
	"""Class that represents the top-level dialogue window"""
	def __init__ (self):
		GEntry.__init__(self)
		Container.__init__(self)
		Inconsistency.__init__(self, False)
		self._minWidth = 0
		self._minHeight = 0
		self._maxWidth = 0
		self._maxHeight = 0
		self.title = "Freeconf generated config dialog"

	@property
	def minHeight(self):
		return self._minHeight

	@minHeight.setter
	def minHeight(self, height):
		self._minHeight = height
		if self._minHeight > self._maxHeight != 0:
			self._maxHeight = self._minHeight

	@property
	def minWidth(self):
		return self._minWidth

	@minWidth.setter
	def minWidth(self, width):
		self._minWidth = width
		if self._minWidth > self._maxWidth != 0:
			self._maxWidth = self._minWidth

	@property
	def maxHeight(self):
		return self._maxHeight

	@maxHeight.setter
	def maxHeight(self, height):
		self._maxHeight = height
		if self._maxHeight < self._minHeight != 0:
			self._minHeight = self._maxHeight

	@property
	def maxWidth(self):
		return self._maxWidth

	@maxWidth.setter
	def maxWidth(self, width):
		self._maxWidth = width
		if self._maxWidth < self._minWidth != 0:
			self._minWidth = self._maxWidth

	@property
	def inconsistent (self):
		return ContainerInconsistency.inconsistent.fget(self)

	def initState (self):
		"""Counts states of all the objects in the GUI tree. Number of active and mandatory keys is stored."""
		for tab in self.entries:
			tab.initState()
			
	def showAll (self, value):
		for tab in self.entries:
			tab.showAll(value)
			
	def notifyParent(self, value):
		self.callWidget(Signals.CHANGE_INCONSISTENCY, value)


