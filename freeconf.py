
from src.View.Flask.main import socketio, create_app
_author__ = 'Ondřej Lanč'


app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)
