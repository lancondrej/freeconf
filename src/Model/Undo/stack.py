#!/usr/bin/python3
# -*- coding: utf-8 -*-#

__author__ = 'Ondřej Lanč'


class Stack(object):
    """Simple implementation of stack. Stack must have set limit count of items.
    :param max_length: maximum count of item in stack
    """
    def __init__(self, max_length):
        self._max_length = max_length
        self._len = 0
        self._items = []

    def push(self, item):
        """Push item to stack if stack is full pop first item else increase length by 1.
        :param item: item
        """
        self._items.append(item)
        if self._len < self._max_length:
            self._len += 1
        else:
            self._items.pop(0)

    def pop(self):
        """Pop last item and decrease length by 1.
        :return item or None
        """
        if self._len:
            self._len -= 1
            return self._items.pop()
        return None

    def flush(self):
        """Delete all stack item and set length to 0."""
        self._items = []
        self._len = 0
