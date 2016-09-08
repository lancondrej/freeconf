from Model.constants import Types

__author__ = 'Ondřej Lanč'

from flask import render_template


class Renderer(object):
    def __init__(self):
        self.render = {
            'Container': self.render_container,
            'Fuzzy': self.render_fuzzy,
            'Bool': self.render_bool,
            'Number': self.render_number,
            'String': self.render_string,
            # 'MultipleContainer': self.render_multiple_container,
            'MultipleContainer': self.render_multiple_container_collapse,
            'MultipleKeyWord': self.render_multiple_key_word,
            'GSection': self.render_section,
        }

    def entry_render(self, entry):
        try:
            return self.render[type(entry).__name__](entry)
        except:
            pass

    def render_container(self, container):
        entries = []
        for entry in container.entries.values():
            entries.append(self.entry_render(entry))
        return render_template('entries/container.html', label=container.label, entries=entries)

    def render_fuzzy(entry):
        pass

    def render_bool(self, entry):
        return render_template('entries/bool.html', name=entry.name, full_name=entry.full_name, label=entry.label,
                               checked=entry.grade)

    def render_number(self, entry):
        return render_template('entries/number.html', name=entry.name, full_name=entry.full_name, label=entry.label,
                               value=entry.value, step=entry.step, min=entry.min, max=entry.max)

    def render_string(self, entry):
        if entry.list and not entry.user_values:
            return render_template('entries/select.html', name=entry.name, full_name=entry.full_name, label=entry.label,
                                   value=entry.value, list=entry.list)
        return render_template('entries/string.html', name=entry.name, full_name=entry.full_name, label=entry.label,
                               value=entry.value, list=entry.list)

    def render_multiple_container(self, container):
        entries = [(i, container.primary_value(i), entry.full_name) for i, entry in enumerate(container.entries)]
        return render_template('entries/multiple_cont.html', label=container.name, full_name=container.full_name,
                               name=container.name, entries=entries)

    def render_multiple_container_collapse(self, container):
        entries = [(i, container.primary_value(i), entry.full_name) for i, entry in enumerate(container.entries)]
        return render_template('entries/multiple_cont_collapse.html', label=container.name,
                               full_name=container.full_name, name=container.name, entries=entries)

    def render_multiple_key_word(self, mult_entry):
        entries = [(i, entry.name, self.entry_render(entry)) for i, entry in enumerate(mult_entry.entries)]
        return render_template('entries/multiple_key.html', label=mult_entry.name, full_name=mult_entry.full_name,
                               name=mult_entry.name, entries=entries)

    def render_section(self, section):
        entries = []
        for entry in section.entries:
            entries.append(self.entry_render(entry))
        return render_template('entries/section.html', label=section.label, entries=entries)

    def render_modal(self, entry):
        content = self.entry_render(entry)
        return render_template('elements/modal.html', content=content, name=entry.name, index=entry.index,
                               full_name=entry.full_name)

    def render_collapse(self, entry):
        content = self.entry_render(entry)
        return render_template('elements/collapse.html', content=content, name=entry.name, index=entry.index,
                               full_name=entry.full_name)

    def reload_element(self, entry):
        content = self.entry_render(entry)
        return content
