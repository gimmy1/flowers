# services/users/project/config.py

class BaseConfig:
    """ Base Configuration """
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """ Development Configuration """
    pass

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    pass
