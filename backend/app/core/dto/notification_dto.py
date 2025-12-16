"""Notification DTOs."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from ..models.notification import NotificationType


class NotificationResponseDTO(BaseModel):
    """DTO for notification response."""
    id: int
    user_id: int
    notification_type: NotificationType
    title: str
    message: str
    article_id: Optional[int]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True




