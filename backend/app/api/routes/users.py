"""User routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.utils.database import get_db
from app.core.dto.user_dto import UserResponseDTO, UserUpdateDTO
from app.api.middleware.auth import get_current_active_user
from app.bll.services.user_service import UserService
from app.dal.models import UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponseDTO)
async def get_current_user_profile(
    current_user: UserModel = Depends(get_current_active_user)
):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponseDTO)
async def update_current_user_profile(
    user_data: UserUpdateDTO,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    user_service = UserService(db)
    updated_user = user_service.update_user(current_user.id, user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user by ID."""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user




