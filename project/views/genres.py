from flask import request, abort
from flask_restx import Namespace, Resource

from container import genre_service
from project.dao.model.genre_model import GenreSchema
from decorators import auth_required

genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route("/")
class GenresView(Resource):
    @auth_required
    def get(self):
        try:
            genres = genre_service.get_all()
            return genres_schema.dump(genres), 200
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def post(self):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            if 'name' not in req_json or not req_json['name'].strip():
                abort(400, "Genre name is required")
            new_genre = genre_service.create(req_json)
            return genre_schema.dump(new_genre), 201
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")


@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        try:
            genre = genre_service.get(gid)
            if not genre:
                abort(404, f"Genre with id {gid} not found")
            return genre_schema.dump(genre), 200
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def put(self, gid):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            if 'name' not in req_json or not req_json['name'].strip():
                abort(400, "Genre name is required")
            update_genre = genre_service.update(gid, req_json)
            if not update_genre:
                abort(404, f"Genre with id {gid} not found")

            return genre_schema.dump(update_genre), 200

        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def delete(self, gid):
        genre_service.delete(gid)
        return "", 204
