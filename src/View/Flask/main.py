from flask import Flask, render_template
from View.Flask.renderer import Renderer
# configuration
from Presenter.controller import Controller

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.autoescape = False


con=Controller()
con.load_package()
tabs=con.tabs()


def render_default(sections=None):
    return render_template('layout.html', text='cot', tabs=tabs, sections=sections)

@app.route("/")
def hello():
    return render_default()


@app.route("/b")
def baf():
    return render_default()


@app.route("/tab/<name>")
def tab(name):
    sections=con.tab(name)
    Rsection=""
    for section in sections:
        Rsection=Rsection+Renderer.entry_render(section)
    return render_default(Rsection)


def alert():
    print('bbb')

if __name__ == "__main__":
    app.run()

