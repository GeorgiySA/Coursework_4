from sqlalchemy import desc
from project.dao.model.movie_model import Movie


class MovieDao:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Movie)

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all_sorted(self):
        return self.session.query(Movie).order_by(Movie.year)
