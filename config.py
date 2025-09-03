import os
from dotenv import load_dotenv


load_dotenv() # Загружает данные из .env файла

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///movies.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
    JSON_AS_ASCII = False
    JWT_SECRET = os.getenv('JWT_SECRET')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    DEBUG = False
