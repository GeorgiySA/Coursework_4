from flask import Flask, render_template
from flask_cors import CORS
from flask_restx import Api

from config import Config
from setup_db import db
from project.dao.model.genre_model import Genre
from project.dao.model.director_model import Director
from project.dao.model.movie_model import Movie
from project.dao.model.user_model import User
from project.views.genres import genres_ns
from project.views.directors import director_ns
from project.views.movies import movie_ns
from project.views.auth import auth_ns
from project.views.users import user_ns


def create_app(config: Config) -> Flask:
    """ Функция создания основного объекта app. """
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    app.app_context().push()
    @app.route("/")
    def index():
        return render_template("index.html")
    configure_app(app)

    return app

def configure_app(app):
    """ функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...) """
    db.init_app(app)
    api = Api(app)
    api.add_namespace(genres_ns)
    api.add_namespace(director_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    load_data(app, db)

def load_data(app, db):
    with app.app_context():
        db.create_all()
        # u1 = User(email="999-66-66@mail.ru", password="TOR_THE_GOOD",
        # name="tor", surname="elder", favorite_genre="thriller")
        # u2 = User(email="999-77-77@mail.ru", password="goodness_and_power",
        # name="bilbo", surname="baggins", favorite_genre="comedy")
        # m1 = Movie(title="Чужой", description="Страх и ужас", trailer="1",
        #            year=1990, rating="8.8", genre_id=1, director_id=1)
        # m2 = Movie(title="Чернокнижник", description="Ужас и ужас", trailer="2",
        #            year=1991, rating="7.8", genre_id=2, director_id=2)
        # g1 = Genre(name="Страх")
        # g2 = Genre(name="Ужас")
        # d1 = Director(name="Джон Пипетка")
        # d2 = Director(name="Марк Подгузник")
        # with db.session.begin():
        #     db.session.add_all([u1, u2, m1, m2, g1, g2, d1, d2])


if __name__ == "__main__":
    app = create_app(Config)
    CORS(app)
    app.run(debug=True)
