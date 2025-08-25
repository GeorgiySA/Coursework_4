import pytest
from unittest.mock import MagicMock, Mock
from project.dao.model.movie_model import Movie
from project.services.movies_service import MovieService


class TestMovieService:

    @pytest.fixture
    def mock_dao(self):
        return Mock()

    @pytest.fixture
    def movie_service(self, mock_dao):
        service = MovieService(mock_dao)
        service.session = MagicMock()
        return service

    @pytest.fixture
    def sample_movie(self):
        return Movie(
            id=1,
            title="Test Movie",
            description="Test Description",
            trailer="Test Trailer",
            year=2023,
            rating=8.5,
            genre_id=3,
            director_id=3
        )

    def test_get_one_movie_exists(self, movie_service, mock_dao, sample_movie):
        mock_dao.get_one.return_value = sample_movie

        result = movie_service.get_one(1)

        assert result.id == 1
        assert result.title == "Test Movie"
        mock_dao.get_one.assert_called_once_with(1)

    def test_get_one_movie_not_found(selfself, movie_service, mock_dao):
        mock_dao.get_one.return_value = None

        with pytest.raises(ValueError, match='Movie with id 999 does not found'):
            movie_service.get_one(999)

    def test_create_movie(self, movie_service, mock_dao, sample_movie):
        movie_data = {
            "title": "New Movie",
            "description": "New Description",
            "trailer": "New Trailer",
            "year": 2024,
            "rating": 8.5,
            "genre_id": 2,
            "director_id": 2
        }
        mock_dao.create.return_value = sample_movie

        result = movie_service.create(movie_data)

        assert result.id == 1
        mock_dao.create.assert_called_once_with(movie_data)

    def test_update_movie(self, movie_service, mock_dao, sample_movie):
        mock_dao.get_one.return_value = sample_movie
        mock_dao.update.return_value = sample_movie

        update_data = {
            "title": "Update Movie",
            "description": "Update Description",
            "trailer": "Update Trailer",
            "year": 2024,
            "rating": 7.5,
            "genre_id": 1,
            "director_id": 1
        }
        result = movie_service.update(update_data, 1)

        assert result.title == "Update Movie"
        mock_dao.get_one.assert_called_once_with(1)
        mock_dao.update.assert_called_once()
