#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Types:
    """Basic Freeconf types."""
    # # Entry Types ##
    UNKNOWN_ENTRY = 1
    CONTAINER = 2
    KEY_WORD = 3
    FUZZY = 4
    BOOL = 5
    NUMBER = 6
    STRING = 7


class Signals:
    """List of signals, that can be sent from PyFC to GUI Widget"""
    CHANGE_ENABLED = 1  # property enabled of entry changed
    CHANGE_ACTIVE = 2  # property mandatory of entry changed
    CHANGE_MANDATORY = 3  # property mandatory of entry changed
    CHANGE_VALUE = 4  # value of key_word has been changed by a dependency
    CHANGE_MIN = 5  # property min of Number has been changed
    CHANGE_MAX = 6  # property max of Number has been changed
    CHANGE_STEP = 7  # property step of Number has been changed
    CHANGE_STRING_LIST = 8  # property values of String has been changed
    CHANGE_INCONSISTENCY = 9  # property inconsistency of keyWord has been changed
    CHANGE_EMPTINESS = 10  # this signal is invoked if a section or tab has only inactive or non-mandatory children
    CHANGE_SHOW_ALL = 11  # this signal is called when the show all button has been pressed