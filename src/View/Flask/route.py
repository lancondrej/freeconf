from flask import render_template
from View.Flask.main import app

__author__ = 'Ondřej Lanč'


@app.route("/")
def root():
    return render_template("index.html")