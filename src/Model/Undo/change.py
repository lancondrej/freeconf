__author__ = 'Ondřej Lanč'


class Change(object):
    def __init__(self, address):
        self.object_address = None

    def transform(self):
        raise NotImplementedError


class ValueChange(Change):
    def __init__(self, address, old_value, new_value):
        Change.__init__(self, address)
        self.old_value=old_value
        self.new_value=new_value

    def transform(self):
        self.old_value, self.new_value = self.new_value, self.old_value


class NewMultipleChange(Change):
    def __init__(self, address):
        Change.__init__(self, address)

    def transform(self):
        self.__class__ = RemoveMultipleChange


class RemoveMultipleChange(Change):
    def __init__(self, address, object):
        Change.__init__(self, address)
        self._object = object

    def transform(self):
        self.__class__ = NewMultipleChange


class MoveUpMultipleChange(Change):
    def __init__(self, address):
        Change.__init__(self, address)

    def transform(self):
        self.__class__ = MoveDownMultipleChange


class MoveDownMultipleChange(Change):
    def __init__(self, address):
        Change.__init__(self, address)

    def transform(self):
        self.__class__ = MoveUpMultipleChange
