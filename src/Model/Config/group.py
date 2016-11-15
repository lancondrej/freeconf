import os


class Group:
    """This class represents group of entries and it's settings."""

    def __init__(self, name):
        self._name = name
        self.package = None
        ## Main XSL file
        self._transform_file = None
        self.included_transforms = []
        self._native_output = None
        # Output defaults settings
        self.output_defaults = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def transform_file(self):
        return os.path.abspath(os.path.join(self.package.location, self._transform_file)) if self._transform_file else None

    @transform_file.setter
    def transform_file(self, transform_file):
        self._transform_file=transform_file

    @property
    def native_output(self):
        return self._native_output

    @native_output.setter
    def native_output(self, native_output):
        self._native_output=native_output

    def include_transform(self, plugin, filelocation):
        """Add transform file to list of included transform files."""
        self.included_transforms.append(os.path.abspath(os.path.join(plugin.location, filelocation)))
