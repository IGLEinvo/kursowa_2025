"""Notification service with Strategy and Observer patterns."""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.dal.repositories.notification_repository import NotificationRepository
from app.dal.models import NotificationModel, NotificationTypeEnum
from app.bll.services.notification_strategy import NotificationFactory, INotificationStrategy
from app.bll.services.observer import Observer


class NotificationService:
    """Notification service with Strategy and Observer patterns."""
    
    def __init__(self, db: Session):
        self.notification_repository = NotificationRepository(db)
        self.db = db
        self._observers: List[Observer] = []
    
    def subscribe(self, observer: Observer) -> None:
        """Subscribe an observer (Observer pattern)."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribe an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self, event: Dict[str, Any]) -> None:
        """Notify all observers (Observer pattern)."""
        for observer in self._observers:
            observer.update(event)
    
    def send_notification(
        self,
        user_id: int,
        notification_type: str,
        data: Dict[str, Any]
    ) -> NotificationModel:
        """Send notification using Strategy pattern."""
        # Handle both string and enum types
        if isinstance(notification_type, str):
            notification_type_enum = NotificationTypeEnum(notification_type)
        else:
            notification_type_enum = notification_type
        strategy: INotificationStrategy = NotificationFactory.create_strategy(notification_type_enum)
        return strategy.send_notification(user_id, data, self.db)
    
    def get_user_notifications(self, user_id: int, skip: int = 0, limit: int = 100) -> List[NotificationModel]:
        """Get all notifications for a user."""
        return self.notification_repository.get_all_by_user(user_id, skip, limit)
    
    def get_unread_notifications(self, user_id: int, skip: int = 0, limit: int = 100) -> List[NotificationModel]:
        """Get unread notifications for a user."""
        return self.notification_repository.get_unread_by_user(user_id, skip, limit)
    
    def mark_notification_as_read(self, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read."""
        notification = self.notification_repository.get_by_id(notification_id)
        if not notification or notification.user_id != user_id:
            return False
        notification.is_read = True
        self.notification_repository.update(notification)
        return True
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        return self.notification_repository.mark_all_as_read(user_id)

