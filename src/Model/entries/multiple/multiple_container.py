#!/usr/bin/python3
#
from Model.entries.container import Container
from Model.entries.multiple.multiple_entry import MultipleEntry
from Model.exception_logging.exception import MultipleError

__author__ = 'Ondřej Lanč'



class MultipleContainer(MultipleEntry, Container):
    """Container for multiple config entries."""

    def __init__(self, entry):
        MultipleEntry.__init__(self, entry)
        self._primary = ""

    def add_entry(self, entry):
        if self._template.is_container() or self._template.is_multiple_entry_container():
            return self.template.add_entry(entry)
        raise MultipleError("Add entry - Multiple container is not container.")

    def get_entry(self, name):
        if self._template.is_container():
            return self._template.get_entry(name)
        raise MultipleError("get entry - Multiple container is not container.")

    @property
    def primary(self):
        return self._primary

    @primary.setter
    def primary(self, primary):
        self._primary=primary

    def create_new(self):
        entry = super().create_new()
        if entry:
            entry.primary=entry.get_entry(self.primary)
