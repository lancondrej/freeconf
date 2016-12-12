#!/usr/bin/python3
# -*- coding: utf-8 -*-#

__author__ = 'Ondřej Lanč'


class Inconsistency(object):
    """This class is used for handling inconsistent states in non-container entries.
    The entry is inconsistent if it is active, mandatory and its value
     has not been set. Inconsistent entries can not be disabled"""

    def __init__(self):
        self._inconsistent = False

    @property
    def inconsistent(self):
        """inconsistent getter"""
        return self._inconsistent

    def change_inconsistency(self, value):
        """This method is called whenever the inconsistency must be changed"""
        if self._inconsistent != value:
            self._inconsistent = value
            self._evaluate_inconsistency()

    def _evaluate_inconsistency(self):
        """Check if the entry is still inconsistent and notify parent."""
        self._notify_parent(self._inconsistent)

    def _notify_parent(self, inconsistent):
        """Notifies parent about change of inconsistency"""
        if self.package is not None:
            self.package.inconsistency_signal(self)
        for parent in self.inc_parents:
            if parent is not None:
                parent.change_inconsistency(inconsistent)

    @property
    def inc_parents(self):
        """get parents entry. Must be reimplemented in sub-class"""
        raise NotImplementedError


class ContainerInconsistency(Inconsistency):
    """This class is used for handling inconsistent states in container entries. The entry is inconsistent if it contains
    at least one inconsistent child. Otherwise it is consistent"""

    def __init__(self):
        Inconsistency.__init__(self)
        # number of inconsistent children
        self._inconsistent_count = 0

    @property
    def inconsistent(self):
        """inconsistent getter"""
        return bool(self._inconsistent_count)

    def change_inconsistency(self, value):
        """This method is called whenever the inconsistency must be changed"""
        assert self._inconsistent_count >= 0

        if value:
            self._inconsistent_count += 1
        else:
            self._inconsistent_count -= 1
        self._evaluate_inconsistency()

    def _evaluate_inconsistency(self):
        """Check if the entry is still inconsistent and notify parent."""
        if self._inconsistent != self.inconsistent:
            self._inconsistent = self.inconsistent
            self._notify_parent(self._inconsistent)

    @property
    def inc_parents(self):
        """get parents entry. Must be reimplemented in sub-class"""
        raise NotImplementedError


class MultipleInconsistency(ContainerInconsistency):
    """This class is used for handling inconsistent states in multiple entries. The entry is inconsistent if it contains
    at least one inconsistent child. Otherwise it is consistent"""

    def __init__(self):
        ContainerInconsistency.__init__(self)
        # number of inconsistent children
        self._self_inconsistent = True

    @property
    def inconsistent(self):
        """inconsistent getter"""
        return bool(self._inconsistent_count) or self._self_inconsistent

    def change_inconsistency(self, value):
        """This method is called whenever the inconsistency must be changed"""
        assert self._inconsistent_count >= 0

        if value:
            self._inconsistent_count += 1
        else:
            self._inconsistent_count -= 1
        self._evaluate_inconsistency()

    def change_self_inconsistency(self, value):
        """This method is called whenever the inconsistency must be changed"""
        if self._self_inconsistent != value:
            self._self_inconsistent = value
            self._evaluate_inconsistency()

    def _evaluate_inconsistency(self):
        """Check if the entry is still inconsistent and notify parent."""
        if self._inconsistent != self.inconsistent:
            self._inconsistent = self.inconsistent
            self._notify_parent(self._inconsistent)

    @property
    def inc_parents(self):
        """get parents entry. Must be reimplemented in sub-class"""
        raise NotImplementedError