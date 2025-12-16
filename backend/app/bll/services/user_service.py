"""User service."""
from typing import Optional
from sqlalchemy.orm import Session
from app.dal.repositories.user_repository import UserRepository
from app.dal.models import UserModel
from app.core.models.user import User, SubscriptionType
from app.core.dto.user_dto import UserCreateDTO, UserUpdateDTO
from app.core.utils.security import get_password_hash, verify_password


class UserService:
    """User service implementation."""
    
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.db = db
    
    def register_user(self, user_data: UserCreateDTO) -> UserModel:
        """Register a new user."""
        # Check if user already exists
        if self.user_repository.get_by_email(user_data.email):
            raise ValueError("User with this email already exists")
        if self.user_repository.get_by_username(user_data.username):
            raise ValueError("User with this username already exists")
        
        # Create user
        user = UserModel(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            subscription_type=SubscriptionType.FREE.value
        )
        return self.user_repository.create(user)
    
    def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        """Authenticate a user."""
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        if not user.is_active:
            return None
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """Get user by ID."""
        return self.user_repository.get_by_id(user_id)
    
    def update_user(self, user_id: int, user_data: UserUpdateDTO) -> Optional[UserModel]:
        """Update user information."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.subscription_type is not None:
            user.subscription_type = user_data.subscription_type.value
        
        return self.user_repository.update(user)
    
    def update_subscription(self, user_id: int, subscription_type: SubscriptionType) -> Optional[UserModel]:
        """Update user subscription."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        user.subscription_type = subscription_type.value
        return self.user_repository.update(user)




