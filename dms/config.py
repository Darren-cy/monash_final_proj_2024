"""Configuration for Flask app"""
import os 

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True