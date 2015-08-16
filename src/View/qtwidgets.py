#!/usr/bin/python

from PyQt4 import QtGui, QtCore
from Controller.client_interface import *
from Model.constants import Signals, Types, escapeXML
from View.exception_logging.log import log
from View.exception_logging.exception import FcGeneralError


class QtCEntry(QtCore.QObject, FcGEntry):
    """Base class for config widgets"""
    def __init__ (self, communicator, parent, activePos):
        QtCore.QObject.__init__(self, None)
        FcGEntry.__init__(self, communicator)
        self.parent = parent
        self.rendered = False
        self.widget = None
        self.activePos = activePos

    def beginRender(self):
        """This method is called before the widget is rendered"""
        if self.parent is None or self.parent.layout is None:
            log.error("Widget's parent and layout must be set before render. parent=%s, class=%s, name=%s" %
                      (str(self.parent), str(self), self.communicator.name))

    def endRender(self):
        """This method is called after rendering of the widget has been finished"""
        if self.widget == None: return
        self.checkMandatory(self.communicator.mandatory)
        self.checkEnabled(self.communicator.enabled)
        self.checkInconsistency(self.communicator.inconsistent)

    def render(self):
        """This method renders the widget"""
        self.beginRender()
        #Render widget only if it is active or a section
        if self.communicator.active == True or self.communicator.type == Types.SECTION:
            self.createGUI()
        self.endRender()

    def checkMandatory (self, mandatory):
        """Checks mandatority and alters the widget accordingly"""
        if self.widget == None: return
        label = self.parent.layout.labelForField(self.widget)
        if mandatory == False and self.parent.communicator.showAllChildren == False:
            self.widget.setVisible(False)
            if label != None:
                label.setVisible(False)
        else:
            self.widget.setVisible(True)
            if label != None:
                label.setVisible(True)

    def checkInconsistency (self, inconsistent):
        """Checks inconsistency and alters the widget accordingly"""
        if self.widget == None: return
        label = self.parent.layout.labelForField(self.widget)
        if inconsistent == True:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 86, 106))
            brush.setStyle(QtCore.Qt.SolidPattern)
            #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            palette.setBrush(QtGui.QPalette.WindowText, brush)
            if label != None:
                label.setPalette(palette)
            else:
                self.widget.setPalette(palette)
            font = QtGui.QFont()
            font.setWeight(75)
            font.setBold(True)
            if label != None:
                label.setFont(font)
            else:
                self.widget.setFont(font)
        else:
            if label != None:
                label.setPalette(QtGui.QApplication.palette(label))
                label.setFont(QtGui.QApplication.font(label))
            else:
                self.widget.setPalette(QtGui.QApplication.palette(self.widget))
                self.widget.setFont(QtGui.QApplication.font(self.widget))

    def checkEnabled (self, enabled):
        """Checks enable/disable state and alters the widget accordingly"""
        if self.widget == None: return
        label = self.parent.layout.labelForField(self.widget)
        if label != None:
            label.setEnabled(enabled)
        self.widget.setEnabled(enabled)

    def createGUI (self):
        """This method must create all visual elements that form the widget. Must be implemented in sub-classes"""
        raise NotImplementedError("It is an abstract method")

    def destroyGUI (self, disconnect = False):
        """Destroys all visual elements that form the widget"""
        if self.widget != None:
            label = self.parent.layout.labelForField(self.widget)
            if label != None:
                label.deleteLater()
            widget = self.parent.layout.takeAt(self.parent.layout.indexOf(self.widget))
            self.widget.deleteLater()
        self.widget = None
        if self.parent.layout != None:
            self.parent.layout.update()
        if disconnect == True:
            self.communicator.disconnect()

    def processSignal(self, signal, value):
        """Handles signals from the library"""
        if self.widget != None:
            label = self.parent.layout.labelForField(self.widget)
        if signal == Signals.CHANGE_ENABLED:
            self.checkEnabled(value)
        elif signal == Signals.CHANGE_ACTIVE:
            if value == True:
                if self.widget == None:
                    self.render()
            else:
                self.destroyGUI()
        elif signal == Signals.CHANGE_MANDATORY:
            self.checkMandatory(value)
        elif signal == Signals.CHANGE_SHOW_ALL:
            if self.widget != None:
                self.widget.setVisible(value)
                if label != None:
                    label.setVisible(value)
        elif signal == Signals.CHANGE_INCONSISTENCY:
            self.checkInconsistency(value)


class QtCSEntry(QtCEntry):
    """This class represents a group-box section"""
    def __init__ (self, communicator, parent, activePos):
        QtCEntry.__init__(self, communicator, parent, activePos)
        self.frameLess = False
        self.layout = None
        self.fillChildren()

    def fillChildren (self):
        """Process all children of the widget and form the widget tree"""
        self.children = []
        position = 0
        if self.communicator != None:
            newEntry = None
            for entry in self.communicator.children:
                log.debug("Building GUI for "+entry.name)
                if entry.type == Types.SECTION:
                    if entry.multiple:
                        if entry.isMultipleEntryContainer:
                            newEntry = QtMCContainer(entry, self, position)
                        else:
                            newEntry = QtMCSEntry(entry, self, position)
                    else:
                        newEntry = QtCSEntry(entry, self, position)
                elif entry.type == Types.FUZZY:
                    newEntry = QtCKFuzzy(entry, self, position)
                elif entry.type == Types.BOOL:
                    newEntry = QtCKBool(entry, self, position)
                elif entry.type == Types.NUMBER:
                    newEntry = QtCKNumber(entry, self, position)
                elif entry.type == Types.STRING:
                    newEntry = QtCKString(entry, self, position)
                else:
                    log.warning("Unknown config node %d" % (entry.type))
                if newEntry != None:
                    position += 1
                    self.children.append(newEntry)

    def destroyGUI (self, disconnect = False):
        """Destroy all children and itself"""
        log.debug("Destroying gui for " + str(self.communicator.name))
        for child in self.children:
            child.destroyGUI(disconnect)
        if self.widget != None:
            self.widget.deleteLater()
            self.widget = None
        if self.layout != None:
            self.layout.deleteLater()
            self.layout = None
        if disconnect == True:
            self.communicator.disconnect()

    def disconnect(self, entry):
        """Remove child."""
        try:
            self.children.remove(entry)
            entry.parent = None
            return True
        except ValueError or KeyError:
            return False


    def createGUI (self):
        """Creates either a border-less or a border representation of the group"""
        self.layout = QtGui.QFormLayout()
        self.layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.layout.setWidget(len(self.children) - 1, QtGui.QFormLayout.SpanningRole, None)

        ## Normal section
        if self.frameLess:
            self.layout.setContentsMargins(0, 0, 0, 4)
            self.widget = QtGui.QFrame()
            self.widget.setFrameShape(QtGui.QFrame.NoFrame)
            self.widget.setFrameShadow(QtGui.QFrame.Plain)
            self.widget.setLayout(self.layout)
        else:
            self.widget = QtGui.QGroupBox(self.communicator.label)
            self.widget.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
            self.widget.setLayout(self.layout)
        self.parent.layout.setWidget(self.activePos, QtGui.QFormLayout.SpanningRole, self.widget)

        self.renderChildren()

    def endRender(self):
        """Sets visual hints for visibility and inconsistency"""
        self.widget.setVisible(not self.communicator.empty)
        self.checkInconsistency(self.communicator.inconsistent)

    def checkInconsistency (self, inconsistent):
        """Checks inconsistency and draws the group-box red if needed"""
        if inconsistent == True:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(235, 100, 100))
            brush.setStyle(QtCore.Qt.SolidPattern)
            #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
            palette.setBrush(QtGui.QPalette.Window, brush)
            self.widget.setPalette(palette)
        else:
            self.widget.setPalette(QtGui.QApplication.palette(self.widget))

    def renderChildren (self):
        """Renders all children"""
        for entry in self.children:
            entry.render()

    def processSignal(self, signal, value):
        """Handles signals from the library"""
        if signal == Signals.CHANGE_EMPTINESS:
            if self.widget != None:
                self.widget.setVisible(not value)
        if signal == Signals.CHANGE_INCONSISTENCY:
            self.checkInconsistency(value)

class QtMCContainer(QtCSEntry):
    """This class represents list of multiple entries."""


    class ListItem(QtGui.QListWidgetItem):
        """Item for list of multiple entries."""
        def __init__(self, qtEntry):
            QtGui.QListWidgetItem.__init__(self)
            self.entry = qtEntry
            self.entry.listItem = self # Connect Qt Entry to list item
            primaryChild = self.entry.communicator.primaryChild
            if primaryChild != None and primaryChild.value != None:
                self.setText(str(primaryChild.valueRepr))
            else:
                self.setText(self.entry.communicator.name)

            # Store original background color
            self.__originalBackground = self.background()
            self.checkInconsistency(self.entry.communicator.inconsistent)

        def checkInconsistency (self, inconsistent):
            """Checks inconsistency and draws the group-box red if needed"""
            if inconsistent == True:
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(235, 150, 150))
                brush.setStyle(QtCore.Qt.SolidPattern)
                self.setBackground(brush)
            else:
                self.setBackground(self.__originalBackground)


    def __init__ (self, communicator, parent, activePos):
        QtCSEntry.__init__(self, communicator, parent, activePos)
        self.list_widget = None

    def createGUI(self):
        # Frame
        container = QtGui.QGroupBox(self.communicator.label)
        container.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        hbox_layout = QtGui.QHBoxLayout()
        container.setLayout(hbox_layout)
        self.widget = container
        self.parent.layout.setWidget(self.activePos, QtGui.QFormLayout.SpanningRole, container)

        # List View
        self.list_widget = QtGui.QListWidget()
        self.list_widget.itemActivated.connect(self.itemActivated)
        hbox_layout.addWidget(self.list_widget)

        # Layout for buttons
        vbox_layout = QtGui.QVBoxLayout()
        hbox_layout.addLayout(vbox_layout)

        # Add button
        addButton = QtGui.QPushButton("Add Entry")
        addButton.setIcon(QtGui.QIcon.fromTheme("list-add"))
        self.connect(addButton, QtCore.SIGNAL("clicked()"), self.addEntry)
        vbox_layout.addWidget(addButton)

        # Remove Button
        removeButton = QtGui.QPushButton("Remove Entry")
        removeButton.setIcon(QtGui.QIcon.fromTheme("list-remove"))
        self.connect(removeButton, QtCore.SIGNAL("clicked()"), self.removeEntry)
        vbox_layout.addWidget(removeButton)

        # Up button
        upButton = QtGui.QPushButton("Move Up")
        upButton.setIcon(QtGui.QIcon.fromTheme("go-up"))
        self.connect(upButton, QtCore.SIGNAL("clicked()"), self.moveUp)
        vbox_layout.addWidget(upButton)

        # Down button
        downButton = QtGui.QPushButton("Move Down")
        downButton.setIcon(QtGui.QIcon.fromTheme("go-down"))
        self.connect(downButton, QtCore.SIGNAL("clicked()"), self.moveDown)
        vbox_layout.addWidget(downButton)

        vbox_layout.addStretch()

        # Fill list with multiple entries
        self.fillList()

        # Create dummy layout
        self.layout = QtGui.QFormLayout()

    def fillList(self):
        ## Refill List View
        self.list_widget.clear()
        for entry in self.children:
            self.list_widget.addItem(self.ListItem(entry))

    def addEntry(self):
        new_comm = self.communicator.createEntry()
        if new_comm.type == Types.SECTION:
            new_entry = QtMCSEntry(new_comm, self, len(self.children))
            self.children.append(new_entry)
            self.list_widget.addItem(self.ListItem(new_entry))
        else:
            raise FcGeneralError("Multiple entries are not supported yet. Use multiple section instead.")

    def removeEntry(self):
        # Get active item
        item = self.list_widget.currentItem()
        if item == None:
            return # No item selected

        entry = item.entry
        entry.communicator.deleteNode()
        #entry.destroyGUI()
        self.disconnect(entry)
        self.list_widget.takeItem(self.list_widget.row(item))

    def moveUp(self):
        # Get active item
        row = self.list_widget.currentRow()
        if row == -1:
            return # No item selected
        if row == 0:
            return # Nowhere to move
        item = self.list_widget.item(row)

        # Tell FC library that we move the item
        entry = item.entry
        entry.communicator.moveUp()

        # Move item in GUI
        self.list_widget.takeItem(row)
        self.list_widget.insertItem(row - 1, item)
        self.list_widget.setCurrentRow(row - 1)

    def moveDown(self):
        # Get active item
        row = self.list_widget.currentRow()
        if row == -1:
            return # No item selected
        if row == self.list_widget.count() - 1:
            return # Nowhere to move
        item = self.list_widget.item(row)

        # Tell FC library that we move the item
        entry = item.entry
        entry.communicator.moveDown()

        # Move item in GUI
        row = self.list_widget.row(item)
        self.list_widget.takeItem(row)
        self.list_widget.insertItem(row + 1, item)
        self.list_widget.setCurrentRow(row + 1)

    def itemActivated(self, item):
        if item.entry.communicator.empty:
            # Display warning instead of empty dialog window.
            win = QtGui.QApplication.activeWindow()
            msgBox = QtGui.QMessageBox(win)
            msgBox.setText("Section %s is empty!" % (item.entry.communicator.name,))
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            # Set geometry of the dialog to center of parent window. This should be automatic,
            # I don't know why it does not work without this code :/
            rect = msgBox.geometry()
            rect.moveCenter(win.geometry().center())
            msgBox.setGeometry(rect)

            msgBox.exec_()
        else:
            item.entry.render()


class QtMCSEntry(QtCSEntry):
    """Visualization of multiple config section entry."""

    def __init__ (self, communicator, parent, activePos):
        QtCSEntry.__init__(self, communicator, parent, activePos)
        self.listItem = None

    def createGUI(self):
        if self.widget != None:
            return

        ## Create dialog
        win = QtGui.QApplication.activeWindow()
        self.widget = QtGui.QDialog(win)
        # Set geometry of the dialog to center of parent window. This should be automatic,
        # I don't know why it does not work without this code :/
        rect = self.widget.geometry()
        rect.moveCenter(win.geometry().center())
        self.widget.setGeometry(rect)

        self.widget.setModal(False)
        self.widget.setWindowTitle(self.communicator.name)
        self.widget.finished.connect(self.dialogClosed)

        vbox_layout = QtGui.QVBoxLayout()
        self.widget.setLayout(vbox_layout)

        # Main Layout
        self.layout = QtGui.QFormLayout()
        self.layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.layout.setWidget(len(self.children) - 1, QtGui.QFormLayout.SpanningRole, None)
        vbox_layout.addLayout(self.layout)

        vbox_layout.addStretch()

        # Add Line
        line = QtGui.QFrame()
        line.setMinimumSize(QtCore.QSize(0, 2))
        line.setMaximumSize(QtCore.QSize(16777215, 2))
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        vbox_layout.addWidget(line)

        ## Dialog buttons
        button_layout = QtGui.QHBoxLayout()

        ## Advanced button
        #advancedButton = QtGui.QPushButton(QtGui.QApplication.translate("main", "&Show advanced", None, QtGui.QApplication.UnicodeUTF8))
        #button_layout.addWidget(advancedButton)

        button_layout.addStretch()
        # Close dialog button
        closeButton = QtGui.QPushButton("&Close")
        closeButton.setIcon(QtGui.QIcon.fromTheme("dialog-ok"))
        closeButton.clicked.connect(self.widget.accept)
        button_layout.addWidget(closeButton)
        vbox_layout.addLayout(button_layout)

        self.renderChildren()

    def dialogClosed(self, code = 0):
        self.destroyGUI()

    def checkInconsistency (self, inconsistent):
        """Checks inconsistency and sets dialog title if needed."""
        hint_text = " [inconsistent]"
        if inconsistent == True:
            title = self.widget.windowTitle()
            if hint_text not in title:
                title = title + hint_text
                self.widget.setWindowTitle(title)
        else:
            title = self.widget.windowTitle()
            if hint_text in title:
                title = title.replace(hint_text, "")
                self.widget.setWindowTitle(title)
        if self.listItem != None:
            self.listItem.checkInconsistency(inconsistent)


class QtCSRootEntry(object):
    """This class represents a special top-level section"""
    def __init__ (self, communicator, rootLayout):
        self.layout = rootLayout
        self.layout.setSpacing(0)
        self.rootSection = QtCSEntry(communicator.content, self, 0)

    def destroyGUI (self):
        """Destroy all children and itself"""
        self.rootSection.destroyGUI(True)
        self.rootSection = None
        for i in range(self.layout.count()):
            self.layout.takeAt(0)

    def render (self):
        """This method renders all children of the widget"""
        if self.layout == None or self.rootSection == None:
            log.error("Root section and layout must be set before render")
            return
        self.rootSection.frameLess = True
        self.rootSection.render()


class QtCKBool(QtCEntry):
    """This class represents a check-box"""
    def __init__ (self, communicator, parent, activePos):
        QtCEntry.__init__(self, communicator, parent, activePos)

    def createGUI (self):
        if self.widget == None:
            self.widget = QtGui.QCheckBox()
        self.widget.setText(self.communicator.label)
        self.widget.setToolTip("<qt>" + escapeXML(self.communicator.help) + "</qt>")
        self.parent.layout.setWidget(self.activePos, QtGui.QFormLayout.SpanningRole, self.widget)

        if self.communicator.value == None:
            self.widget.setTristate(True)
            self.widget.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            if self.communicator.value == True:
                self.widget.setChecked(QtCore.Qt.Checked)
            else:
                self.widget.setChecked(QtCore.Qt.Unchecked)

        self.rendered = True
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL("stateChanged(int)"), self.stateChanged)

    def stateChanged (self, state):
        if state != QtCore.Qt.PartiallyChecked:
            self.widget.setTristate(False)
        else: return
        if state == QtCore.Qt.Checked:
            self.communicator.value = True
        else:
            self.communicator.value = False


class QtCKNumber(QtCEntry):
    """This class represents a spin-box"""
    def __init__ (self, communicator, parent, activePos):
        QtCEntry.__init__(self, communicator, parent, activePos)
        self.notSet = False

    def createGUI (self):
        label = QtGui.QLabel(self.communicator.label)
        if self.widget == None:
            self.widget = QtGui.QDoubleSpinBox()
        self.widget.setRange(self.communicator.min, self.communicator.max)
        self.widget.setSingleStep(self.communicator.step)
        self.widget.setDecimals(self.communicator.precision)
        if self.communicator.value == None:
            self.widget.setMinimum(self.communicator.min - self.communicator.step)
            self.widget.setValue(self.widget.minimum())
            self.widget.setSpecialValueText(self.tr("value not set"))
            self.notSet = True
        else:
            self.widget.setValue(self.communicator.value)

        label.setToolTip("<qt>" + escapeXML(self.communicator.help) + "</qt>")

        self.parent.layout.setWidget(self.activePos, QtGui.QFormLayout.LabelRole, label)
        self.parent.layout.setWidget(self.activePos, QtGui.QFormLayout.FieldRole, self.widget)

        self.rendered = True
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)

    def valueChanged(self, value):
        if self.notSet == True and value != self.widget.minimum():
            self.notSet = False
            self.widget.setMinimum(self.widget.minimum() + self.communicator.step)
            self.widget.setSpecialValueText("")
        elif self.notSet == True and value == self.widget.minimum(): return
        self.communicator.value = value


class QtCKString(QtCEntry):
    """This class represents either a line-edit or a combo-box"""
    def __init__ (self, communicator, parent, activePos):
        QtCEntry.__init__(self, communicator, parent, activePos)
        self.dropDown = False
        self.chooseOnePresent = False

    def createGUI (self):
        label = QtGui.QLabel(self.communicator.label)
        label.setToolTip("<qt>" + escapeXML(self.communicator.help) + "</qt>")

        self.dropDown = (self.communicator.list != None)

        if self.dropDown == True:
            if self.widget == None:
                self.widget = QtGui.QComboBox()
            i = 0
            if self.communicator.value == None:
                self.chooseOnePresent = True
                self.widget.addItem(self.tr("--choose one--"))
            for entry in self.communicator.list.entries:
                if entry.label != "":
                    self.widget.addItem(entry.label)
                else:
                    self.widget.addItem(entry.value)

                if entry.help != "":
                    self.widget.setItemData(i, entry.help, QtCore.Qt.ToolTipRole)
                if self.communicator.value != None and entry.value == self.communicator.value:
                    self.widget.setCurrentIndex(i)
                i = i + 1

            if self.communicator.value != None:
                self.widget.setEditText(self.communicator.value)
            QtCore.QObject.connect(self.widget, QtCore.SIGNAL("editTextChanged(const QString&)"), self.textChanged)
            QtCore.QObject.connect(self.widget, QtCore.SIGNAL("currentIndexChanged(int)"), self.indexChanged)
        else:
            if self.widget == None:
                self.widget = QtGui.QLineEdit()
            if self.communicator.value != None:
                self.widget.setText(self.communicator.value)
            else:
                #self.widget.setPlaceholderText(self.tr("no value set"))
                self.widget.setText(self.tr("no value set"))
            QtCore.QObject.connect(self.widget, QtCore.SIGNAL("textChanged(const QString&)"), self.textChanged)

        self.rendered = True
        self.parent.layout.setWidget(self.activePos, QtGui.QFormLayout.LabelRole, label)
        self.parent.layout.setWidget(self.activePos, QtGui.QFormLayout.FieldRole, self.widget)

    def textChanged (self, text):
        self.communicator.value = str(text)
        #self.widget.setPlaceholderText("")

    def indexChanged (self, index):
        if self.chooseOnePresent == True and index == 0: return
        self.communicator.value = str(self.widget.itemText(index))
        if self.chooseOnePresent == True:
            #this stops the chain calling of removeItem()
            #removeItem() invokes the indexChanged() slot
            self.chooseOnePresent = False
            self.widget.removeItem(0)


class QtCKFuzzy (QtCKString):
    """This class represents a combo-box"""
    def __init__ (self, communicator, parent, activePos):
        QtCKString.__init__(self, communicator, parent, activePos)


class QtGTab (FcGEntry):
    """This class represents a tab"""
    def __init__ (self, communicator, iconList, tabLabel, layout):
        FcGEntry.__init__(self, communicator)
        self.widget = None
        self.iconList = iconList
        self.tabLabel = tabLabel
        self.layout = layout
        self.rootEntry = None
        self.current = False

    def createGUI (self):
        """Creates the tab's icon and puts it into the icon list"""
        self.widget = QtGui.QListWidgetItem(self.iconList)
        self.widget.setSizeHint(QtCore.QSize(122, 70))
        self.widget.setIcon(self.__loadIcon(self.communicator.icon))
        self.widget.setText(self.communicator.label)
        self.widget.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.widget.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def render (self):
        """Renders the widget"""
        self.createGUI()
        self.endRender()

    def endRender (self):
        """Check emptiness and inconsistency and sets the visual hints accordingly"""
        if self.communicator.empty == True:
            self.widget.setHidden(True)
        self.checkInconsistency(self.communicator.inconsistent)

    def checkInconsistency (self, inconsistent):
        """Checks inconsistency and draws the tab with red gradient background if needed"""
        if inconsistent == True:
            grad = QtGui.QRadialGradient(66, 37, 70)
            grad.setColorAt(0.0, QtGui.QColor(255, 255, 255))
            grad.setColorAt(1.0, QtGui.QColor(255, 100, 100))
            self.widget.setBackground(QtGui.QBrush(grad))
        else:
            self.widget.setBackground(QtGui.QListWidgetItem().background())


    def __loadIcon (self, icon):
        icon = QtGui.QIcon.fromTheme(icon.split('/')[1])
        if icon.isNull():
            icon = QtGui.QIcon.fromTheme("unknown")
        return icon

    @property
    def empty (self):
        return self.communicator.empty

    def activateTab (self):
        """The tab has been selected by the user and its content must be drawn"""
        if self.communicator.empty == True or self.current == True: return
        self.tabLabel.setText(self.communicator.description)
        self.rootEntry = QtCSRootEntry(self.communicator, self.layout)
        self.rootEntry.render()
        self.current = True

    def deactivateTab (self):
        """The tab has been deselected by the user and its content must be destroyed"""
        if self.current == False: return
        self.rootEntry.destroyGUI()
        self.rootEntry = None
        self.tabLabel.setText("")
        self.current = False

    def processSignal (self, signal, value):
        """Handles signals from the library"""
        if signal == Signals.CHANGE_EMPTINESS:
            self.widget.setHidden(value)
        if signal == Signals.CHANGE_INCONSISTENCY:
            self.checkInconsistency(value)


class QtGWindow (QtCore.QObject, FcGEntry):
    """This class represents the top-level dialogue window"""
    def __init__ (self, communicator, ok, apply, iconList, tabLabel, contentLayout):
        QtCore.QObject.__init__(self, None)
        FcGEntry.__init__(self, communicator)
        self.ok = ok
        self.apply = apply
        self.iconList = iconList
        self.tabLabel = tabLabel
        self.contentLayout = contentLayout
        self.tabs = []
        self.current = -1

    def changeTab (self, previous, current):
        """Different tab has been selected, change the tab content"""
        if self.current == current: return
        if previous != -1:
            self.tabs[previous].deactivateTab()
        self.tabs[current].activateTab()
        self.current = current

    def render (self):
        """Render this widget"""
        self.createGUI()
        self.endRender()

    def createGUI (self):
        """Creates all tabs"""
        for tab in self.communicator.tabs:
            newTab = QtGTab(tab, self.iconList, self.tabLabel, self.contentLayout)
            newTab.render()
            self.tabs.append(newTab)

    def endRender(self):
        """Checks inconsistency and sets the visual hints accordingly"""
        index = self.__getNextVisibleTab()
        self.tabLabel.setVisible(index != -1)
        self.iconList.setCurrentRow(index)
        self.current = index
        self.checkInconsistency(self.communicator.inconsistent)

    def checkInconsistency (self, inconsistent):
        """Checks inconsistency and sets disable state of the ok and apply button if needed"""
        if inconsistent == True:
            self.ok.setEnabled(False)
            self.apply.setEnabled(False)
            self.ok.setToolTip(self.tr("The package contains inconsistent keys and cannot be saved. Fill in all missing values inside the marked fields first."))
            self.apply.setToolTip(self.tr("The package contains inconsistent keys and cannot be saved. Fill in all missing values inside the marked fields first."))
        else:
            self.ok.setEnabled(True)
            self.apply.setEnabled(True)
            self.ok.setToolTip(self.tr("Save changes and close the window."))
            self.apply.setToolTip(self.tr("Save changes but remain open."))

    def __getNextVisibleTab (self):
        """Finds the closest visible tab from the current possition. Looks first up the tab list and then down"""
        if self.current == -1:
            for index in range(0, len(self.tabs)):
                if self.tabs[index].empty == False:
                    return index
            else:
                return -1
        else:
            for index in range(self.current, -1, -1):
                if self.tabs[index].empty == False:
                    return index
            for index in range(self.current + 1, len(self.tabs)):
                if self.tabs[index].empty == False:
                    return index
            return -1

    def toggleAdvanced (self):
        """If show advanced is deselected some visible tab must be selected"""
        index = self.__getNextVisibleTab()
        self.tabLabel.setVisible(index != -1)
        self.iconList.setCurrentRow(index)
        self.current = index

    def processSignal (self, signal, value):
        """Handles signals from the library"""
        if signal == Signals.CHANGE_INCONSISTENCY:
            self.checkInconsistency(value)
