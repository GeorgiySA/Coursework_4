from typing import List, Optional

from project.dao.model.genre_model import Genre


class GenreDao:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> List[Genre]:
        return self.session.query(Genre).all()

    def get_one(self, gid: int) -> Optional[Genre]:
        return self.session.query(Genre).get(gid)

    def create(self, data: dict) -> Genre:
        genre = Genre(**data)

        self.session.add(genre)
        self.session.commit()

        return genre

    def update(self, genre: Genre) -> Genre:
        self.session.add(genre)
        self.session.commit()

    def delete(self, gid: int) -> bool:
        self.session.delete(self.session.query(Genre).get(gid))
        self.session.commit()
        return True
