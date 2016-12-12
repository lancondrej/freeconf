#!/usr/bin/python3
# -*- coding: utf-8 -*-#
from copy import deepcopy

from src.Model.Package.inconsistency import MultipleInconsistency

__author__ = 'Ondřej Lanč'

from src.Model.Package.entries.entry import Entry
 # TODO: nekonzistentní pokud mám záznamů mimom rozsah

class MultipleEntry(Entry, MultipleInconsistency):
    """Container for multiple config entries."""

    def __init__(self, entry):
        Entry.__init__(self, entry.name, entry.package)
        MultipleInconsistency.__init__(self)
        self._template = entry
        self._template.multiple = True
        self._template.multiple_entry = self
        self._template.index=-1
        self._template.inc_parents.add(self)
        self.template.init_inconsistency()
        self._entries = []
        self._default = []
        # Multiple properties
        self._multiple_min = None
        self._multiple_max = None
        self._inc_parents = set()

    def __deepcopy__(self, memo):
        template=deepcopy(self.template)
        newone = type(self)(template)
        # TODO: není potřeba kopíravat template, ale je v tom případě potřeba vyřešit správně směrování na parent
        newone.__dict__.update(self.__dict__)
        newone._entries = deepcopy(self.entries)
        newone._default = deepcopy(self._default)
        newone._inc_parents = set()
        return newone

    @property
    def multiple_max(self):
        return self._multiple_max

    @multiple_max.setter
    def multiple_max(self, value):
        if value > 0:
            self._multiple_max = value
        else:
            # 0 or less means multipleMax property is disabled
            self._multiple_max = None

    @property
    def multiple_min(self):
        return self._multiple_min

    @multiple_min.setter
    def multiple_min(self, value):
        if value > 0:
            self._multiple_min = value
        else:
            # 0 or less means multipleMin property is disabled
            self._multiple_min = None

    @property
    def name(self):
        """get name"""
        return self.template.name

    @name.setter
    def name(self, name):
        """set name"""
        self.template.name(name)

    @property
    def parent(self):
        """get name"""
        return self.template.parent

    @parent.setter
    def parent(self, parent):
        """set name"""
        self.inc_parents.add(parent)
        self.template._parent = parent

    @property
    def package(self):
        """get package"""
        return self.template.package

    @package.setter
    def package(self, package):
        """set package"""
        self.template.package(package)

    @property
    def group(self):
        return self.template.group

    @group.setter
    def group(self, group):
        self.template.group = group

    @property
    def multiple(self):
        return False

    @property
    def label(self):
        return self.template.label

    @label.setter
    def label(self, label):
        self.template.label=label

    @property
    def help(self):
        return self.template.help

    @help.setter
    def help(self, help):
        self.template.help=help

    @property
    def active(self):
        return self.template.active

    @active.setter
    def active(self, active):
        self.template.active=active

    @property
    def static_active(self):
        return self.template.static_active

    @static_active.setter
    def static_active(self, active):
        self.template.static_active = active

    @property
    def mandatory(self):
        return self.template.mandatory

    @mandatory.setter
    def mandatory(self, mandatory):
        self.template.mandatory =mandatory

    def create_new(self, length):
        if self.multiple_max is None or length < self.multiple_max:
            newone = deepcopy(self._template)
            newone.index = length
            return newone
        return None

    def delete_entry(self, index):
        length = self.size()
        if self.multiple_min is None or length > self.multiple_min:
            entry = self._entries.pop(int(index))
            self._rename_all()
            self.check_inconsistency()
            if entry.inconsistent:
                self.change_inconsistency(False)
            return entry
        return None

    def _rename_all(self):
        for i, entry in enumerate(self._entries):
            entry.index = i

    def is_container(self):
        return self._template.is_container()

    def is_keyword(self):
        return self._template.is_keyword()

    def is_multiple_entry_container(self):
        return True

    def get_multiple_entry(self, i):
        return self._entries[i]

    def insert(self, position, entry):
        self._entries.insert(int(position), entry)
        entry.inc_parents.add(self)
        self.check_inconsistency()
        if entry.inconsistent:
            self.change_inconsistency(True)
        self._rename_all()

    def append(self, entry=None):
        entry = entry or self.create_new(self.size())
        if entry:
            self._entries.append(entry)
            self.check_inconsistency()
            entry.inc_parents.add(self)
            if entry.inconsistent:
                self.change_inconsistency(True)
        return entry

    def append_default(self, entry=None):
        entry = entry or self.create_new(self.default_size())
        if entry:
            self._default.append(entry)
        return entry

    @property
    def entries(self):
        return self._entries

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template_entry):
        self._template = template_entry

    def size(self):
        return len(self._entries)

    def default_size(self):
        return len(self._default)

    def _swap(self, i, j):
        """Swap entries at given positions."""
        # Check range
        i = min(self.size() - 1, max(0, i))
        j = min(self.size() - 1, max(0, j))
        if i != j:
            (self._entries[i], self._entries[j]) = (self._entries[j], self._entries[i])
            self._rename_all()
            return True
        return False

    def move_up(self, i):
        """Move given entry up in the list. If it is on the top of the list, nothing happens."""
        i = int(i)
        return self._swap(i, i - 1)

    def move_down(self, i):
        """Move given entry down in the list. If it is no the bottom of the list, nothing happens."""
        i = int(i)
        return self._swap(i, i + 1)

    @property
    def type(self):
        return self.template.type

    def find_entry(self, relative_name):
        """Find entry in tree. Name is given in format: a/b/c../entry"""
        try:
            (number, rest) = relative_name.split('/', 1)
            if self.is_container:
                return self._entries[int(number)].find_entry(rest)
        except ValueError:
            return self._entries[int(relative_name)]
        return None

    def check_inconsistency(self):
        length = self.size()
        if self.multiple_min is not None and length < self.multiple_min or self.multiple_max is not None and length > self.multiple_max:
            self.change_self_inconsistency(True)
        else:
            self.change_self_inconsistency(False)

    def init_inconsistency(self):
        self.check_inconsistency()
        for entry in self._entries:
            entry.init_inconsistency()
        self.template.inc_parents.clear()
        self.template.init_inconsistency()
        self.template.inc_parents.add(self)

    def set_default(self):
        self._entries = deepcopy(self._default)
        for entry in self._entries:
            entry.set_default()
