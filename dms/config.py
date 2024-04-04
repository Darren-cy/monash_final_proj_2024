"""Configuration for Flask app"""
from datetime import timedelta
import os 

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True