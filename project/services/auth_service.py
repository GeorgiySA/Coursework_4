from flask import abort
from datetime import datetime, timedelta
import jwt
import calendar

from constants import JWT_ALGORITHM, JWT_SECRET


class AuthService:
    """ Проверяет правильность пароля по имени пользователя,
    формирует новый набор данных (username, role, token """
    def __init__(self, user_service):
        self.user_service = user_service

    def generate_token(self, email, password, is_refresh=False):
        if not email or not password:
            raise ValueError("Email and password are required")

        user = self.user_service.get_by_email(email)
        if user is None:
            raise ValueError("User not found")

        if not is_refresh and not self.user_service.compare_password(user.password,
                                                                     password):
            raise ValueError("Invalid password")

        data = {
            "email": user.email
        }

        min30 = datetime.utcnow() + timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        day130 = datetime.utcnow() + timedelta(days=130)
        data["exp"] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        try:
            # Принудительное преобразование в строку
            if isinstance(refresh_token, bytes):
                refresh_token = refresh_token.decode('utf-8')
            elif not isinstance(refresh_token, str):
                refresh_token = str(refresh_token)

            # Удаление возможных кавычек и пробелов
            refresh_token = refresh_token.strip().strip('"').strip("'")

            data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            email = data.get("email")
            if not email:
                raise ValueError("Email not found in token")
            return self.generate_token(email, None, is_refresh=True)
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token {str(e)}")
        except Exception as e:
            raise ValueError(f"Token processing error: {str(e)}")
