# #!/usr/bin/python3
#
#
# from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
#
#
# app = Flask(__name__)
# app.config.from_object(__name__)
# app.jinja_env.autoescape = False
# app.secret_key = 'some_secret'
# app.debug = True
# toolbar = DebugToolbarExtension(app)
# app.config['DEBUG_TB_PROFILER_ENABLED'] = True
#
from src.View.Flask.freeconf_flask import FreeconfFlask



app = FreeconfFlask(__name__)
app.config.from_object(__name__)
app.jinja_env.autoescape = False
app.secret_key = 'some_secret'
app.debug = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

toolbar = DebugToolbarExtension(app)
