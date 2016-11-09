

class Group:
    """This class represents group of entries and it's settings."""

    def __init__(self, name):
        self.name = name
        ## Initialize properties
        ## Main XSL file
        self.transform = None
        self.native_output = None
        # Output defaults settings
        self.output_defaults = True
