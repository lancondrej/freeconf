#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Inconsistency(object):
    """This class is used for handling inconsistent states in non-container entries.
    The entry is inconsistent iff    it is active, mandatory and its value and default
     value has not been set. Inconsistent entries can not be disabled"""

    def __init__(self):
        self._inconsistent = False

    @property
    def inconsistent(self):
        return self._inconsistent

    def change_inconsistency(self, value):
        """This method is called whenever the inconsistency must be changed"""
        if self._inconsistent != value:
            self._inconsistent = value
            self._evaluate_inconsistency()

    def _evaluate_inconsistency(self):
        """Check if the entry is still inconsistent. Usually reimplemented in sub-class"""
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
        """get parent entry. Must be reimplemented in sub-class"""
        raise NotImplementedError


class ContainerInconsistency(Inconsistency):
    """This class is used for handling inconsistent states in section entries. The entry is inconsistent if it contains
    at least one inconsistent child. Otherwise it is consistent"""

    def __init__(self):
        Inconsistency.__init__(self)
        # number of inconsistent children
        self._inconsistent_count = 0

    @property
    def inconsistent(self):
        return bool(self._inconsistent_count)

    def change_inconsistency(self, value):
        assert self._inconsistent_count >= 0

        if value:
            self._inconsistent_count += 1
        else:
            self._inconsistent_count -= 1
        self._evaluate_inconsistency()

    def _evaluate_inconsistency(self):
        # if change happends
        if self._inconsistent != self.inconsistent:
            self._inconsistent = self.inconsistent
            self._notify_parent(self._inconsistent)

    @property
    def inc_parents(self):
        """get parent entry. Must be reimplemented in sub-class"""
        raise NotImplementedError
