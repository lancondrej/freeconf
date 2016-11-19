from src.Presenter.config_presenter import ConfigPresenter
from src.Presenter.package_presenter import PackagePresenter
from src.Presenter.presenter import Presenter
__author__ = 'Ondřej Lanč'


class MainPresenter(Presenter):
    def __init__(self):
        self._config=ConfigPresenter()
        self._package=None
        self._view=None

    @property
    def package(self):
        return self._package

    @property
    def config(self):
        return self._config

    def load_package(self, name):
        if self.package is not None and self.package.package_name == name:
            return True
        if name not in self.config.packages_list:
            return False
        self._package=PackagePresenter(self.config.package(name))
        self.package.load_package()
        return True

    @property
    def entry(self):
        return self.package.entry