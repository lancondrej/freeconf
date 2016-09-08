__author__ = 'Ondřej Lanč'

from flask.views import View
from flask import render_template

class BaseEntryView(View):

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        # context = {'objects': self.get_objects()}
        # return self.render_template(context)
        return "ahoj"
