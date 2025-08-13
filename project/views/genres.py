from flask import request
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
        return genres_schema.dump(genre_service.get_all()), 200

@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        return genre_schema.dump(genre_service.get_one(gid)), 200
