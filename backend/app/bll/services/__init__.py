"""Services package."""
from .user_service import UserService
from .article_service import ArticleService
from .comment_service import CommentService
from .notification_service import NotificationService
from .recommendation_service import RecommendationService
from .notification_strategy import (
    INotificationStrategy,
    BreakingNewsStrategy,
    DailyDigestStrategy,
    AuthorUpdateStrategy,
    CommentReplyStrategy,
    ArticleLikeStrategy,
    NotificationFactory,
)
from .observer import Observer, SubscriptionObserver

__all__ = [
    "UserService",
    "ArticleService",
    "CommentService",
    "NotificationService",
    "RecommendationService",
    "INotificationStrategy",
    "BreakingNewsStrategy",
    "DailyDigestStrategy",
    "AuthorUpdateStrategy",
    "CommentReplyStrategy",
    "ArticleLikeStrategy",
    "NotificationFactory",
    "Observer",
    "SubscriptionObserver",
]




