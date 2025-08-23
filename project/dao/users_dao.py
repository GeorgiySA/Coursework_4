from typing import List, Optional
from project.dao.model.user_model import User


class UserDao:
    def __init__(self, session):
        self.session = session

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def get_one(self, uid:int) -> Optional[User]:
        return self.session.query(User).get(uid)

    def create(self, data: dict) -> User:
        user = User(**data)

        self.session.add(user)
        self.session.commit()

        return user

    def update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, uid: int) -> bool:
        user = self.session.query(User).get(uid)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()
