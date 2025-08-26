import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session

from project.dao.genres_dao import GenreDao
from project.dao.model.genre_model import Genre


class TestGenresDAO:

    @pytest.fixture
    def mock_session(self):
        return create_autospec(Session, instance=True)

    @pytest.fixture
    def genre_dao(self, mock_session):
        return GenreDao(mock_session)

    def test_get_all_genres(self, genre_dao, mock_session):
        mock_genres = [Genre(id=1, name="Action"), Genre(id=2, name="Drama")]
        mock_session.query.return_value.all.return_value = mock_genres

        result = genre_dao.get_all()

        assert result == mock_genres
        mock_session.query.assert_called_once_with(Genre)
        mock_session.query.return_value.all.assert_called_once()

    def test_get_one_genre_not_found(self, genre_dao, mock_session):
        mock_session.query.return_value.get.return_value = None

        result = genre_dao.get_one(100)

        assert result is None
        mock_session.query.return_value.get.assert_called_once_with(100)

    def test_delete_genre_successful(self, genre_dao, mock_session):
        mock_genre = Genre(id=1, name="Test Genre")
        mock_session.query.return_value.get.return_value = mock_genre

        result = genre_dao.delete(1)

        assert result is True
        mock_session.query.assert_called_with(Genre)
        mock_session.query.return_value.get.assert_called_with(1)
        mock_session.delete.assert_called_once_with(mock_genre)
        mock_session.commit.assert_called_once()
