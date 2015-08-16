#!/usr/bin/python3
#

# from Controller.client_interface import FcGUICommunicator
from Model.constants import Types, Signals


class GEntry(object):
	"""Base class for GUI entries"""
	def __init__(self, config_buddy=None, parent=None):
		self.configBuddy = config_buddy
		# Reference to the communicator that handles communication between the library and the client
		self.__proxy = None
		self.parent = parent
		self._label = ""
		self._name = ""
		self._showAll = False

	@property
	def name(self):
		if self._name != "":
			return self._name
		if self.configBuddy is not None:
			return self.configBuddy.name
		else:
			return ""

	@name.setter
	def name(self, name):
		self._name = name
		# implicit fallback to key name
		if self._label == "":
			self._label = name

	@property
	def type (self):
		if self.configBuddy is not None:
			return self.configBuddy.type
		return Types.UNKNOWN_ENTRY
		
	@property
	def inconsistent (self):
		"""GUI entry is inconsistent if the matching config entry is inconsistent"""
		if self.configBuddy is not None:
			return self.configBuddy.inconsistent
		else:
			return None

	@property
	def label (self, language=""):
		if self.configBuddy is not None:
			label = self.configBuddy.templateBuddy.keyLabel(language)
			if label == "":
				return self.configBuddy.templateBuddy.name
			else:
				return label
		return self._label

	@label.setter
	def label (self, label):
		self._label = label


	# @property
	# def proxy (self):
	# 	"""Returns proxy object of this entry"""
	# 	if self.__proxy is None:
	# 		self.__proxy = FcGUICommunicator(self)
	# 	return self.__proxy

	def callWidget(self, signal, arg):
		"""Sends a signal to the client widget through the client interface"""
		if self.__proxy is not None:
			self.__proxy.processSignal(signal, arg)
			
	def initState(self):
		"""Counts states of all objects in the GUI tree. Number of active and mandatory keys is stored."""
		pass
	
	def showAll(self, value):
		"""Show all non-mandatory entries when "show advanced" button has been toggled"""
		if self.configBuddy is None or not self.configBuddy.templateBuddy.dynamicActive: return
		if value:
			self.callWidget(Signals.CHANGE_SHOW_ALL, True)
		elif value == False and self.configBuddy.templateBuddy.dynamicMandatory == False:
			self.callWidget(Signals.CHANGE_SHOW_ALL, False)


