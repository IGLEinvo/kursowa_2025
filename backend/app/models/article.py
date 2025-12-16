"""
Article model
"""
from datetime import datetime


class Article:
    """Article model"""
    
    def __init__(self, id=None, title=None, slug=None, content=None, excerpt=None,
                 author_id=None, category_id=None, is_breaking=False, is_premium=False,
                 status='draft', views_count=0, likes_count=0, published_at=None,
                 created_at=None, updated_at=None, author=None, category=None):
        self.id = id
        self.title = title
        self.slug = slug
        self.content = content
        self.excerpt = excerpt
        self.author_id = author_id
        self.category_id = category_id
        self.is_breaking = is_breaking
        self.is_premium = is_premium
        self.status = status
        self.views_count = views_count
        self.likes_count = likes_count
        self.published_at = published_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.author = author
        self.category = category
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'excerpt': self.excerpt,
            'author_id': self.author_id,
            'category_id': self.category_id,
            'is_breaking': self.is_breaking,
            'is_premium': self.is_premium,
            'status': self.status,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'published_at': self.published_at.isoformat() if isinstance(self.published_at, datetime) else self.published_at,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
            'author': self.author.to_dict() if self.author else None,
            'category': self.category.to_dict() if self.category else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Article from dictionary"""
        from .category import Category
        from .user import User
        
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            slug=data.get('slug'),
            content=data.get('content'),
            excerpt=data.get('excerpt'),
            author_id=data.get('author_id'),
            category_id=data.get('category_id'),
            is_breaking=data.get('is_breaking', False),
            is_premium=data.get('is_premium', False),
            status=data.get('status', 'draft'),
            views_count=data.get('views_count', 0),
            likes_count=data.get('likes_count', 0),
            published_at=data.get('published_at'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            author=User.from_dict(data['author']) if data.get('author') else None,
            category=Category.from_dict(data['category']) if data.get('category') else None
        )

