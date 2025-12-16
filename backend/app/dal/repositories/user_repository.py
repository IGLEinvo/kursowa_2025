"""User repository."""
from typing import Optional
from sqlalchemy.orm import Session
from app.dal.models import UserModel
from app.dal.repositories.base_repository import BaseRepository
from app.core.models.user import User, SubscriptionType


class UserRepository(BaseRepository[UserModel]):
    """User repository implementation."""
    
    def __init__(self, db: Session):
        super().__init__(db, UserModel)
    
    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Get user by email."""
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username."""
        return self.db.query(UserModel).filter(UserModel.username == username).first()
    
    def get_active_users(self, skip: int = 0, limit: int = 100):
        """Get all active users."""
        return self.db.query(UserModel).filter(
            UserModel.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_subscription_type(self, subscription_type: SubscriptionType, skip: int = 0, limit: int = 100):
        """Get users by subscription type."""
        return self.db.query(UserModel).filter(
            UserModel.subscription_type == subscription_type.value
        ).offset(skip).limit(limit).all()




