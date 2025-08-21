from flask import request, abort
from flask_restx import Namespace, Resource

from container import director_service
from project.dao.model.director_model import DirectorSchema
from decorators import auth_required

director_ns = Namespace("directors")

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route("/")
class DirectorsView(Resource):
    @auth_required
    def get(self):
        try:
            directors = director_service.get_all()
            return directors_schema.dump(directors), 200
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def post(self):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            if "name" not in req_json or not req_json["name"].strip():
                abort(400, "Director name is required")
            new_director = director_service.create(req_json)
            return director_schema.dump(new_director), 201
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")


@director_ns.route("/<int:did>")
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        try:
            director = director_service.get(did)
            if not director:
                abort(404, f"Director with id {did} not found")
            return director_schema.dump(director), 200
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def put(self, did):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            if "name" not in req_json or not req_json["name"].strip():
                abort(400, "Director name is required")
            update_director = director_service.update(did, req_json)
            if not update_director:
                abort(404, f"Director with id {did} not found")

            return director_schema.dump(update_director), 200

        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def delete(self, did):
        director_service.delete(did)
        return "", 204
