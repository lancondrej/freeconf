from Model.constants import Types

__author__ = 'Ondřej Lanč'

from flask import render_template


class Renderer(object):

    @staticmethod
    def entry_render(entry):
        try:
            method_name = 'render_' + str(entry.type.name)
            method = getattr(Renderer, method_name)
            return method(entry)
        except:
            pass

    @staticmethod
    def multiple_entry_render(entry):
        try:
            method_name = 'render_' + str(entry.type.name)
            method = getattr(Renderer, method_name)
            return method(entry)
        except:
            pass

    @staticmethod
    def render_UNKNOWN_ENTRY(entry):
        pass

    @staticmethod
    def render_CONTAINER(container):
        entries=[]
        for entry in container.entries.values():
            entries.append(Renderer.entry_render(entry))
        return render_template('entries/section.html', label=container.label, entries=entries)

    @staticmethod
    def render_KEY_WORD(entry):
        pass

    @staticmethod
    def render_FUZZY(entry):
        pass

    @staticmethod
    def render_BOOL(entry):
        return render_template('entries/bool.html', name=entry.name, full_name=entry.full_name, label=entry.label, checked=entry.grade)

    @staticmethod
    def render_NUMBER(entry):
        return render_template('entries/number.html', name=entry.name, full_name=entry.full_name, label=entry.label, value=entry.value, step=entry.step, min=entry.min, max=entry.max)

    @staticmethod
    def render_STRING(entry):
        if entry.list and not entry.user_values:
            return render_template('entries/select.html', name=entry.name, full_name=entry.full_name, label=entry.label, value=entry.value, list=entry.list)
        return render_template('entries/string.html', name=entry.name, full_name=entry.full_name, label=entry.label, value=entry.value, list=entry.list)

    @staticmethod
    def render_MULTIPLE(container):
        entries=[(i, entry.name, Renderer.multiple_entry_render(entry)) for i, entry in enumerate(container.entries)]
        if container.template.type==Types.CONTAINER:
            return render_template('entries/multiple_cont.html', label=container.name, full_name=container.full_name, name=container.name, entries=entries)
        else:
            return render_template('entries/multiple_key.html', label=container.name, full_name=container.full_name, name=container.name, entries=entries)

    @staticmethod
    def render_SECTION(section):
        entries=[]
        for entry in section.entries:
            entries.append(Renderer.entry_render(entry))
        return render_template('entries/section.html', label=section.label, entries=entries)
