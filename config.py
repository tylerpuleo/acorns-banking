import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'AyLjQJ$!}mP2Em.'
    SQLALCHEMY_DATABASE_URI = "postgresql:///acorns_take_home"


class ProductionConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
