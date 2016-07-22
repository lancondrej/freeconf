#!/usr/bin/python3


from flask import Flask, render_template, flash, request, redirect, url_for
from View.Flask.renderer import Renderer
# configuration
from Controller.controller import Controller

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.autoescape = False
app.secret_key = 'some_secret'


con=Controller()
con.load_package()
tabs=con.tabs()


def render_default(body=""):
    return render_template('layout.html', text='cot', tabs=tabs, main=body)

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
    return render_default(Rsection)

@app.route("/tab/<name>/save", methods=['POST'])
def save(name):
    if request.method == 'POST':
        form=request.form
        for key in form:
            con.save_value(key, form[key])
    return redirect('tab/'+name)

@app.route("/tab/<name>/multiple_new", methods=['POST'])
def multiple_new(name):

    if request.method == 'POST':
        form=request.form
        for key in form:
            con.multiple_new(key)
    return redirect('tab/'+name)

@app.route("/tab/<name>/multiple_delete", methods=['POST'])
def multiple_delete(name):

    if request.method == 'POST':
        form=request.form
        for key in form:
            con.multiple_delete(key, form[key])
    return redirect('tab/'+name)

def alert():
    print('bbb')

if __name__ == "__main__":
    app.run()

