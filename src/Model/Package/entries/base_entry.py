#!/usr/bin/python3
#
from src.Model.Package.constants import Types
from src.Model.Package.exception_logging import log

__author__ = 'Ondřej Lanč'


class BaseEntry(object):
    """This is basis class for all entries."""

    def __init__(self, name):
        self._name = name
        self._label = None
        self._help = {}
        self._parent = None
        self._static_active = True
        self._dynamic_active = True
        self._static_mandatory = False
        self._dynamic_mandatory = False
        self._enabled = True

        self._multiple = False

        self._group = None  # Group of entry
        self._package = None  # Plugin or package, from which this entry originates.

        self._inconsistent = False
        #self.guiBuddy = None

    def __deepcopy__(self, memo):
        newone = type(self)(self.name)
        newone.__dict__.update(self.__dict__)
        return newone

    @property
    def name(self):
        """get name"""
        return self._name

    @name.setter
    def name(self, name):
        """set name"""
        self._name = str(name)

    @property
    def parent(self):
        """get name"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        """set name"""
        self._parent = parent

    @property
    def package(self):
        """get package"""
        return self._package

    @package.setter
    def package(self, package):
        """set package"""
        self._package = package

    @property
    def root(self):
        """Return root of tree."""
        if self.parent:
            return self.parent.root
        return self

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

    @property
    def full_name(self):
        """Return full path in current tree in form of: /a/b/c/..."""
        path = "/" + self.name
        if self.multiple:
            path = path + "/" + str(self.index)
        if self.parent:
            path = self.parent.full_name + path
        return path

    def __repr__(self):
        return self.__class__.__name__ + '(' + self.name + ')'

    # def move_to_position(self, destination):
    #     """Moves this entry into different position in the parent container."""
    #     if self._parent is None:
    #         return False
    #     self._parent.disconnect(self)
    #     if destination.is_container:
    #         return destination.add_entry(self)

    @property
    def label(self):
        """Returns the correct mutation of the entry's label"""
        return self._label or self.name

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def help(self):
        return self._help

    @help.setter
    def help(self, help):
        self._help = help

    @property
    def group(self):
        if self._group is None and self._parent is not None:
            # Propagate group from entry's parent
            return self._parent.group
        return self._group

    @group.setter
    def group(self, group):
        self._group = group

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
    def active(self):
        """Dynamic activity is the activity set by dependencies"""
        return self._static_active and self._dynamic_active

    @active.setter
    def active(self, active):
        if not self._static_active and active:
            log.error("Key " + self.name +
                      " cannot be set active by a dependency because it is switched off in the template.")
        self._dynamic_active = active

    @property
    def mandatory(self):
        """Dynamic mandatority is the mandatority set by dependencies"""
        return self._static_mandatory or self._dynamic_mandatory

    @mandatory.setter
    def mandatory(self, mandatory):
        if self._static_mandatory and not mandatory:
            log.error("Key " + self.name +
                      " cannot be set non-mandatory by a dependency because it is set mandatory in the template.")
        self._dynamic_mandatory = mandatory

    # @property
    # def inconsistent(self):
    #     return self._inconsistent
    #
    # def handle_dependency_event (self, event, value):
    #     """This property is a bridge between the tree and the dependency code. Special dependency signals
    #     can be handled in sub-classes"""
    #     if event == "active":
    #         if value == self.dynamic_active:
    #             return
    #         self.dynamic_active = value
    #     elif event == "mandatory":
    #         if value == self.dynamic_mandatory:
    #             return
    #         self.dynamic_mandatory = value
    #
    # @property
    # def enabled(self):
    #     return self._enabled

    @property
    def multiple(self):
        return self._multiple

    @multiple.setter
    def multiple(self, multiple):
        self._multiple=multiple
