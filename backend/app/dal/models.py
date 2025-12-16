"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.utils.database import Base


class SubscriptionTypeEnum(str, enum.Enum):
    """Subscription type enumeration."""
    FREE = "free"
    PAID = "paid"
    PREMIUM = "premium"


class ArticleStatusEnum(str, enum.Enum):
    """Article status enumeration."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class NotificationTypeEnum(str, enum.Enum):
    """Notification type enumeration."""
    BREAKING_NEWS = "breaking_news"
    DAILY_DIGEST = "daily_digest"
    AUTHOR_UPDATE = "author_update"
    COMMENT_REPLY = "comment_reply"
    ARTICLE_LIKE = "article_like"


class UserModel(Base):
    """User SQLAlchemy model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    subscription_type = Column(Enum(SubscriptionTypeEnum), default=SubscriptionTypeEnum.FREE)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    author = relationship("AuthorModel", back_populates="user", uselist=False)
    comments = relationship("CommentModel", back_populates="user")
    likes = relationship("LikeModel", back_populates="user")
    saved_articles = relationship("SavedArticleModel", back_populates="user")
    notifications = relationship("NotificationModel", back_populates="user")


class CategoryModel(Base):
    """Category SQLAlchemy model."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    articles = relationship("ArticleModel", back_populates="category")


class AuthorModel(Base):
    """Author SQLAlchemy model."""
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    bio = Column(Text)
    profile_image_url = Column(String(255))
    articles_count = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="author")
    articles = relationship("ArticleModel", back_populates="author")


class ArticleModel(Base):
    """Article SQLAlchemy model."""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(500))
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    status = Column(Enum(ArticleStatusEnum), default=ArticleStatusEnum.DRAFT, index=True)
    is_exclusive = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    author = relationship("AuthorModel", back_populates="articles")
    category = relationship("CategoryModel", back_populates="articles")
    comments = relationship("CommentModel", back_populates="article")
    likes = relationship("LikeModel", back_populates="article")
    saved_articles = relationship("SavedArticleModel", back_populates="article")
    tags = relationship("ArticleTagModel", back_populates="article", cascade="all, delete-orphan")
    notifications = relationship("NotificationModel", back_populates="article")


class ArticleTagModel(Base):
    """Article tag SQLAlchemy model."""
    __tablename__ = "article_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    tag = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    article = relationship("ArticleModel", back_populates="tags")


class CommentModel(Base):
    """Comment SQLAlchemy model."""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="comments")
    article = relationship("ArticleModel", back_populates="comments")
    parent = relationship("CommentModel", remote_side=[id], backref="replies")


class LikeModel(Base):
    """Like SQLAlchemy model."""
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="likes")
    article = relationship("ArticleModel", back_populates="likes")


class SavedArticleModel(Base):
    """Saved article SQLAlchemy model."""
    __tablename__ = "saved_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="saved_articles")
    article = relationship("ArticleModel", back_populates="saved_articles")


class NotificationModel(Base):
    """Notification SQLAlchemy model."""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    notification_type = Column(Enum(NotificationTypeEnum), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="SET NULL"), index=True)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    
    # Relationships
    user = relationship("UserModel", back_populates="notifications")
    article = relationship("ArticleModel", back_populates="notifications")


class UserPreferenceModel(Base):
    """User preference SQLAlchemy model."""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    preferred_categories = Column(JSON)
    notification_settings = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class AuthorFollowerModel(Base):
    """Author follower SQLAlchemy model."""
    __tablename__ = "author_followers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())




