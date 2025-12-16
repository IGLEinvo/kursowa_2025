"""Database connection singleton."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
import os

Base = declarative_base()


class DatabaseConnection:
    """Singleton database connection manager."""
    
    _instance: Optional['DatabaseConnection'] = None
    _engine = None
    _session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            database_url = os.getenv(
                "DATABASE_URL",
                "mysql+pymysql://root:password@localhost/news_portal?charset=utf8mb4"
            )
            self._engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
    
    def get_session(self) -> Session:
        """Get database session."""
        return self._session_factory()
    
    def get_engine(self):
        """Get database engine."""
        return self._engine
    
    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=self._engine)
    
    def drop_tables(self):
        """Drop all tables."""
        Base.metadata.drop_all(bind=self._engine)


def get_db() -> Session:
    """Dependency for getting database session."""
    db = DatabaseConnection().get_session()
    try:
        yield db
    finally:
        db.close()




