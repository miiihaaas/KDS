import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Osnovna konfiguracija."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'connect_args': {
            'connect_timeout': 10
        }
    }

class DevelopmentConfig(Config):
    """Development konfiguracija."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production konfiguracija."""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing konfiguracija."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    # Specifične opcije za SQLite bazu u memoriji
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
