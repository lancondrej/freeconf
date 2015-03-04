#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class FcFileLocation:
    """Structure storing name of file and it's full path."""
    def __init__(self, name=None):
        self.name = name
        self.fullPath = None

    def __nonzero__(self):
        return self.name is not None and self.name != ""

    def __repr__(self):
        return "%s(%s)" % (self.name, self.fullPath)


class FcIncludeFileLocation(FcFileLocation):
    """Extension of FcFileLocation: reference to plugin."""
    def __init__(self, plugin, name = None):
        FcFileLocation.__init__(self, name)
        self.plugin = plugin



