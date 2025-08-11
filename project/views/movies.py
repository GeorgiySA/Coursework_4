from flask import request
from flask_restx import Namespace, Resource

from project.dao.model.movie_model import MovieSchema
from container import movie_service


movie_ns = Namespace("movies")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movie_ns.route("/")
class MovieView(Resource):
    def get(self):
        status = request.args.get("status", False)
        page = request.args.get("page", False)
        return movies_schema.dump(movie_service.get_all(status, page)), 200

@movie_ns.route("/<int:mid")
class MovieView(Resource):
    def get(self, mid):
        return movie_schema.dump(movie_service.get_one(mid)), 200