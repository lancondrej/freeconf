# from src.View.Flask.main import app
# from src.Presenter.main_presenter import MainPresenter
from src.Presenter.main_presenter import MainPresenter
from src.View.Flask.freeconf_flask import FreeconfFlask

_author__ = 'Ondřej Lanč'
# from src.View.Flask.main import socketio, app


if __name__ == "__main__":
    # app.presenter = MainPresenter()
    # app.run()
    #
    freeconf_view=FreeconfFlask()
    freeconf_view.presenter = MainPresenter()
    freeconf_view.run(port=1234, debug=True)
    # socketio.run(app, debug=True)



