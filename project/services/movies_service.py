from project.dao.movies_dao import MovieDao


class MovieService:
    def __init__(self, dao: MovieDao):
        self.dao = dao

    def get_all(self, status=None, page=None):
        if status == "new":
            movies = self.dao.get_all_sorted()
        else:
            movies = self.dao.get_all()
        if page:
            return movies.limit(12).offset((int(page) - 1) * 12).all()
        return movies.all()

    def get_one(self, mid):
        return self.dao.get_one(mid)
