from typing import Dict, Any, Optional, List

from project.dao.directors_dao import DirectorDao
from project.dao.model.director_model import Director


class DirectorService:
    def __init__(self, dao: DirectorDao):
        self.dao = dao

    def get_all(self) -> List[Director]:
        return self.dao.get_all()

    def get_one(self, did: int) -> Optional[Director]:
        director = self.dao.get_one(did)
        if not director:
            raise ValueError(f"Director with id {did} not found")
        return director

    def create(self, data: Dict[str, Any]) -> Director:
        return self.dao.create(data)

    # def update(self, did: int, data: Dict[str, Any]) -> Optional[Director]:
    #     director = self.get_one(did)
    #     if not director:
    #         return None
    #
    #     if "name" in data:
    #         director.name = data["name"]
    #
    #     return self.dao.update(director)

    # def delete(self, did):
    #     self.dao.delete(did)
