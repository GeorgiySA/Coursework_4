import pytest
import sys
import os

from config import TestConfig
from run import create_app


app = create_app(TestConfig)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(
    __file__), '..')))


@pytest.fixture
def app():
    from run import create_app
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """ Создание тестового клиента. """
    return app.test_client()
