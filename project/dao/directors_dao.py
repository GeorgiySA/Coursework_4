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

    def delete(self, did: int) -> bool:
        self.session.delete(self.session.query(Director).get(did))
        self.session.commit()
        return True
    