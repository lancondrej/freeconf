#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


from Model.constants import Types
from Model.exception_logging.log import log

class List:
    """Class for string lists and fuzzy lists."""

    def __init__(self, name):
        self.name = name
        self.values = {}

    def append(self, entry):
        self.values[entry.value] = entry

    def contains(self, value):
        """Return True/False if this list contains given value or not."""
        return value in self.values

    @property
    def entries(self):
        """Return list of entries."""
        return self.values.values()

    def get_entry(self, value):
        """Return entry by value."""
        try:
            return self.values[value]
        except KeyError:
            return None

    def get_first_entry(self):
        """Return first entry in the list. If there is no entry, return None"""
        if len(self.values) == 0:
            return None
        return self.values[min(self.values.keys())]


class StringList(List):
    """Class for string lists."""

    class Entry:

        """This class describes particular string for string config keyword.
        It contains string value, optional label and help as an explanation for
        meaning of given string value."""

        def __init__(self, value="", label="", help=""):
            self.value = value
            self.help = help
            self.label = label

        def __repr__(self):
            return 'StringEntry(%s, "%s", "%s")' % (self.value, self.label, self.help)

    def __init__(self, name):
        List.__init__(self, name)

    @property
    def type(self):
        """Return type of this list entries."""
        return Types.STRING


class FuzzyList(List):
    """Class for fuzzy lists."""

    class Entry:
        """This class describes particular value for fuzzy config keyword."""

        def __init__(self, grade, value="", label="", help=""):
            assert 0 <= grade <= 1
            self.grade = grade
            self.value = value
            self.help = help
            self.label = label

        def __repr__(self):
            return 'FuzzyEntry(%s, "%s", "%s")' % (self.value, self.label, self.help)

    def __init__(self, name):
        List.__init__(self, name)

    @property
    def type(self):
        """Return type of this list entries."""
        return Types.FUZZY

    def get_exact_grade(self, grade):
        """Return entry with given grade. If such entry is not found, None is returned."""
        for e in self.values.values():
            if e.grade == grade:
                return e
        return None

    def get_max_grade(self, max_grade=1.0):
        """Return entry with maximum grade that is lower or equal than maxGrade."""
        max_entry = None
        for e in self.values.values():
            if e.grade <= max_grade and (max_entry is None or max_entry.grade < e.grade):
                max_entry = e
        return max_entry

    def get_min_grade(self, min_grade=0.0):
        """Return entry with minimum grade that is higher or equal than minGrade."""
        min_entry = None
        for e in self.values.values():
            if e.grade >= min_grade and (min_entry is None or min_entry.grade > e.grade):
                min_entry = e
        return min_entry

    def join_list(self, new_list):
        """Add new value list to this fuzzy list."""
        for key in new_list.values:
            if not key in self.values:
                self.values[key] = new_list.values[key]
            else:
                # Key is already in the list. Check if it has same grade
                if new_list.values[key].grade != self.values[key].grade:
                    log.error("FcFuzzyList: joinList: Joining %s with %s. "
                              "Value '%s' is already in the list but with"
                              " different grade!"% (self.name, new_list.name, key))
        return self


class BoolList(FuzzyList):
    """Constant fuzzy list of bool values."""

    def __init__(self):
        List.__init__(self, "bool")
        # Define bool values
        self.append(FuzzyList.Entry(0.0, "no", "No"))
        self.append(FuzzyList.Entry(1.0, "yes", "Yes"))

    @property
    def type(self):
        """Return type of this list entries."""
        return Types.BOOL

# Create constant list of boolean values
boolList = BoolList()

