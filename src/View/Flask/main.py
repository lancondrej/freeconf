# #!/usr/bin/python3
#
#

from flask import Flask
from flask_socketio import SocketIO,emit
from flask_debugtoolbar import DebugToolbarExtension

socketio = SocketIO()





def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.jinja_env.autoescape = False
    app.config['SECRET_KEY'] = '56asdasss545'
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True

    from src.View.Flask.routes import main_blueprint
    app.register_blueprint(main_blueprint)
    from src.View.Flask.routes import package_blueprint
    app.register_blueprint(package_blueprint)

    socketio.init_app(app)
    return app
