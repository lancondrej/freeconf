#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Ondřej Lanč'

from src.Model.Package.entries.key_word import KeyWord
from src.Model.Package.lists.constants import Types

class Number(KeyWord):
    """This is a class for keyword entries of type number."""

    def __init__(self, name, package):
        KeyWord.__init__(self, name, package)
        # # Initialize Properties
        # Maximum possible value
        self._max = float("inf")
        # Minimum possible value
        self._min = -float("inf")
        # Increment / decrement step
        self._step = None
        # number precision
        self._precision = None
        # number format
        self._print_sign = False

        self._leading_zeros = None



    @property
    def output_value(self):
        """convert value to output string format"""
        if self.value is not None:
            format_string = "{:0="
            if self.print_sign:
                format_string += "+"
            if self.leading_zeros is not None:
                format_string += "{:d}".format(self.leading_zeros)
            else:
                format_string += "0"
            if self.precision is not None:
                format_string += ".{:d}".format(int(self.precision))
            format_string += "f}"
            str=format_string.format(self.value)
            return format_string.format(self.value)


    @property
    def type(self):
        return Types.NUMBER

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
        if self.precision is not None:
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
        self._max = self.convert_precision(value)

    @min.setter
    def min(self, value):
        assert type(value) in [float, int]
        self._min = self.convert_precision(value)

    @step.setter
    def step(self, step):
        assert type(step) in [float, int]
        self._step = self.convert_precision(step)

    @precision.setter
    def precision(self, precision):
        self._precision = int(precision)
        self.max = self._max
        self.min = self._min
        self.step = self._step

    @print_sign.setter
    def print_sign(self, print_sign):
        self._print_sign = print_sign

    @leading_zeros.setter
    def leading_zeros(self, leading_zeros):
        self._leading_zeros = leading_zeros

    def convert_value(self, value):
        """Check if given value can be converted to value for this entry, and if so, return converted value."""
        return self.convert_precision(float(value))

    def check_value(self):
        """Check if entry's value is within permitted range."""
        if self.value is not None:
            if self.value > self.max:
                return False
            if self.value < self.min:
                return False
        return True
