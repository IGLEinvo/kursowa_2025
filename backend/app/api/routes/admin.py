"""Admin routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.utils.database import get_db
from app.core.dto.user_dto import UserResponseDTO
from app.core.dto.article_dto import ArticleResponseDTO
from app.api.middleware.auth import get_current_admin_user
from app.bll.services.user_service import UserService
from app.bll.services.article_service import ArticleService
from app.dal.repositories.category_repository import CategoryRepository
from app.dal.models import UserModel, CategoryModel
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])


class CategoryCreateDTO(BaseModel):
    """DTO for creating a category."""
    name: str
    slug: str
    description: str = None


@router.get("/users", response_model=List[UserResponseDTO])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)."""
    user_service = UserService(db)
    users = user_service.user_repository.get_all(skip, limit)
    return users


@router.get("/articles", response_model=List[ArticleResponseDTO])
async def get_all_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all articles (admin only)."""
    article_service = ArticleService(db)
    from app.dal.repositories.article_repository import ArticleRepository
    article_repo = ArticleRepository(db)
    articles = article_repo.get_all(skip, limit)
    return articles


@router.post("/categories", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreateDTO,
    current_user: UserModel = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new category (admin only)."""
    category_repo = CategoryRepository(db)
    # Check if category already exists
    existing = category_repo.get_by_slug(category_data.slug)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    
    from app.dal.models import CategoryModel
    category = CategoryModel(
        name=category_data.name,
        slug=category_data.slug,
        description=category_data.description
    )
    category = category_repo.create(category)
    return {"id": category.id, "name": category.name, "slug": category.slug}


@router.get("/categories", response_model=List[dict])
async def get_all_categories(
    current_user: UserModel = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all categories (admin only)."""
    category_repo = CategoryRepository(db)
    categories = category_repo.get_all()
    return [{"id": c.id, "name": c.name, "slug": c.slug, "description": c.description} for c in categories]


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete yourself")
    
    user_service = UserService(db)
    success = user_service.user_repository.delete(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")




