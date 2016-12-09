import os


class Group:
    """This class represents group of entries and it's settings."""

    def __init__(self, name):
        self._name = name
        self.package = None
        #: Main XSL file
        self._transform_file = None
        self.included_transforms = []
        self._native_output = None
        #: Output defaults settings
        self.output_defaults = True

    @property
    def name(self):
        """name getter"""
        return self._name

    @name.setter
    def name(self, name):
        """name setter
        :param name
        """
        self._name = name

    @property
    def transform_file(self):
        """transform file location
        :return full path of file or None if file not set
        """
        return os.path.abspath(os.path.join(self.package.location, self._transform_file))\
            if self._transform_file else None

    @transform_file.setter
    def transform_file(self, transform_file):
        """transform file setter
        :param transform_file
        """
        self._transform_file = transform_file

    @property
    def native_output(self):
        """native output file getter"""
        return self._native_output

    @native_output.setter
    def native_output(self, native_output):
        """native output file setter
        :param native_output
        """
        self._native_output = native_output

    def include_transform(self, plugin, file_location):
        """Add transform file to list of included transform files.
        :param plugin: plugin from which is transform included
        :param file_location: location of trasform file in plugin
        """
        self.included_transforms.append(os.path.abspath(os.path.join(plugin.location, file_location)))

default = Group('default')