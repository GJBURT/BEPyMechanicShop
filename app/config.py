from os import getenv
import os
from pathlib import Path
from dotenv import load_dotenv
from utils.util import SECRET_KEY

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

class CommonConfig:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications to save memory

class BaseConfig(CommonConfig):
    # Fetching DB_USER and DB_PASSWORD for all environments
    DB_USER = os.getenv('DB_USER', 'root')  # Default to 'root' for testing, can be overridden
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'empty string')  # Default to empty string for testing, can be overridden
    # Default for development, can be overridden in .env file
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@localhost/mechanicshop_db'
    
    # If DB_USER and DB_PASSWORD is not set and it is not testing environment, raise an error
    if not DB_USER or not DB_PASSWORD:
        raise ValueError("ERROR: DB_USER or DB_PASSWORD not set in environment.")

    # print(f"DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}")  # Debugging

class DevelopmentConfig(BaseConfig):
    
    DEBUG = True
    TESTING = False
    
class TestingConfig(CommonConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite database for testing
    DEBUG = True
    TESTING = True
    CACHE_TYPE = 'null'  # Use null cache for testing
    RATELIMIT_ENABLED = False
    SECRET_KEY = 'testing_secret_key'

class ProductionConfig(BaseConfig):
    # Production specific URI that will override the default one
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"  # Use SimpleCache for production
    DEBUG = False
    TESTING = False

# Mapping configuration names to classes
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


