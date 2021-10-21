import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'telegity')

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@telegity.com')
    ADMIN_NAME = os.environ.get('ADMIN_NAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')

class ProductionConfig(Config):
    #DB_USER = os.environ.get('MYSQL_USER', 'root')
    #DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    #DB_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    #DB_DATABASE = os.environ.get('MYSQL_DATABASE', 'db')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'app.sqlite')

class DevelopmentConfig(Config):
    DEBUG = True

    # SQLAlchemy folder
    os.makedirs(os.path.join(basedir, 'db'), exist_ok=True)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'app.sqlite')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

class TestingConfig(Config):
    DEBUG = True

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True
