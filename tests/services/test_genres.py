from unittest.mock import Mock, patch
import pytest
from project.dao.model.genre_model import Genre
from project.services.genres_service import GenresService
from config import TestConfig


class TestGenresService:

    @pytest.fixture
    def mock_dao(self):
        return Mock()

    @pytest.fixture
    def genres_service(self, mock_dao):
        return GenresService(mock_dao)

    @pytest.fixture
    def sample_genre(self):
        return Genre(id=1, name='Test Genre')

    def test_get_all_genres(self, genres_service, mock_dao, sample_genre):
        mock_dao.get_all.return_value = [sample_genre]

        result = genres_service.get_all()

        assert len(result) == 1
        assert result[0].id == 1
        mock_dao.get_all.assert_called_once()

    def test_get_one_genre_exists(self, genres_service, mock_dao, sample_genre):
        mock_dao.get_one.return_value = sample_genre

        result = genres_service.get_one(1)

        assert result.id == 1
        assert result.name == "Test Genre"
        mock_dao.get_one.assert_called_once_with(1)

    def test_get_one_genre_not_found(self,genres_service, mock_dao):
        mock_dao.get_one.return_value = None

        with pytest.raises(ValueError, match='Genre with id 9 does not found'):
            genres_service.get_one(9)

    def test_create_genre(self, genres_service, mock_dao, sample_genre):
        genre_data = {"name": "New Genre"}
        mock_dao.create.return_value = sample_genre

        result = genres_service.create(genre_data)

        assert result.id == 1
        mock_dao.create.assert_called_once_with(genre_data)
