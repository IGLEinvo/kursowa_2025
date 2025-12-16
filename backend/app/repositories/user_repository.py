"""
User Repository - Repository Pattern
"""
from app.database import db
from app.models.user import User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user data access"""
    
    def __init__(self):
        self.table = 'users'
    
    def create(self, user):
        """Create a new user"""
        with db.get_cursor() as cursor:
            sql = """
                INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user.username, user.email, user.password_hash,
                user.first_name, user.last_name, user.role, user.is_active
            ))
            user.id = cursor.lastrowid
            return user
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return User.from_dict(result) if result else None
    
    def find_by_email(self, email):
        """Find user by email"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            return User.from_dict(result) if result else None
    
    def find_by_username(self, username):
        """Find user by username"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            return User.from_dict(result) if result else None
    
    def update(self, user):
        """Update user"""
        with db.get_cursor() as cursor:
            sql = """
                UPDATE users 
                SET username = %s, email = %s, first_name = %s, last_name = %s,
                    role = %s, is_active = %s, updated_at = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                user.username, user.email, user.first_name, user.last_name,
                user.role, user.is_active, datetime.now(), user.id
            ))
            return user
    
    def delete(self, user_id):
        """Delete user"""
        with db.get_cursor() as cursor:
            sql = "DELETE FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            return cursor.rowcount > 0
    
    def find_all(self, limit=None, offset=None):
        """Find all users with pagination"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM users ORDER BY created_at DESC"
            if limit:
                sql += f" LIMIT {limit}"
                if offset:
                    sql += f" OFFSET {offset}"
            cursor.execute(sql)
            results = cursor.fetchall()
            return [User.from_dict(row) for row in results]

