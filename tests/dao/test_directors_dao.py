import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session

from project.dao.directors_dao import DirectorDao
from project.dao.model.director_model import Director


class TestDirectorDao:

    @pytest.fixture
    def mock_session(self):
        return create_autospec(Session, instance=True)

    @pytest.fixture
    def director_dao(self, mock_session):
        return DirectorDao(mock_session)

    def test_get_all_directors(self, director_dao, mock_session):
        mock_directors = [Director(id=1, name="Director 1"),
                          Director(id=2, name="Director 2")]
        mock_session.query.return_value.all.return_value = mock_directors

        result = director_dao.get_all()

        assert result == mock_directors
        mock_session.query.assert_called_once_with(Director)
        mock_session.query.return_value.all.asserrt_called_once()

    def test_get_one_director_exists(self, director_dao, mock_session):
        mock_director = Director(id=1, name="Test Director")
        mock_session.query.return_value.get.return_value = mock_director

        result = director_dao.get_one(1)

        assert result == mock_director
        mock_session.query.assert_called_once_with(Director)
        mock_session.query.return_value.get.assert_called_once_with(1)

    def test_create_director(self, director_dao, mock_session):
        director_data = {"name": "New Director"}
        expected_director = Director(**director_data)

        result = director_dao.create(director_data)

        assert isinstance(result, Director)
        assert result.name == "New Director"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
