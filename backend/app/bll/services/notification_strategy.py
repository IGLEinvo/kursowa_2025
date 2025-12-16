"""Notification strategy pattern implementation."""
from abc import ABC, abstractmethod
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.dal.repositories.notification_repository import NotificationRepository
from app.dal.models import NotificationModel, NotificationTypeEnum


class INotificationStrategy(ABC):
    """Notification strategy interface."""
    
    @abstractmethod
    def send_notification(self, user_id: int, data: Dict[str, Any], db: Session) -> NotificationModel:
        """Send notification to user."""
        pass


class BreakingNewsStrategy(INotificationStrategy):
    """Strategy for breaking news notifications."""
    
    def send_notification(self, user_id: int, data: Dict[str, Any], db: Session) -> NotificationModel:
        """Send breaking news notification."""
        notification_repo = NotificationRepository(db)
        notification = NotificationModel(
            user_id=user_id,
            notification_type=NotificationTypeEnum.BREAKING_NEWS,
            title=data.get("title", "Breaking News"),
            message=data.get("message", ""),
            article_id=data.get("article_id")
        )
        return notification_repo.create(notification)


class DailyDigestStrategy(INotificationStrategy):
    """Strategy for daily digest notifications."""
    
    def send_notification(self, user_id: int, data: Dict[str, Any], db: Session) -> NotificationModel:
        """Send daily digest notification."""
        notification_repo = NotificationRepository(db)
        notification = NotificationModel(
            user_id=user_id,
            notification_type=NotificationTypeEnum.DAILY_DIGEST,
            title=data.get("title", "Daily Digest"),
            message=data.get("message", "Your daily news digest is ready!"),
            article_id=None
        )
        return notification_repo.create(notification)


class AuthorUpdateStrategy(INotificationStrategy):
    """Strategy for author update notifications."""
    
    def send_notification(self, user_id: int, data: Dict[str, Any], db: Session) -> NotificationModel:
        """Send author update notification."""
        notification_repo = NotificationRepository(db)
        notification = NotificationModel(
            user_id=user_id,
            notification_type=NotificationTypeEnum.AUTHOR_UPDATE,
            title=data.get("title", "New Article from Author"),
            message=data.get("message", ""),
            article_id=data.get("article_id")
        )
        return notification_repo.create(notification)


class CommentReplyStrategy(INotificationStrategy):
    """Strategy for comment reply notifications."""
    
    def send_notification(self, user_id: int, data: Dict[str, Any], db: Session) -> NotificationModel:
        """Send comment reply notification."""
        notification_repo = NotificationRepository(db)
        notification = NotificationModel(
            user_id=user_id,
            notification_type=NotificationTypeEnum.COMMENT_REPLY,
            title=data.get("title", "New Reply to Your Comment"),
            message=data.get("message", ""),
            article_id=data.get("article_id")
        )
        return notification_repo.create(notification)


class ArticleLikeStrategy(INotificationStrategy):
    """Strategy for article like notifications."""
    
    def send_notification(self, user_id: int, data: Dict[str, Any], db: Session) -> NotificationModel:
        """Send article like notification."""
        notification_repo = NotificationRepository(db)
        notification = NotificationModel(
            user_id=user_id,
            notification_type=NotificationTypeEnum.ARTICLE_LIKE,
            title=data.get("title", "Your Article Was Liked"),
            message=data.get("message", ""),
            article_id=data.get("article_id")
        )
        return notification_repo.create(notification)


class NotificationFactory:
    """Factory for creating notification strategies."""
    
    _strategies = {
        NotificationTypeEnum.BREAKING_NEWS: BreakingNewsStrategy,
        NotificationTypeEnum.DAILY_DIGEST: DailyDigestStrategy,
        NotificationTypeEnum.AUTHOR_UPDATE: AuthorUpdateStrategy,
        NotificationTypeEnum.COMMENT_REPLY: CommentReplyStrategy,
        NotificationTypeEnum.ARTICLE_LIKE: ArticleLikeStrategy,
    }
    
    @classmethod
    def create_strategy(cls, notification_type: NotificationTypeEnum) -> INotificationStrategy:
        """Create notification strategy based on type."""
        strategy_class = cls._strategies.get(notification_type)
        if not strategy_class:
            raise ValueError(f"Unknown notification type: {notification_type}")
        return strategy_class()




