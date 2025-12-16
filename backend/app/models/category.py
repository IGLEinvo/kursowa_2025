"""
Category model
"""
from datetime import datetime


class Category:
    """Category model"""
    
    def __init__(self, id=None, name=None, slug=None, description=None, created_at=None):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Category from dictionary"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            slug=data.get('slug'),
            description=data.get('description'),
            created_at=data.get('created_at')
        )

