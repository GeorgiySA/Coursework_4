from project.dao.genres_dao import GenreDao


class GenresService:
    def __init__(self, dao: GenreDao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, gid):
        return self.dao.get_one(gid)
