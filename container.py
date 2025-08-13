from project.dao.genres_dao import GenreDao
from project.dao.directors_dao import DirectorDao
from project.dao.movies_dao import MovieDao
from project.dao.users_dao import UserDao

from project.services.genres_service import GenresService
from project.services.directors_service import DirectorService
from project.services.movies_service import MovieService
from project.services.users_service import UserService
from project.services.auth_service import AuthService
from setup_db import db

genre_dao = GenreDao(db.session)
genre_service = GenresService(dao=genre_dao)

director_dao = DirectorDao(db.session)
director_service = DirectorService(dao=director_dao)

movie_dao = MovieDao(db.session)
movie_service = MovieService(dao=movie_dao)

user_dao = UserDao(db.session)
user_service = UserService(dao=user_dao)

auth_service = AuthService(user_service)
