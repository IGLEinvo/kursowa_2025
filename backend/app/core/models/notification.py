"""Notification domain model."""
from datetime import datetime
from enum import Enum
from typing import Optional


class NotificationType(str, Enum):
    """Notification type enumeration."""
    BREAKING_NEWS = "breaking_news"
    DAILY_DIGEST = "daily_digest"
    AUTHOR_UPDATE = "author_update"
    COMMENT_REPLY = "comment_reply"
    ARTICLE_LIKE = "article_like"


class Notification:
    """Notification domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        notification_type: NotificationType = NotificationType.BREAKING_NEWS,
        title: str = "",
        message: str = "",
        article_id: Optional[int] = None,
        is_read: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.notification_type = notification_type
        self.title = title
        self.message = message
        self.article_id = article_id
        self.is_read = is_read
        self.created_at = created_at or datetime.utcnow()
    
    def mark_as_read(self) -> None:
        """Mark notification as read."""
        self.is_read = True




