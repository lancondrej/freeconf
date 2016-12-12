#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from src.Model.Package.entries.entry import Entry
from src.Model.Package.inconsistency import Inconsistency
from src.Model.Package.lists.constants import Types

__author__ = 'Ondřej Lanč'


class KeyWord(Entry, Inconsistency):
    """This is a class for keyword entries"""

    def __init__(self, name, package):
        Entry.__init__(self, name, package)
        Inconsistency.__init__(self)
        self._default_value = None
        self._value = None
        self._dependents = []
        self._static_mandatory = False
        self._dynamic_mandatory = False
        self._list = None
        # If true, user can insert value which is not in the list
        self.user_values = False
        self._inconsistency_init = False

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        """Set default value."""
        if value is not None:
            value = self.convert_value(value)
        self._default_value = value
        # if self._value is None:
        #     self._value = value
        self.logger.debug("setting default def %s on %s" % (str(self._default_value), str(self.name)))

    def is_container(self):
        return False

    def is_keyword(self):
        return True

    def is_multiple_entry_container(self):
        return False

    @property
    def output_value(self):
        """convert value to output string format"""
        raise NotImplementedError("This is abstract method!")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        else:
            self._value = self.convert_value(value)
        self.check_inconsistency()

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
            from src.Model.exception import IncompatibleListTypeException
            raise IncompatibleListTypeException("%s:  Can't set list to '%s'.", str(self), l.name)

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
    def mandatory(self):
        """Dynamic mandatority is the mandatority set by dependencies"""
        return self._static_mandatory or self._dynamic_mandatory

    @mandatory.setter
    def mandatory(self, mandatory):
        if self._static_mandatory and not mandatory:
            from src.Model.exception import PropertyException
            raise PropertyException("Key {} cannot be set non-mandatory by a dependency,"
                                    " because it is static mandatory.".format(self.name))
        self._dynamic_mandatory = mandatory

    def convert_value(self, value):
        """convert value."""
        raise NotImplementedError("This is abstract method!")

    def check_value(self):
        """Check if given value is correct for this entry"""
        raise NotImplementedError("This is abstract method!")

    def check_inconsistency(self):
        if self._inconsistency_init:
            if self.mandatory and self.active and self._value is None:
                self.change_inconsistency(True)
            elif self.check_value():
                self.change_inconsistency(False)
            else:
                self.change_inconsistency(True)

    def init_inconsistency(self):
        self._inconsistency_init=True
        self.check_inconsistency()

    def set_default(self):
        self.value = self.default_value