import jwt
from flask import request, abort


from constants import JWT_ALGORITHM, JWT_SECRET

def auth_required(func):
    """ Проверяет JWT в заголовке Authorization реквеста. """
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            return {"error": "Authorization header is missing"}, 401

        token = request.headers["Authorization"].split("Bearer ")[-1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        except Exception as e:
            return {"error": str(e)}, 401

        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    """ Проверка прав доступа пользователя. """
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        token = request.headers["Authorization"].split("Bearer ")[-1]
        role = None
        try:
            user_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user_token.get("role", "user")
            print(role)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
