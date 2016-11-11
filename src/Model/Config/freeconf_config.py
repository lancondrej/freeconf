
__author__ = 'Ondřej Lanč'


class Config(object):
    def __init__(self):
        self._config_file = "freeconf.xml"
        self._packages={}
        self._lang = []

    @property
    def packages(self):
        return self._packages

    def package(self, name):
        return self._packages[name]

    @property
    def config_file(self):
        return self._config_file

    @property
    def lang(self):
        return self._lang

    # def _load_config(self):
    #     tree = ET.parse(self._config_file)
    #     root = tree.getroot()
    #     for package in root.findall('package'):
    #         p = Package()
    #         p.name = package.find('name').text
    #         p.location = package.find('location').text
    #         p.output = package.find('output').text
    #         p.native = package.find('native').text
    #         p.xslt = package.find('xslt').text
    #         self._packages[p.name]=p
    #     for lang in root.findall('.general/lang'):
    #             self._lang.append(lang.text)