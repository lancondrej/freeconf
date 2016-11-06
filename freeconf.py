from src.View.Flask.main import app
from src.Presenter.main_presenter import MainPresenter
_author__ = 'Ondřej Lanč'


if __name__ == "__main__":
    app.presenter = MainPresenter()
    app.run()
