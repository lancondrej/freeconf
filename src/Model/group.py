#!/usr/bin/python
#
# group.py
# begin: 30.8.2011 by Jan Ehrenberger
#
# Group of records
#
from Model.exception_logging import log


class FcGroup:
    """This class represents group of entries and it's settings."""

    def __init__(self, name):
        self.__name = name
        ## Initialize properties
        ## Main XSL file
        self.transform = None
        self.included_transforms = []
        self.native_output = None
        # Output defaults settings
        self.output_defaults = True

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def include_transform(self, filelocation):
        """Add transform file to list of included transform files."""
        self.included_transforms.append(filelocation)
