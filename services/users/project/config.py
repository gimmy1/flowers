# services/users/project/config.py
import os

class BaseConfig:
    """ Base Configuration """
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False 


class DevelopmentConfig(BaseConfig):
    """ Development Configuration """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
