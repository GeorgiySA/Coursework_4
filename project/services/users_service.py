from typing import Dict, Any, Optional, List
import base64
import hashlib
import hmac


from project.dao.users_dao import UserDao
from project.dao.model.user_model import User
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_all(self) -> List[User]:
        return self.dao.get_all()

    def get_one(self, uid: int) -> Optional[User]:
        user = self.dao.get_one(uid)
        if not user:
            raise ValueError(f"User with id {uid} does not exist")
        return user

    def create(self, data: Dict[str, Any]) -> User:
        """ Создает нового пользователя с хэшированным паролем. """
        data["password"] = self.get_hash(data["password"])
        return self.dao.create(data)

    def update(self, data: Dict[str, Any], uid: int) -> Optional[User]:
        """ Полное обновление пользователя. """
        uid = data["id"]
        user = self.get_one(uid)
        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = self.get_hash(data["password"])
        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "favourite_genre" in data:
            user.favorite_genre = data["favorite_genre"]

        return self.dao.update(user)

    def update_partial(self, data: Dict[str, Any], uid: int) -> Optional[User]:
        """ Частичное обновление пользователя. """
        user = self.get_one(uid)
        if not user:
            return None

        # Обработка смены пароля (старый и новый)
        if "password_1" in data and "password_2" in data:
            if self.compare_password(user.password, data["password_1"]):
                user.password = self.get_hash(data["password_2"])

        if "email" in data:
            user.email = data["email"]
        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "favorite_genre" in data:
            user.favorite_genre = data["favorite_genre"]

        return self.dao.update(user)

    def delete(self, uid: int) -> bool:
        self.dao.delete(uid)

    def get_hash(self, password):
        """ Хэширует пароль с использованием PBKDF2 """
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest).decode('utf-8')

    def get_by_email(self, email: str) -> Optional[User]:
        return self.dao.get_by_email(email)

    def compare_password(self, password_hash: str, other_password: str) -> bool:
        decoded_digest = base64.b64decode(password_hash.encode('utf-8'))

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digest, hash_digest)
