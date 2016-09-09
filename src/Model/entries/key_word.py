#!/usr/bin/python3
#

__author__ = 'Ondřej Lanč'

from src.Model.constants import Types
from src.Model.entries.base_entry import BaseEntry
from src.Model.exception_logging.log import log


class KeyWord(BaseEntry):
    """This is a class for keyword entries"""

    def __init__(self):
        BaseEntry.__init__(self)
        self._default_value = None
        self._value = None
        self._dependents = []
        self._enabled = True
        self._list = None
        # If true, user can insert value which is not in the list
        self.user_values = False

    # def __deepcopy__(self):
    #     entry = BaseEntry.__deepcopy__(self)

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        """Set default value."""
        if value is not None:
            value = self.convert_value(value)
        self._default_value = value
        log.debug("setting default def %s on %s" % (str(self._default_value), str(self.name)))

    def is_container(self):
        return False

    def is_keyword(self):
        return True

    def is_multiple_entry_container(self):
        return False

    @property
    def value(self):
        if self._value is None:
            return self._default_value
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.convert_value(value)

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
