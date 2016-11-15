__author__ = 'Ondřej Lanč'


class Change(object):
    def __init__(self, entry):
        self.entry = entry

    def transform(self):
        raise NotImplementedError

    def change(self):
        raise  NotImplementedError


class ValueChange(Change):
    def __init__(self, entry, old_value):
        Change.__init__(self, entry)
        self.old_value = old_value

    def transform(self):
        return ValueChange(self.entry, self.entry.value)

    def change(self):
        self.entry.value=self.old_value


class NewMultipleChange(Change):
    def __init__(self, entry, newone):
        Change.__init__(self, entry)
        self.newone = newone

    def transform(self):
        return RemoveMultipleChange(self.entry, self.newone)

    def change(self):
        self.entry.delete_entry(self.newone.index)


class RemoveMultipleChange(Change):
    def __init__(self, entry, removed):
        Change.__init__(self, entry)
        self.removed = removed

    def transform(self):
        return NewMultipleChange(self.entry, self.removed)

    def change(self):
        self.entry.insert(self.removed.index, self.removed)


class MoveUpMultipleChange(Change):
    def __init__(self, entry, index):
        Change.__init__(self, entry)
        self.index = index

    def transform(self):
        return MoveDownMultipleChange(self.entry, self.index - 1)

    def change(self):
        self.entry.move_down(self.index)


class MoveDownMultipleChange(Change):
    def __init__(self, entry, index):
        Change.__init__(self, entry)
        self.index = index

    def transform(self):
        return MoveUpMultipleChange(self.entry, self.index + 1)

    def change(self):
        self.entry.move_up(self.index)
