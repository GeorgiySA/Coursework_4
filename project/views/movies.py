from flask import request, abort
from flask_restx import Namespace, Resource

from project.dao.model.movie_model import MovieSchema
from container import movie_service
from decorators import auth_required


movie_ns = Namespace("movies")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route("/")
class MovieView(Resource):
    @auth_required
    def get(self):
        try:
            genres_args = request.args.get("genre_id")
            director_args = request.args.get("director_id")
            year_args = request.args.get("year")
            status = request.args.get("status")
            page = request.args.get("page")

            genres_args = int(genres_args) if genres_args else None
            director_args = int(director_args) if director_args else None
            year_args = int(year_args) if year_args else None

            return movies_schema.dump(movie_service.get_all(
                genres_args, director_args, year_args, status, page)), 200
        except ValueError as e:
            abort(400, "Invalid parameter type")
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def post(self):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            new_movie = movie_service.create(req_json)
            return movie_schema.dump(new_movie), 201
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")


@movie_ns.route("/<int:mid>")
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        try:
            movie = movie_service.get_one(mid)
            return movie_schema.dump(movie), 200
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def put(self, mid):
        if not request.json:
            abort(400, "No JSON data provided")
        try:
            req_json = request.json
            update_movie = movie_service.update(req_json, mid)
            if not update_movie:
                abort(404, f"Movie with id {mid} not found")

            return movie_schema.dump(update_movie), 200

        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")

    @auth_required
    def delete(self, mid):
        try:
            movie_service.delete(mid)
            return "", 204
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            abort(500, f"Internal server error: {str(e)}")
