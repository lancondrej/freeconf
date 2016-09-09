#!/usr/bin/python3


from flask import Flask, render_template, flash, request, redirect, url_for, jsonify

from src.IO.XMLPackageParser.output import XMLOutput
from src.View.Flask.renderer import Renderer
# configuration
from src.Controller.controller import Controller
# from flask_debugtoolbar import DebugToolbarExtension
from src.IO.XMLPackageParser.input import XMLParser
from src.IO.output import Output
from src.Model.package import PackageBase

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.autoescape = False
app.secret_key = 'some_secret'
app.debug = True

# toolbar = DebugToolbarExtension(app)
package=PackageBase("test")
package.current_language = "cs"
input_parser = XMLParser("/home/ondra/škola/Freeconf/Freeconf/packages/test")
output=XMLOutput(package)
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
    return render_default(Rsection)

@app.route("/tab/<name>/save", methods=['POST'])
def save(name):
    if request.method == 'POST':
        form=request.form
        for key in form:
            con._entry_controller.save_value(key, form[key])
    return redirect('tab/'+name)


@app.route("/_multiple_new")
def multiple_new():
    full_name = request.args.get('full_name')
    result=result=con._entry_controller.multiple_new(full_name)
    if not result:
        flash(u'Maximum element reach', 'warning')
    return jsonify(result=result)


@app.route("/_multiple_delete")
def multiple_delete():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    result=result=con._entry_controller.multiple_delete(full_name, value)
    if not result:
        flash(u'Minimum element reach', 'warning')
    return jsonify(result=result)


@app.route("/_multiple_up")
def multiple_up():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con._entry_controller.multiple_up(full_name, value)
    return ""


@app.route("/_multiple_down")
def multiple_down():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con._entry_controller.multiple_down(full_name, value)
    return ""


@app.route('/_multiple_modal')
def multiple_modal():
    full_name = request.args.get('full_name')
    entry=con._entry_controller.get_entry(full_name)
    return renderer.render_modal(entry)


@app.route('/_multiple_collapse')
def multiple_collapse():
    full_name = request.args.get('full_name')
    entry=con._entry_controller.get_entry(full_name)
    return renderer.render_collapse(entry)


@app.route('/_reload_element')
def reload_element():
    full_name = request.args.get('full_name')
    entry=con._entry_controller.get_entry(full_name)
    return renderer.reload_element(entry)


@app.route('/_flash')
def flash_message():
    return render_template('elements/flash.html')


def alert():
    print('bbb')


@app.route("/save")
def config():
    output.write_output()
    return render_default()

#
# if __name__ == "__main__":
#     app.run()
#
