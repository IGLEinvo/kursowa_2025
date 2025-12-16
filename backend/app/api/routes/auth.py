"""Authentication routes."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.utils.database import get_db
from app.core.utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dto.user_dto import UserCreateDTO, UserLoginDTO, UserResponseDTO, TokenResponseDTO
from app.bll.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    """Register a new user."""
    user_service = UserService(db)
    try:
        user = user_service.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponseDTO)
async def login(credentials: UserLoginDTO, db: Session = Depends(get_db)):
    """Login user and get access token."""
    user_service = UserService(db)
    user = user_service.authenticate_user(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}




