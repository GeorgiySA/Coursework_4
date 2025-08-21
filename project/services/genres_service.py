from typing import Dict, Any, Optional, List

from project.dao.genres_dao import GenreDao
from project.dao.model.genre_model import Genre


class GenresService:
    def __init__(self, dao: GenreDao):
        self.dao = dao

    def get_all(self) -> List[Genre]:
        return self.dao.get_all()

    def get_one(self, gid: int) -> Optional[Genre]:
        genre = self.dao.get_one(gid)
        if not genre:
            raise ValueError(f"Genre with id {gid} does not found")
        return genre

    def create(self, data: Dict[str, Any]) -> Genre:
        return self.dao.create(data)

    # def update(self, gid: int, data: Dict[str, Any]) -> Optional[Genre]:
    #     genre = self.get_one(gid)
    #     if not genre:
    #         return None
    #
    #     if 'name' in data:
    #         genre.name = data['name']
    #
    #     return self.dao.update(genre)
