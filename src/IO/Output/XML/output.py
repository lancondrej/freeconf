from IO.Output.output import Output
from IO.Output.XML.config_file import ConfigFileWriter
__author__ = 'Ondřej Lanč'


class XMLOutput(Output):

    def __init__(self, package):
        self._package = package

    def write_output(self):
        config_file_writer = ConfigFileWriter('s', self._package.tree)
        config_file_writer.write_config()


    def write_package(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    def write_native(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    @property
    def output(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    @output.setter
    def output(self, output):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    @property
    def package(self):
        return self.package


    @package.setter
    def package(self, package):
        self._package = package


    @property
    def config(self):
        return self._config


    @config.setter
    def config(self, config):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    @property
    def native(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    @native.setter
    def native(self, native):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError