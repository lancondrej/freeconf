from src.Model.GUI.gentry import GEntry
from src.Model.constants import Types
from src.Model.container import Container
from src.Model.exception_logging.exception import *

__author__ = 'Ondřej Lanč'


class GContainer(GEntry, Container):
    """GUI container class"""
    def __init__ (self, buddy = None, parent = None):
        Container.__init__(self)
        GEntry.__init__(self, buddy, parent)
        self._activeShown = 0
        self._mandatoryShown = 0
        self._sectionShown = 0
        self.empty = None
        self._showAllChildren = False

        @property
        def type (self):
            return Types.CONTAINER

        @property
        def showAllChildren(self):
            return self._showAllChildren

        @property
        def primaryChildName(self):
            raise AttributeError("Property primaryChildName is write only!")

        @primaryChildName.setter
        def primaryChildName(self, name):
            self._primaryChildName = name
            self._primaryChild = None
