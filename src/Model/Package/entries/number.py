#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

from src.Model.Package.entries.key_word import KeyWord
from src.Model.Package.lists.constants import Types


class Number(KeyWord):
    """This is a class for keyword entries of type number."""

    def __init__(self, name, package):
        KeyWord.__init__(self, name, package)
        # # Initialize Properties
        # Maximum possible value
        self._max_set = False
        # self.__max = sys.float_info.max
        self._max = 999999999.0
        # Minimum possible value
        self._min_set = False
        self._min = -999999999.0
        # Increment / decrement step
        self._step_set = False
        self._step = 1
        # number precision
        self._precision_set = False
        self._precision = 0
        # number format
        self._print_sign_set = False
        self._print_sign = False

        self._leading_zeros_set = False
        self._leading_zeros = False

    @property
    def type(self):
        return Types.NUMBER

    @property
    def max_set(self):
        return self._max_set

    @property
    def min_set(self):
        return self._min_set

    @property
    def step_set(self):
        return self._step_set

    @property
    def precision_set(self):
        return self._precision_set

    @property
    def max(self):
        return self._max

    @property
    def min(self):
        return self._min

    @property
    def step(self):
        return self._step

    @property
    def precision(self):
        return self._precision

    def convert_precision(self, value):
        if self._precision_set:
            if self._precision == 0:
                return int(value)
            else:
                return round(value, self._precision)
        return value

    @property
    def print_sign(self):
        return self._print_sign

    @property
    def leading_zeros(self):
        return self._leading_zeros

    @max.setter
    def max(self, value):
        assert type(value) in [float, int]
        self._max_set = True
        self._max = self.convert_precision(value)

    @min.setter
    def min(self, value):
        assert type(value) in [float, int]
        self._min_set = True
        self._min = self.convert_precision(value)

    @step.setter
    def step(self, step):
        assert type(step) in [float, int]
        self._step_set = True
        self._step = self.convert_precision(step)

    @precision.setter
    def precision(self, precision):
        self._precision_set = True
        self._precision = int(precision)
        self.max = self._max
        self.min = self._min
        self.step = self._step

    @print_sign.setter
    def print_sign(self, print_sign):
        self._precision_set = True
        self._print_sign = print_sign

    @leading_zeros.setter
    def leading_zeros(self, leading_zeros):
        self._leading_zeros_set = True
        self._leading_zeros = leading_zeros

    def convert_value(self, v):
        """Check if given value can be converted to value for this entry, and if so, return converted value."""
        return self.convert_precision(self.check_value(float(v)))

    def check_value(self, value=None):
        """Check if entry's value is within permitted range. If not, return nearest value that is in the range."""
        if self.max_set and value > self.max:
            return self.max
        elif self.min_set and value < self.min:
            return self.min
        return value