#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.Model.Package.entries.base_entry import BaseEntry

__author__ = 'Ondřej Lanč'


class Entry(BaseEntry):
    """This is basis class for all entries."""

    def __init__(self, name, package):
        BaseEntry.__init__(self, name, package)
        self._help = None
        self._parent = None
        self._static_active = True
        self._dynamic_active = True
        self._enabled = True
        self._inc_parents = set()

        self._multiple = False
        self._group = None  # Group of entry

        self._inconsistent = False

    def __deepcopy__(self, memo):
        newone = type(self)(self.name, self.package)
        newone.__dict__.update(self.__dict__)
        newone._inc_parents = set()
        return newone

    @property
    def parent(self):
        """get name"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        """set name"""
        self.inc_parents.add(parent)
        self._parent = parent

    @property
    def inc_parents(self):
        return self._inc_parents

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
    def full_name(self):
        """Return full path in current tree in form of: /a/b/c/..."""
        path = "/" + self.name
        if self.multiple:
            path = path + "/" + str(self.index)
        if self.parent:
            path = self.parent.full_name + path
        else:
            path = ""
        return path

    @property
    def help(self):
        return self._help

    @help.setter
    def help(self, help):
        self._help = help

    @property
    def group(self):
        # Propagate group from entry's parent
        return self._group or (self.parent.group if self.parent is not None else None)

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
    def active(self):
        """Dynamic activity is the activity set by dependencies"""
        return self._static_active and self._dynamic_active

    @active.setter
    def active(self, active):
        if not self._static_active and active:
            from src.Model.exception import PropertyException
            raise PropertyException("Key {} cannot be set active by a dependency,"
                                    " because it is non inactive by template.".format(self.name))
        self._dynamic_active = active

    @property
    def multiple(self):
        return self._multiple

    @multiple.setter
    def multiple(self, multiple):
        self._multiple=multiple

    def set_default(self):
        raise NotImplementedError