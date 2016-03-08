#!/usr/bin/python3
#
from src.Model.constants import Types
from src.Model.exception_logging.exception import ModelGeneralError
from src.Model.key_word import KeyWord
from src.Model.exception_logging.log import log
__author__ = 'Ondřej Lanč'


class Fuzzy(KeyWord):
    """This is a class for keyword entries of type fuzzy."""

    def __init__(self):
        KeyWord.__init__(self)
        # # Initialize Properties
        # Maximum possible value
        self._max_set = False
        self._max = 1.0
        # Minimum possible value
        self._min_set = False
        self._min = 0.0

    @property
    def type(self):
        return Types.FUZZY

    @property
    def max_set(self):
        return self._max_set

    @property
    def min_set(self):
        return self._min_set

    @property
    def max(self):
        return self._max

    @property
    def min(self):
        return self._min

    @max.setter
    def max(self, m):
        assert type(m) == float and 0.0 <= m <= 1.0
        self._max_set = True
        self._max = m

    @min.setter
    def min(self, m):
        assert type(m) == float and 0.0 <= m <= 1.0
        self._min_set = True
        self._min = m

    @property
    def _type_name(self):
        return "FUZZY"


    def value_to_grade(self, value):
        """Return grade for given value."""
        if value is None:
            return None
        entry = self.list.get_entry(value)
        if entry is not None:
            return entry.grade
        else:
            return None

    def grade_to_value(self, grade):
        """Return valid value from fuzzy list with given grade."""
        if grade is None:
            return None
        else:
            # Find value with given grade
            entry = self.list.get_exact_grade(grade)
            if entry is None:
                raise ModelGeneralError(
                    "Value with grade %d was not found in fuzzy list %s!" % (grade, self.list.name))
            return entry.value

    @property
    def default_grade(self):
        """Get grade of default value."""
        return self.value_to_grade(self.default_value)

    @default_grade.setter
    def default_grade(self, grade):
        """Set default value with given garde."""
        self.default_value = self.grade_to_value(grade)

    def convert_value(self, v):
        """Check if given value can be converted to value for this entry, and if so, return converted value."""
        v = str(v)
        entry = self.list.get_entry(v)
        assert entry is not None
        return entry.value

    def check_value(self, value=None):
        """Check if entry's value is within permitted range. If not, return nearest value that is in the range."""
        if value is None:
            value = self.value

        e = self.list.get_entry(value)
        if e is None:
            log.error("Value '%s' was not found in fuzzy list '%s' for entry %s!" % (
                value, self.list.name, self.name))
            # Return first value in the list
            first = self.list.get_first_entry()
            if first is None:
                log.error("Fuzzy list '%s' is empty!" % (self.list.name,))
                # TODO:nemelo by to tady vyhodit spis chybu?
                return ''
            else:
                return first.value
        if e.grade > self.max:
            # Find value with lower grade
            e = self.list.get_max_grade(self.max)
        if e.grade < self.min:
            # Find value with higher grade
            e = self.list.getMinGrade(self.min)
        return e.value

    def handle_dependency_event(self, event, value):
        """Handles incoming dependency events"""
        KeyWord.handle_dependency_event(self, event, value)
        if event == "min":
            if value == self.min:
                return
            self.min = value
            self.set_value(self.check_value(), True)
        elif event == "max":
            if value == self.max:
                return
            self.max = value
            self.set_value(self.check_value(), True)

    @property
    def grade(self):
        return self.value_to_grade(self.value)

    @grade.setter
    def grade(self, grade):
        self.value = self.grade_to_value(grade)