from src.IO.XMLPackageParser.config_file import ConfigFileWriter
from src.IO.XMLPackageParser.native_file import NativeFileWriter
from src.IO.output import Output

__author__ = 'Ondřej Lanč'


class XMLOutput(Output):

    def __init__(self, package, output, native, xslt):
        self._package = package
        self._output=output
        self._native=native
        self._xslt=xslt


    def write_output(self):
        config_file_writer = ConfigFileWriter(self._package.tree)
        config_file_writer.write_config(self._output)


    def write_package(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    def write_native(self):
        config_file_writer = ConfigFileWriter(self._package.tree)
        native_file_writer = NativeFileWriter(self._native, self._xslt, config_file_writer)
        native_file_writer.write_native()


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