"""Notification routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.utils.database import get_db
from app.core.dto.notification_dto import NotificationResponseDTO
from app.api.middleware.auth import get_current_active_user
from app.bll.services.notification_service import NotificationService
from app.dal.models import UserModel

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=List[NotificationResponseDTO])
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    unread_only: bool = Query(False),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user notifications."""
    notification_service = NotificationService(db)
    if unread_only:
        notifications = notification_service.get_unread_notifications(current_user.id, skip, limit)
    else:
        notifications = notification_service.get_user_notifications(current_user.id, skip, limit)
    return notifications


@router.put("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_notification_as_read(
    notification_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    notification_service = NotificationService(db)
    success = notification_service.mark_notification_as_read(notification_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")


@router.put("/read-all", status_code=status.HTTP_204_NO_CONTENT)
async def mark_all_notifications_as_read(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read."""
    notification_service = NotificationService(db)
    notification_service.mark_all_as_read(current_user.id)




