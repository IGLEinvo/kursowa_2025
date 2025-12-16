"""Article domain model."""
from datetime import datetime
from enum import Enum
from typing import Optional, List


class ArticleStatus(str, Enum):
    """Article status enumeration."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Article:
    """Article domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        title: str = "",
        content: str = "",
        summary: Optional[str] = None,
        author_id: int = 0,
        category_id: int = 0,
        status: ArticleStatus = ArticleStatus.DRAFT,
        is_exclusive: bool = False,
        views_count: int = 0,
        likes_count: int = 0,
        comments_count: int = 0,
        published_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ):
        self.id = id
        self.title = title
        self.content = content
        self.summary = summary
        self.author_id = author_id
        self.category_id = category_id
        self.status = status
        self.is_exclusive = is_exclusive
        self.views_count = views_count
        self.likes_count = likes_count
        self.comments_count = comments_count
        self.published_at = published_at
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.tags = tags or []
    
    def is_published(self) -> bool:
        """Check if article is published."""
        return self.status == ArticleStatus.PUBLISHED
    
    def increment_views(self) -> None:
        """Increment view count."""
        self.views_count += 1
        self.updated_at = datetime.utcnow()




