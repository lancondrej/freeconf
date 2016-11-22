#!/usr/bin/python3
#
from src.Model.Package.constants import Types
from src.Model.Package.entries.base_entry import BaseEntry
from src.Model.Package.exception_logging.log import log
from src.Model.Package.inconsistency import Inconsistency

__author__ = 'Ondřej Lanč'


class KeyWord(BaseEntry, Inconsistency):
    """This is a class for keyword entries"""

    def __init__(self, name, package):
        BaseEntry.__init__(self, name, package)
        Inconsistency.__init__(self)
        self._default_value = None
        self._value = None
        self._dependents = []
        self._enabled = True
        self._list = None
        # If true, user can insert value which is not in the list
        self.user_values = False

    #
    # def __deepcopy__(self, memo):
    #     return BaseEntry.__deepcopy__(self, memo)

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        """Set default value."""
        if value is not None:
            value = self.convert_value(value)
        self._default_value = value
        if self._value is None:
            self._value = value
        log.debug("setting default def %s on %s" % (str(self._default_value), str(self.name)))

    def is_container(self):
        return False

    def is_keyword(self):
        return True

    def is_multiple_entry_container(self):
        return False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
            if self.mandatory and self.active:
                self.change_inconsistency(True)
        else:
            self._value = self.convert_value(value)
            self.change_inconsistency(False)

    @property
    def type(self):
        return Types.KEY_WORD

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, l):
        if l.type == self.type:
            self._list = l
        else:
            log.error("%s: Incompatible list type! Can't set list to '%s'.", str(self), l.name)
            pass

    def convert_value(self, value):
        """Check if given value can be converted to value for this entry, and if so, return converted value."""
        raise NotImplementedError("This is abstract method!")

    # def handle_dependency_event(self, event, value):
    #     BaseEntry.handle_dependency_event(self, event, value)
    #     if event == "enable":
    #         if value == self._enabled:
    #             return
    #         self._enabled = value
    #     elif event == "value":
    #         self.value = value

    # def add_dependent(self, dep):
    #     """Add dependency that depends on this entry."""
    #     self._dependents.append(dep)
    #
    # def remove_dependent(self, dep):
    #     """Remove given dependency from list of dependent dependencies."""
    #     self._dependents.remove(dep)
    #
    # def update_dependents(self):
    #     """Indicates that value of this entry changed. Update all dependent dependencies."""
    #     log.debug("Updating dependencies on " + str(self))
    #     for d in self._dependents:
    #         d.execute()

    def init_inconsistency(self):
        if self.mandatory and self.active and (self._default_value is None) and (self._value is None):
            self.change_inconsistency(True)
    # @property
    # def inconsistent(self):
    #     if self.mandatory and self.active:
    #         return super().inconsistent
    #     return False
