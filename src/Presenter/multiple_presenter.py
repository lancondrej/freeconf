from src.Presenter.entry_presenter import EntryPresenter

__author__ = 'Ondřej Lanč'


class MultiplePresenter(EntryPresenter):
    def __init__(self, tree):
        super(MultiplePresenter, self).__init__(tree)

    def multiple_new(self, path):
        entry = self.get_entry(path)
        return entry.create_new()

    def multiple_delete(self, path, index):
        entry = self.get_entry(path)
        return entry.delete_entry(index)

    def multiple_up(self, path, index):
        entry = self.get_entry(path)
        entry.move_up(index)

    def multiple_down(self, path, index):
        entry = self.get_entry(path)
        entry.move_down(index)