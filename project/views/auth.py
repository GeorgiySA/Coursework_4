from flask import request
from flask_restx import Namespace, Resource

from container import auth_service
from container import user_service


auth_ns = Namespace("auth")

@auth_ns.route("/login/")
class AuthViews(Resource):
    def post(self):
        data = request.json
        if not data or None in [data.get("email"), data.get("password")]:
            return {"error": "Email and password are required"}, 400
        try:
            tokens = auth_service.generate_token(data.get("email"), data.get("password"))
            return tokens, 201
        except Exception as e:
            return {"error": str(e)}, 401

    def put(self):
        data = request.json
        if not data:
            return {"error": "No JSON data provided"}, 400

        refresh_token = data.get("refresh_token")

        # # Отладочная информация
        # print(f"Received refresh_token type: {type(refresh_token)}")
        # print(f"Received refresh_token: {refresh_token}")

        if not refresh_token:
            return {"error": "Refresh token is required"}, 400
        if "access_token" in data:
            return {"error": "Only refresh token should be provided"}, 400

        try:
            tokens = auth_service.approve_refresh_token(refresh_token)
            return tokens, 201
        except Exception as e:
            return {"error": str(e)}, 401

@auth_ns.route("/register/")
class RegisterViews(Resource):
    def post(self):
        req_json = request.json
        if not req_json:
            return {"error": "No JSON data provided"}, 400
        if not req_json.get("email") or not req_json.get("password"):
            return {"error": "Email and password are required"}, 400

        try:
            user = user_service.create(req_json)
            return {"message": "User created successfully", "id": user.id}, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Registration error: {str(e)}"}, 400
