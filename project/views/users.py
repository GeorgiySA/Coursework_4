from flask import request, abort
from flask_restx import Namespace, Resource
from container import user_service
from project.dao.model.user_model import UserSchema


user_ns = Namespace("user")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_ns.route("/")
class UsersView(Resource):
    def get(self):
        try:
            users = user_service.get_all()
            return users_schema.dump(users), 200
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    def post(self):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            new_user = user_service.create(req_json)
            return user_schema.dump(new_user), 201
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")


@user_ns.route("/<int:uid>")
class UserViews(Resource):
    def get(self, uid):
        try:
            user = user_service.get_one(uid)
            return user_schema.dump(user), 200
        except ValueError as e:
            abort(404, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    def put(self, uid):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            update_user = user_service.update(req_json, uid)
            if not update_user:
                abort(404, f"User with id {uid} not found")

            return user_schema.dump(update_user), 200

        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    def patch(self, uid):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            update_user = user_service.update_partial(req_json, uid)
            if not update_user:
                abort(404, f"User with id {uid} not found")

            return user_schema.dump(update_user), 200

        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")


@user_ns.route("/password/<int:uid>")
class UserPasswordView(Resource):
    def put(self, uid):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            update_user = user_service.update_partial(req_json, uid)
            if not update_user:
                abort(404, f"User with id {uid} not found")

            return user_schema.dump(update_user), 200

        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")
