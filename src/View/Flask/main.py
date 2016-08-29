#!/usr/bin/python3


from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from View.Flask.renderer import Renderer
# configuration
from Controller.controller import Controller
from Controller.entry_controller import EntryController
from flask_debugtoolbar import DebugToolbarExtension
from IO.XMLPackageParser.input import XMLParser
from IO.output import Output
from Model.package import PackageBase

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.autoescape = False
app.secret_key = 'some_secret'
app.debug = True

toolbar = DebugToolbarExtension(app)
package=PackageBase("test")
package.current_language = "en"
input_parser = XMLParser("/home/ondra/škola/Freeconf/Freeconf/packages/Freeconf")
output = Output()

con=Controller(package, input_parser, output)
con.load_package()
tabs=con.tabs()
renderer=Renderer()


def render_default(body=""):
    return render_template('index.html', text='cot', tabs=tabs, main=body)


@app.route('/_ajax')
def ajax():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con._entry_controller.save_value(full_name, value)
    return jsonify(result=value)

@app.route("/")
def root():
    return render_default()

@app.route("/b")
def baf():
    return render_default()


@app.route("/tab/<name>/")
def tab(name):
    sections=con.tab(name)
    Rsection=""
    for section in sections:
        Rsection=Rsection+renderer.entry_render(section)
    # flash(u'Záložka jméno', 'info')
    return render_default(Rsection)

@app.route("/tab/<name>/save", methods=['POST'])
def save(name):
    if request.method == 'POST':
        form=request.form
        for key in form:
            con._entry_controller.save_value(key, form[key])
    return redirect('tab/'+name)

# @app.route("/tab/<name>/multiple_new", methods=['POST'])
# def multiple_new(name):
#
#     if request.method == 'POST':
#         form=request.form
#         for key in form:
#             con.multiple_new(key)
#     return redirect('tab/'+name)


@app.route("/_multiple_new")
def multiple_new():
    full_name = request.args.get('full_name')
    con._entry_controller.multiple_new(full_name)
    return True

@app.route("/_multiple_delete")
def multiple_delete():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con._entry_controller.multiple_delete(full_name, value)
    return True

@app.route("/_multiple_up")
def multiple_up():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con._entry_controller.multiple_up(full_name, value)
    return True

@app.route("/_multiple_down")
def multiple_down():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con._entry_controller.multiple_down(full_name, value)
    return True

@app.route('/_multiple_modal')
def multiple_modal():
    full_name = request.args.get('full_name')
    entry=con._entry_controller.get_entry(full_name)
    return renderer.render_modal(entry)

def alert():
    print('bbb')

if __name__ == "__main__":
    app.run()

