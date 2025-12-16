"""Notification repository."""
from typing import List
from sqlalchemy.orm import Session
from app.dal.models import NotificationModel
from app.dal.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[NotificationModel]):
    """Notification repository implementation."""
    
    def __init__(self, db: Session):
        super().__init__(db, NotificationModel)
    
    def get_unread_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[NotificationModel]:
        """Get unread notifications for a user."""
        return self.db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        ).order_by(NotificationModel.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_all_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[NotificationModel]:
        """Get all notifications for a user."""
        return self.db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id
        ).order_by(NotificationModel.created_at.desc()).offset(skip).limit(limit).all()
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        count = self.db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        ).update({"is_read": True})
        self.db.commit()
        return count




