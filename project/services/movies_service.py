from project.dao.movies_dao import MovieDao


class MovieService:
    def __init__(self, dao: MovieDao):
        self.dao = dao

    def get_all(self, genres_args=None, director_args=None, year_args=None,
                status=None, page=None):
        if genres_args and director_args:
            movies = list(set(self.dao.get_by_genre(genres_args)) &
                          set((self.dao.get_by_director(director_args)))
        elif genres_args:
            movies = self.dao.get_by_genre(genres_args)
        elif director_args:
            movies = self.dao.get_by_director(director_args)
        elif year_args:
            movies = self.dao.get_by_year(year_args)
        elif status == "new":
            movies = self.dao.get_all_sorted()
        else:
            movies = self.dao.get_all()
        if page:
            return movies.limit(12).offset((int(page) - 1) * 12).all()
        return movies.all()

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_by_genre(self, gid):
        return self.dao.get_by_genre(gid)

    def get_by_director(self, did):
        return self.dao.get_by_director(did)

    def get_by_year(self, year):
        return self.dao.get_by_year(year)

    def create(self, data):
        return self.dao.create(data)
