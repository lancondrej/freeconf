#!/usr/bin/python3


from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from View.Flask.renderer import Renderer
# configuration
from Controller.controller import Controller
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.autoescape = False
app.secret_key = 'some_secret'
app.debug = True

toolbar = DebugToolbarExtension(app)

con=Controller()
con.load_package()
tabs=con.tabs()


def render_default(body=""):
    return render_template('index.html', text='cot', tabs=tabs, main=body)


@app.route('/_ajax')
def ajax():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con.save_value(full_name, value)
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
        Rsection=Rsection+Renderer.entry_render(section)
    # flash(u'Záložka jméno', 'info')
    return render_default(Rsection)

@app.route("/tab/<name>/save", methods=['POST'])
def save(name):
    if request.method == 'POST':
        form=request.form
        for key in form:
            con.save_value(key, form[key])
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
    con.multiple_new(full_name)
    return True

@app.route("/_multiple_delete")
def multiple_delete():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con.multiple_delete(full_name, value)
    return True

@app.route("/_multiple_up")
def multiple_up():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con.multiple_up(full_name, value)
    return True

@app.route("/_multiple_down")
def multiple_down():
    full_name = request.args.get('full_name')
    value = request.args.get('value')
    con.multiple_down(full_name, value)
    return True

@app.route('/_multiple_modal')
def multiple_modal():
    full_name = request.args.get('full_name')
    entry=con.get_entry(full_name)
    return Renderer.render_modal(entry)

def alert():
    print('bbb')

if __name__ == "__main__":
    app.run()

