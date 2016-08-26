__author__ = 'Ondřej Lanč'

# from lxml.etree import Element, ElementTree, SubElement
from xml.etree.ElementTree import Element, ElementTree, SubElement


class ConfigFileWriter (object):
    def __init__(self, file, root):
        self.render = {
            'Container': self.render_container,
            'Fuzzy': self.render_key_word,
            'Bool': self.render_key_word,
            'Number': self.render_key_word,
            'String': self.render_key_word,
            'MultipleContainer': self.render_multiple,
            'MultipleKeyWord': self.render_multiple,
        }
        self._file = file
        self._root = root

    def write_config(self):
        root = self.render_entry(self._root)[0]
        config_tree = ElementTree(root)
        config_tree.write("output.xml", encoding="UTF-8", xml_declaration=True)

    def render_entry(self, entry):
        try:
            return self.render[type(entry).__name__](entry)
        except:
            pass

    def render_container(self, container):
        element = Element('container')
        element.set('name', container.name)
        for entry in container.entries.values():
            sub=self.render_entry(entry)
            element.extend(self.render_entry(entry))
        return [element]

    def render_key_word(self, entry):
        element = Element('entry')
        element.set('name', entry.name)
        element.set('group', entry.group.name)
        value=Element('value')
        value.text = str(entry.value)
        element.append(value)
        return [element]

    def render_multiple(self, mult):
        return [self.render_entry(entry)[0] for entry in mult.entries]