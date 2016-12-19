import unittest

from src.Presenter.main_presenter import MainPresenter
import os


class SamplePackageTestCase(unittest.TestCase):

    def setUp(self):
        os.chdir('../')
        self.main_presenter = MainPresenter()
        self.package_presenter = self.main_presenter.load_package(
            'sample_package')

    def test_getting_unexisting_tab(self):
        self.package_presenter.tab('unexsisting')


if __name__ == '__main__':
    unittest.main()
