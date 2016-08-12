#!/usr/bin/python3
#
from Model.entries.container import Container
from Model.entries.multiple.multiple_entry import MultipleEntry
from Model.exception_logging.exception import MultipleError
import types

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

    # def create_new(self):
    #     entry = super().create_new()
    #     # if entry:
    #         # TODO: je potřeba to vyřešit nějak elegantě naříklad přidat přímo do přídy container
    #         # entry.primary = types.MethodType(primary_value, entry)
    #         # print(entry.primary)


# def primary_value(self):
#     primary = self.get_entry(self.multiple_entry.primary)
#     if primary:
#         primary=primary.value
#     else:
#         primary=self.index
#     return primary