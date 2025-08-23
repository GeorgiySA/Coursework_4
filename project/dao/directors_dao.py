from typing import List, Optional
from project.dao.model.director_model import Director


class DirectorDao:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> List[Director]:
        return self.session.query(Director).all()

    def get_one(self, did: int) -> Optional[Director]:
        return self.session.query(Director).get(did)

    def create(self, data: dict) -> Director:
        director = Director(**data)

        self.session.add(director)
        self.session.commit()

        return director

    def update(self, director: Director) -> Director:
        self.session.add(director)
        self.session.commit()
        return director

    def delete(self, did: int) -> bool:
        director = self.session.query(Director).get(did)
        if director:
            self.session.delete(director)
            self.session.commit()
            return True
        return False
    