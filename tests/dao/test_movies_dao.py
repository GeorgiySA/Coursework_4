import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session

from project.dao.movies_dao import MovieDao
from project.dao.model.movie_model import Movie


class TestMovieDao:

    @pytest.fixture
    def mock_session(self):
        return create_autospec(Session, instance=True)

    @pytest.fixture
    def movie_dao(self, mock_session):
        return MovieDao(mock_session)

    def test_get_all_sorted_movies(self, movie_dao, mock_session):
        mock_movies = [
            Movie(id=1, title="Movie A", year=2020),
            Movie(id=2, title="Movie B", year=2021)
        ]
        mock_query = mock_session.query.return_value
        mock_query.order_by.return_value.all.return_value = mock_movies

        result = movie_dao.get_all_sorted()

        assert result == mock_movies
        mock_session.query.assert_called_once_with(Movie)
        mock_query.order_by.assert_called_once_with(Movie.year)
        mock_query.order_by.return_value.all.assert_called_once()

    def test_get_by_genre(self, movie_dao, mock_session):
        mock_movies = [Movie(id=1, title="Action Movie", genre_id=1)]
        mock_session.query.return_value.filter.return_value = mock_movies

        result = movie_dao.get_by_genre(1)

        assert result == mock_movies
        mock_session.query.assert_called_once_with(Movie)
        mock_session.query.return_value.filter.assert_called()

    def test_get_by_director(self, movie_dao, mock_session):
        mock_movies = [Movie(id=1, title="Director's Movie", director_id=1)]
        mock_session.query.return_value.filter.return_value.all.return_value = mock_movies

        result = movie_dao.get_by_director(1)

        assert result == mock_movies
        mock_session.query.assert_called_once_with(Movie)
        mock_session.query.return_value.filter.assert_called_once()
        mock_session.query.return_value.filter.return_value.all.assert_called_once()
