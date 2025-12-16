"""
Database connection - Thread-safe connection manager
"""
import pymysql
from contextlib import contextmanager
from config import config
import logging
import threading

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Thread-safe database connection manager"""
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Don't connect on initialization - connect lazily when needed
        pass
    
    def _get_thread_connection(self):
        """Get or create connection for current thread"""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            self._local.connection = self._create_connection()
        elif not self._local.connection.open:
            try:
                self._local.connection.close()
            except:
                pass
            self._local.connection = self._create_connection()
        else:
            # Test connection is alive
            try:
                self._local.connection.ping()
            except:
                try:
                    self._local.connection.close()
                except:
                    pass
                self._local.connection = self._create_connection()
        return self._local.connection
    
    def _create_connection(self):
        """Create a new database connection"""
        try:
            conn = pymysql.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,
                connect_timeout=10,
                read_timeout=30,
                write_timeout=30
            )
            logger.debug("Database connection established for thread")
            return conn
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def get_connection(self):
        """Get database connection for current thread"""
        return self._get_thread_connection()
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor - creates new connection per operation"""
        conn = None
        cursor = None
        
        try:
            # Create a fresh connection for each cursor operation to avoid packet sequence errors
            conn = self._create_connection()
            cursor = conn.cursor()
            
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def close(self):
        """Close database connection for current thread"""
        if hasattr(self._local, 'connection') and self._local.connection:
            try:
                if self._local.connection.open:
                    self._local.connection.close()
                    logger.debug("Database connection closed for thread")
            except:
                pass
            finally:
                self._local.connection = None


# Global database instance
db = DatabaseConnection()

