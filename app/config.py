import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'telegity')

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

class ProductionConfig(Config):
    DB_USER = os.environ.get('MYSQL_USER', 'root')
    DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    DB_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    DB_DATABASE = os.environ.get('MYSQL_DATABASE', 'db')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True
