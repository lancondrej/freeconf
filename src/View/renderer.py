#!/usr/bin/python

from View.qtwidgets import *
from View.form import Ui_main
from View.exception_logging.log import log


class GuiHandler (QtGui.QWidget):

	def __init__ (self, package):
		QtGui.QWidget.__init__(self, None)
		self.ui = Ui_main()
		self.ui.setupUi(self)
		desktop = QtGui.QDesktopWidget()
		self.setGeometry(desktop.width()/2 - self.width()/2, desktop.height()/2 - self.height()/2, self.width(), self.height());
		self.package = package
		self.iconSet = ""

		self.setIconTheme()

		self.setWindowTitle(self.package.window.title);
		if self.package.window.minWidth != 0:
			self.setMinimumWidth(self.package.window.minWidth)
		if self.package.window.minHeight != 0:
			self.setMinimumHeight(self.package.window.minHeight)
		if self.package.window.maxWidth != 0:
			self.setMaximumWidth(self.package.window.maxWidth)
		if self.package.window.maxHeight != 0:
			self.setMaximumHeight(self.package.window.maxHeight)
		
		self.window = QtGWindow(self.package.window, self.ui.okButton, self.ui.applyButton, \
		self.ui.iconView, self.ui.tabLabel, self.ui.contentLayout)
		self.window.render()

	def ok (self):
		#self.package.save_configuration()
		QtGui.qApp.quit()

	def apply (self):
		#self.package.save_configuration()
		pass

	def cancel (self):
		QtGui.qApp.quit()
		
	def toggleAdvanced (self, state):
		self.package.showAllActiveWidgets(state)
		self.window.toggleAdvanced()
		if state == True:
			self.ui.advancedButton.setText(self.tr("&Hide advanced"))
		else:
			self.ui.advancedButton.setText(self.tr("&Show advanced"))
		self.ui.iconView.scrollToItem(self.ui.iconView.currentItem(), QtGui.QAbstractItemView.EnsureVisible)

	def tabChanged (self, current, previous):
		if previous != None:
			self.window.changeTab(self.ui.iconView.row(previous), self.ui.iconView.row(current))
		else:
			self.window.changeTab(-1, self.ui.iconView.row(current))
		self.ui.scrollArea.repaint()

	def testIconTheme(self):
		"""Tests if current icon theme has needed icons."""
		# Test against list-add icon
		res =  QtGui.QIcon.hasThemeIcon('list-add')
		return res
	
	def setIconTheme(self):
		"""Find usable icon theme and set it. This function should be called before gui will be created."""
		if not self.testIconTheme():
			# Current icon theme is not ok, try another theme
			QtGui.QIcon.setThemeName("oxygen")
			log.info("Icon theme changed to oxygen.")
		if not self.testIconTheme():
			# Current icon theme is not ok, try another theme
			QtGui.QIcon.setThemeName("default")
			log.info("Icon theme changed to default.")

