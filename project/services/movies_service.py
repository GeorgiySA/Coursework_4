from typing import Dict, Any, Optional, List

from project.dao.movies_dao import MovieDao
from project.dao.model.movie_model import Movie


class MovieService:
    def __init__(self, dao: MovieDao):
        self.dao = dao

    def get_all(self, genres_args=None, director_args=None, year_args=None,
                status=None, page=None) -> List[Movie]:
        query = self.session.query(Movie)

        if genres_args and director_args:
            query = query.filter(Movie.genre_id == genres_args,
                                 Movie.director_id == director_args)
        elif genres_args:
            query = query.filter(Movie.genre_id == genres_args)
        elif director_args:
            query = query.filter(Movie.director_id == director_args)
        elif year_args:
           query = query.filter(Movie.year == year_args)
        elif status == "new":
            query = query.order_by(Movie.title.desc())
        else:
            query = query.all()
        if page:
            return query.limit(12).offset((int(page) - 1) * 12).all()
        return query.all()

    def get_one(self, mid: int) -> Optional[Movie]:
        movie = self.dao.get_one(mid)
        if not movie:
            raise ValueError(f"Movie with id {mid} does not found")
        return movie

    def get_by_genre(self, gid: int) -> List[Movie]:
        movies = self.dao.get_by_genre(gid)
        if not movies:
            raise ValueError(f"Movie with genre - {gid} does not found")
        return movies

    def get_by_director(self, did: int) -> List[Movie]:
        movies = self.dao.get_by_director(did)
        if not movies:
            raise ValueError(f"Movie with director - {did} does not found")
        return movies

    def get_by_year(self, year: int) -> List[Movie]:
        movies = self.dao.get_by_year(year)
        if not movies:
            raise ValueError(f"The film of this release year - {year} was not found")
        return self.dao.get_by_year(year)

    def create(self, data: Dict[str, Any]) -> Movie:
        return self.dao.create(data)

    def update(self, data, mid):
        movie = self.get_one(mid)
        if not movie:
            return None

        movie.title = data["title"]
        movie.description = data["description"]
        movie.trailer = data["trailer"]
        movie.year = data["year"]
        movie.rating = data["rating"]
        movie.genre_id = data["genre_id"]
        movie.director_id = data["director_id"]

        return self.dao.update(movie)

    def update_partial(self, data: Dict[str, Any]) -> Movie:
        mid = data["id"]
        movie = self.get_one(mid)

        if data["title"]:
            movie.title = data["title"]
        if data["description"]:
            movie.description = data["description"]
        if data["trailer"]:
            movie.trailer = data["trailer"]
        if data["year"]:
            movie.year = data["year"]
        if data["rating"]:
            movie.rating = data["rating"]
        if data["genre_id"]:
            movie.genre_id = data["genre_id"]
        if data["director_id"]:
            movie.director_id = data["director_id"]

        return self.dao.update(movie)

    def delete(self, mid: int) -> bool:
        self.dao.delete(mid)
        return True
