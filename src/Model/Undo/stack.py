__author__ = 'Ondřej Lanč'


class Stack(object):
    def __init__(self, max_length):
        self._max_length = max_length
        self._len = 0
        self._items = []

    def push(self, item):
        if self._len < self._max_length:
            item.transform()
            self._items.append(item)
            self._len += 1
            return True
        return False

    def pop(self):
        if self._len:
            self._len -= 1
            return self._items.pop()
        return None
