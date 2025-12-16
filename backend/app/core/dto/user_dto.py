"""User DTOs."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from ..models.user import SubscriptionType


class UserCreateDTO(BaseModel):
    """DTO for creating a user."""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserUpdateDTO(BaseModel):
    """DTO for updating a user."""
    full_name: Optional[str] = None
    subscription_type: Optional[SubscriptionType] = None


class UserResponseDTO(BaseModel):
    """DTO for user response."""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    subscription_type: SubscriptionType
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    """DTO for user login."""
    email: EmailStr
    password: str


class TokenResponseDTO(BaseModel):
    """DTO for token response."""
    access_token: str
    token_type: str = "bearer"




