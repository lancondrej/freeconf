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
            'MultipleContainer': self.render_multiple_container,
            # 'MultipleContainer': self.render_multiple_container_collapse,
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
        return render_template('package/entries/container.html',
                               name=container.name,
                               full_name=container.full_name,
                               label=container.label,
                               help=container.help,
                               inconsistent=container.inconsistent,
                               entries=entries)

    def render_fuzzy(entry):
        pass

    def render_bool(self, entry):
        return render_template('package/entries/bool.html',
                               name=entry.name,
                               full_name=entry.full_name,
                               label=entry.label,
                               help=entry.help,
                               inconsistent=entry.inconsistent,
                               checked=entry.grade,
                               )

    def render_number(self, entry):
        return render_template('package/entries/number.html',
                               name=entry.name,
                               full_name=entry.full_name,
                               label=entry.label,
                               help=entry.help,
                               inconsistent=entry.inconsistent,
                               value=entry.value,
                               step=entry.step,
                               min=entry.min,
                               max=entry.max,
                               )

    def render_string(self, entry):
        if entry.list and not entry.user_values:
            return render_template('package/entries/select.html',
                                   name=entry.name,
                                   full_name=entry.full_name,
                                   label=entry.label,
                                   help=entry.help,
                                   inconsistent=entry.inconsistent,
                                   value=entry.value,
                                   list=entry.list,
                                   )
        return render_template('package/entries/string.html',
                               name=entry.name,
                               full_name=entry.full_name,
                               label=entry.label,
                               help=entry.help,
                               inconsistent=entry.inconsistent,
                               value=entry.value,
                               list=entry.list,
                               )

    def render_multiple_container(self, container):
        entries = [(i, container.primary_value(i), entry.full_name, entry.inconsistent) for i, entry in enumerate(container.entries)]
        return render_template('package/entries/multiple_cont.html',
                               name=container.name,
                               full_name=container.full_name,
                               inconsistent=container.inconsistent,
                               label=container.label,
                               help=container.help,
                               entries=entries,
                               )

    def render_multiple_container_collapse(self, container):
        entries = [(i, container.primary_value(i), entry.full_name, entry.inconsistent) for i, entry in enumerate(container.entries)]
        return render_template('package/entries/multiple_cont_collapse.html',
                               name=container.name,
                               full_name=container.full_name,
                               inconsistent=container.inconsistent,
                               label=container.label,
                               help=container.help,
                               entries=entries,
                               )

    def render_multiple_key_word(self, mult_entry):
        entries = [(i, entry.name, self.entry_render(entry), entry.inconsistent) for i, entry in enumerate(mult_entry.entries)]
        return render_template('package/entries/multiple_key.html',
                               name=mult_entry.name,
                               full_name=mult_entry.full_name,
                               inconsistent=mult_entry.inconsistent,
                               label=mult_entry.label,
                               help=mult_entry.help,
                               entries=entries,
                               )

    def render_section(self, section):
        entries = []
        for entry in section.entries:
            entries.append(self.entry_render(entry))
        return render_template('package/entries/section.html',
                               full_name=section.full_name,
                               label=section.label,
                               inconsistent=section.inconsistent,
                               entries=entries,
                               )

    def render_modal(self, entry):
        content = self.entry_render(entry)
        return render_template('elements/modal.html',
                               name=entry.name,
                               full_name=entry.full_name,
                               inconsistent=entry.inconsistent,
                               content=content,
                               index=entry.index,
                               )

    def render_collapse(self, entry):
        content = self.entry_render(entry)
        return render_template('elements/collapse.html',
                               name=entry.name,
                               full_name=entry.full_name,
                               inconsistent=entry.inconsistent,
                               content=content,
                               index=entry.index,
                               )

    def reload_element(self, entry):
        content = self.entry_render(entry)
        return content
