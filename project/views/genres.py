from flask import request
from flask_restx import Namespace, Resource
from container import genre_service
from project.dao.model.genre_model import GenreSchema

genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genres_ns.route("/")
class GenresView(Resource):
    def get(self):
        return genres_schema.dump(genre_service.get_all()), 200

@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    def get(self, gid):
        return genre_schema.dump(genre_service.get_one(gid)), 200
