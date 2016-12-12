#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from src.Model.Package.inconsistency import ContainerInconsistency
from copy import deepcopy
from src.Model.Package.entries.entry import Entry
from src.Model.exception import AlreadyExistsError

__author__ = 'Ondřej Lanč'




class Container(Entry, ContainerInconsistency):
    """This is a class for keyword entries from Template File"""

    def is_multiple_entry_container(self):
        return False

    def __init__(self, name, package):
        Entry.__init__(self, name, package)
        ContainerInconsistency.__init__(self)
        self._entries = {}

    def __deepcopy__(self, memo):
        newone = type(self)(self.name, self.package)
        newone.__dict__.update(self.__dict__)
        newone._entries = deepcopy(self._entries)
        newone._inc_parents = set()

        for entry in newone._entries.values():
            entry.parent=newone
        return newone

    # Override of functions:
    def is_container(self):
        return True

    def is_keyword(self):
        return False

    def is_in_container(self, name):
        return name in self._entries

    def get_entry(self, name):
        """Get entry by name"""
        try:
            return self._entries[name]
        except KeyError:
            return None

    def add_entry(self, entry):
        """insert entry"""
        # assert isinstance(entry, BaseEntry)
        if entry.name in self._entries:
            if isinstance(entry, Container):
                self._entries[entry.name]._merge_container(entry)
                return True
            else:
                raise AlreadyExistsError(u"Can't add child! There is already key word with name ({})"
                                     u" in the container ({}).".format(entry.name, self.name))
        entry.parent = self
        self._entries[entry.name] = entry
        return True

    def _merge_container(self, container):
        self.logger.info("merge container {}".format(self.name))
        for entry in container.entries.values():
            self.add_entry(entry)

    @property
    def entries(self):
        return self._entries

    def size(self):
        return len(self._entries)

    def find_entry(self, relative_name):
        """Find entry in tree. Name is given in format: a/b/c../entry"""
        try:
            (name, rest) = relative_name.split('/', 1)
            if relative_name == '/':
                return self.root
            if relative_name.startswith('/'):
                return self.root.find_entry(rest)
            if self.is_in_container(name):
                return self.get_entry(name).find_entry(rest)
        except ValueError:
            if self.is_in_container(relative_name):
                return self.get_entry(relative_name)
        return None

    def init_inconsistency(self):
        for entry in self._entries.values():
            entry.init_inconsistency()

    def set_default(self):
        for entry in self.entries.values():
            entry.set_default()