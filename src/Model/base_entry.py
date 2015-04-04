#!/usr/bin/python3
#
from Model.constants import Types
from Model.exception_logging.exception import *
from Model.exception_logging.log import log

__author__ = 'Ondřej Lanč'


class BaseEntry(object):
    """This is basis class for all entries."""

    def __init__(self, name=""):
        self._name = str(name)
        self._label = {}
        self._help = {}
        self.parent = None
        self._static_active = True
        self._dynamic_active = True
        self._static_mandatory = False
        self._dynamic_mandatory = False

        # Multiple properties
        self.multiple = False
        self._multiple_min = None
        self._multiple_max = None

        self._group = None  # Group of entry
        self._package = None  # Plugin or package, from which this entry originates.

        self._inconsistent = False

    @property
    def name(self):
        """get name"""
        return self._name

    @name.setter
    def name(self, name):
        """set name"""
        self._name = str(name)

    @property
    def root(self):
        """Return root of tree."""
        obj = self
        while obj.parent is not None:
            obj = obj.parent
        return obj

    def is_container(self):
        """Return true if it is a container."""
        raise NotImplementedError

    def is_keyword(self):
        """Return true if it is a keyword."""
        raise NotImplementedError

    def is_multiple_entry_container(self):
        """Return true if it is a multiple container."""
        raise NotImplementedError

    @property
    def type(self):
        return Types.UNKNOWN_ENTRY

    def get_path(self):
        """Return full path in current tree in form of: /a/b/c/..."""
        path = self.name
        obj = self
        while obj.parent is not None:
            obj = obj.parent
            path = obj.name + "/" + path
        return "/" + path

    def __repr__(self):
        return self.__class__.__name__ + '(' + self.name + ')'

    def move_to_position(self, destination):
        """Moves this entry into different position in the parent container."""
        if self.parent is None:
            return False
        self.parent.disconnect(self)
        if destination.is_container:
            return destination.add_entry(self)

    def key_label(self, language=""):
        """Returns the correct mutation of the entry's label"""
        try:
            if language == "":
                return self._label[self._package.currentLanguage]
            else:
                return self._label[language]
        except KeyError:
            return ""

    def set_key_label(self, language, label):
        self._label[language] = label

    def set_key_help(self, language, help):
        self._help[language] = help

    @property
    def group(self):
        if self._group is None and self.parent is not None:
            # Propagate group from entry's parent
            return self.parent.group
        return self._group

    @group.setter
    def group(self, group):
        self._group = group

    # def create_entry(self, entry_parent):
    #     """Create and add entry to tree."""
    #     entry = None
    #     if entry_parent is not None and not self.multiple and entry_parent.is_in_container(self.name):
    #         entry = entry_parent.get_entry(self.name)
    #         raise AlreadyExistsError(u"Can't add child! There is already entry with name ({s})"
    #                                  u" in the section ({s}).".format(self.name, entry_parent.name))
    #     if entry is None:
    #         # There is no such config entry yet
    #         if self.multiple:
    #             if entry_parent is not None and entry_parent.is_in_container(self.name):
    #                 # set MC as entry
    #                 entry = entry_parent.get_entry(self.name)
    #                 # Check number of children
    #                 n = entry.size()
    #                 if self.multiple_max and n + 1 > self.multiple_max:
    #                     raise MultipleError(
    #                         u"Can't add child! Maximum number of children ({0:d}) reached.".format(self.multiple_max, ))
    #             else:
    #                 # Create multiple container
    #                 from Model.multiple_entry_container import MultipleEntryContainer
    #                 entry = MultipleEntryContainer(self.name, self.parent)
    #             # add multiple entry to the tree
    #             entry.append(self)
    #         elif entry_parent is not None:
    #             # add normal entry to the tree
    #             entry_parent.add_entry(entry)
    #     return entry

    @property
    def static_active(self):
        """Static activity indicates that the entry is switched on or off. Entries that are off are not processed in
        the client and cannot be turned on by dependencies"""
        return self._static_active

    @static_active.setter
    def static_active(self, active):
        self._static_active = active
        self._dynamic_active = active

    @property
    def static_mandatory(self):
        """Static mandatority indicates that the entry is mandatory or not. Entries that are statically mandatory
        cannot be set non-mandatory by dependencies"""
        return self._static_mandatory

    @static_mandatory.setter
    def static_mandatory(self, mandatory):
        self._static_mandatory = mandatory
        self._dynamic_mandatory = mandatory

    @property
    def dynamic_active(self):
        """Dynamic activity is the activity set by dependencies"""
        if not self._static_active:
            return False
        return self._dynamic_active

    @dynamic_active.setter
    def dynamic_active(self, active):
        if not self._static_active and active:
            log.error("Key " + self.name +
                      " cannot be set active by a dependency because it is switched off in the template.")
            return
        self._dynamic_active = active

    @property
    def dynamic_mandatory(self):
        """Dynamic mandatority is the mandatority set by dependencies"""
        if self._static_mandatory:
            return True
        return self._dynamic_mandatory

    @dynamic_mandatory.setter
    def dynamic_mandatory(self, mandatory):
        if self._static_mandatory and not mandatory:
            log.error("Key " + self.name +
                      " cannot be set non-mandatory by a dependency because it is set mandatory in the template.")
            return
        self._dynamic_mandatory = mandatory

    @property
    def multiple_min(self):
        return self._multiple_min

    @multiple_min.setter
    def multiple_min(self, value):
        if not self.multiple:
            raise ModelGeneralError("Can't set multipleMin property. Entry %s is not multiple!" % (str(self),))
        if value > 0:
            self._multiple_min = value
        else:
            # 0 or less means multipleMin property is disabled
            self._multiple_min = None

    @property
    def inconsistent(self):
        return self._inconsistent

    @property
    def multiple_max(self):
        return self._multiple_max

    @multiple_max.setter
    def multiple_max(self, value):
        if not self.multiple:
            raise ModelGeneralError("Can't set multipleMax property. Entry %s is not multiple!" % (str(self),))
        if value > 0:
            self._multiple_max = value
        else:
            # 0 or less means multipleMax property is disabled
            self._multiple_max = None

    def handle_dependency_event (self, event, value):
        """This property is a bridge between the tree and the dependency code. Special dependency signals
        can be handled in sub-classes"""
        if event == "active":
            if value == self.dynamic_active:
                return
            self.dynamic_active = value
        elif event == "mandatory":
            if value == self.dynamic_mandatory:
                return
            self.dynamic_mandatory = value
