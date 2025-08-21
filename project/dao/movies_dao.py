from typing import List, Optional

from project.dao.model.movie_model import Movie


class MovieDao:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> List[Movie]:
        return self.session.query(Movie).all()

    def get_one(self, mid: int) -> Optional[Movie]:
        return self.session.query(Movie).get(mid)

    def get_all_sorted(self) -> List[Movie]:
        return self.session.query(Movie).order_by(Movie.year).all()

    def get_by_genre(self, gid: int) -> Optional[Movie]:
        return self.session.query(Movie).filter(Movie.genre_id == gid).all()

    def get_by_director(self, did: int) -> Optional[Movie]:
        return self.session.query(Movie).filter(Movie.director_id == did).all()

    def get_by_year(self, year: int) -> Optional[Movie]:
        return self.session.query(Movie).filter(Movie.year == year).all()

    def create(self, data: dict) -> Movie:
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie: Movie) -> Movie:
        self.session.add(movie)
        self.session.commit()

    def delete(self, mid: int) -> bool:
        self.session.delete(self.session.query(Movie).get(mid))
        self.session.commit()
        return True
