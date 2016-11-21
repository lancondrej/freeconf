from src.Presenter.config_presenter import ConfigPresenter
from src.Presenter.package_presenter import PackagePresenter
from src.Presenter.presenter import Presenter
__author__ = 'Ondřej Lanč'


class MainPresenter(Presenter):
    _config = ConfigPresenter()
    def __init__(self):
        self._view=None

    @property
    def config(self):
        return self._config

    @classmethod
    def load_package(cls, name):
        # if self.package is not None and self.package.package_name == name:
        #     return True
        if name not in cls._config.packages_list:
            return None
        return PackagePresenter(cls._config.package(name))
