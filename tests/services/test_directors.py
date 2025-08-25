import pytest
from unittest.mock import Mock, patch
from project.dao.model.director_model import Director
from project.services.directors_service import DirectorService


class TestDirectorService:

    @pytest.fixture
    def mock_dao(self):
        return Mock()

    @pytest.fixture
    def director_service(self, mock_dao):
        return DirectorService(mock_dao)

    @pytest.fixture
    def sample_director(self):
        return Director(id=1, name='Test Director')

    def test_get_all_directors(self, director_service, mock_dao, sample_director):
        mock_dao.get_all.return_value = [sample_director]

        result = director_service.get_all()

        assert len(result) == 1
        assert result[0].id == 1
        mock_dao.get_all.assert_called_once()

    def test_get_one_director_exists(self, director_service, mock_dao,
                                     sample_director):
        mock_dao.get_one.return_value = sample_director

        result = director_service.get_one(1)

        assert result.id == 1
        assert result.name == "Test Director"
        mock_dao.get_one.assert_called_once_with(1)

    # def test_get_one_director_not_found(self, director_service, mock_dao):
    #     mock_dao.get_one.return_value = None
    #
    #     with pytest.raises(ValueError, math='Director with id 9 not found'):
    #         director_service.get_one(9)

    def test_create_director(self, director_service, mock_dao, sample_director):
        director_data = {"name": "New Director"}
        mock_dao.create.return_value = sample_director

        result = director_service.create(director_data)

        assert result.id == 1
        mock_dao.create.assert_called_once_with(director_data)
