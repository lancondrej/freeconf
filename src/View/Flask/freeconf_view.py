#!/usr/bin/python3
from src.Presenter.main_presenter import MainPresenter
from src.View.Flask.renderer import Renderer

__author__ = 'Ondřej Lanč'


class FreeconfView(object):
    _renderer = None

    def __init__(self):
        self._presenter = MainPresenter()
        if self._renderer is None:
            self._renderer = Renderer()

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter = presenter

    @property
    def renderer(self):
        return self._renderer

    def reload_element(self, full_name):
        entry = self.presenter.entry.get_entry(full_name)
        return self._renderer.reload_element(entry)