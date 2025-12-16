"""
User model
"""
from datetime import datetime
import bcrypt


class User:
    """User model"""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None,
                 first_name=None, last_name=None, role='user', is_active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Verify password"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create User from dictionary"""
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role', 'user'),
            is_active=data.get('is_active', True),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

