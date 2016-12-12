#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Presenter.config_presenter import ConfigPresenter
from src.Presenter.package_presenter import PackagePresenter
from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class MainPresenter(Presenter):
    def __init__(self):
        super().__init__()
        self._config = ConfigPresenter()
        self._view = None

    @property
    def config(self):
        return self._config

    def load_package(self, name):
        if name not in self._config.packages_list:
            return None
        return PackagePresenter(self._config.package(name),
                                self._config.language)

    def reload_config(self):
        self._config.reload_config()
        self.log("Config reloaded")
