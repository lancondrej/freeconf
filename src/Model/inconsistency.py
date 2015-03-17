#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Inconsistency(object):
    """This class is used for handling inconsistent states in non-container entries.
    The entry is inconsistent iff    it is active, mandatory and its value and default
     value has not been set. Inconsistent entries can not be disabled"""

    def __init__(self, inconsistent):
        self._inconsistent = inconsistent

    @property
    def inconsistent(self):
        return self._inconsistent

    def change_inconsistency(self, value):
        """This method is called whenever the inconsistency must be changed"""
        if self._inconsistent == value:
            return
        self._inconsistent = value
        self.evaluate_inconsistency()

    def evaluate_inconsistency(self):
        """Check if the entry is still inconsistent. Usually reimplemented in sub-class"""
        self.notify_parent(self._inconsistent)

    def notify_parent(self, value):
        """Notify parent entry when the inconsistency has been changed. Must be reimplemented in sub-class"""
        raise NotImplementedError


class ContainerInconsistency(Inconsistency):
    """This class is used for handling inconsistent states in section entries. The entry is inconsistent if it contains
    at least one inconsistent child. Otherwise it is consistent"""

    def __init__(self):
        Inconsistency.__init__(self, False)
        # number of inconsistent children
        self._inconsistentCount = 0

    def change_inconsistency(self, value):
        if value == True:
            self._inconsistentCount += 1
        else:
            self._inconsistentCount -= 1
        self.evaluate_inconsistency()

    def evaluate_inconsistency(self):
        assert self._inconsistentCount >= 0
        if self._inconsistentCount == 0 and self._inconsistent == True:
            self._inconsistent = False
            self.notify_parent(False)
        elif self._inconsistentCount == 1 and self._inconsistent == False:
            self._inconsistent = True
            self.notify_parent(True)