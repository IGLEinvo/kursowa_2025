"""
Configuration module - Singleton Pattern
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Singleton Configuration class"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.DEBUG = os.getenv('DEBUG', 'True') == 'True'
        
        # Database configuration
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT = int(os.getenv('DB_PORT', 3306))
        self.DB_USER = os.getenv('DB_USER', 'root')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        self.DB_NAME = os.getenv('DB_NAME', 'news_newspaper')
        
        # JWT configuration
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', self.SECRET_KEY)
        # Default to 7 days (604800 seconds) for development, can be changed in .env
        self.JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 604800))
        
        # Application configuration
        self.API_PREFIX = '/api'
        self.CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
        
        # Notification configuration
        self.BREAKING_NEWS_ENABLED = True
        self.DAILY_DIGEST_TIME = os.getenv('DAILY_DIGEST_TIME', '08:00')
        
    @property
    def DATABASE_URL(self):
        """Construct database connection URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()

