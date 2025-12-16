"""Article routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.utils.database import get_db
from app.core.dto.article_dto import (
    ArticleCreateDTO,
    ArticleUpdateDTO,
    ArticleResponseDTO,
    ArticleSearchDTO
)
from app.api.middleware.auth import get_current_active_user, get_current_admin_user
from app.bll.services.article_service import ArticleService
from app.bll.services.recommendation_service import RecommendationService
from app.dal.models import UserModel, ArticleModel

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=List[ArticleResponseDTO])
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get published articles."""
    article_service = ArticleService(db)
    articles = article_service.get_published_articles(skip, limit)
    return articles


@router.get("/search", response_model=List[ArticleResponseDTO])
async def search_articles(
    query: str = Query(None),
    category_id: int = Query(None),
    author_id: int = Query(None),
    is_exclusive: bool = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Search articles."""
    article_service = ArticleService(db)
    search_data = ArticleSearchDTO(
        query=query,
        category_id=category_id,
        author_id=author_id,
        is_exclusive=is_exclusive,
        page=page,
        page_size=page_size
    )
    articles = article_service.search_articles(search_data)
    return articles


@router.get("/trending", response_model=List[ArticleResponseDTO])
async def get_trending_articles(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending articles."""
    recommendation_service = RecommendationService(db)
    articles = recommendation_service.get_trending_articles(limit)
    return articles


@router.get("/recommendations", response_model=List[ArticleResponseDTO])
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations."""
    recommendation_service = RecommendationService(db)
    articles = recommendation_service.get_personalized_recommendations(current_user.id, limit)
    return articles


@router.get("/{article_id}", response_model=ArticleResponseDTO)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Get article by ID."""
    article_service = ArticleService(db)
    article = article_service.get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    # Increment views
    article_service.increment_views(article_id)
    
    return article


@router.post("", response_model=ArticleResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreateDTO,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new article (requires author role)."""
    # Check if user is an author
    if not current_user.author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an author"
        )
    
    article_service = ArticleService(db)
    try:
        article = article_service.create_article(current_user.author.id, article_data)
        return article
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{article_id}", response_model=ArticleResponseDTO)
async def update_article(
    article_id: int,
    article_data: ArticleUpdateDTO,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an article."""
    article_service = ArticleService(db)
    article = article_service.get_article_by_id(article_id)
    
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    # Check if user is the author or admin
    if not current_user.is_admin and (not current_user.author or article.author_id != current_user.author.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this article"
        )
    
    try:
        updated_article = article_service.update_article(article_id, article_data)
        if not updated_article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        return updated_article
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{article_id}/publish", response_model=ArticleResponseDTO)
async def publish_article(
    article_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Publish an article."""
    article_service = ArticleService(db)
    article = article_service.get_article_by_id(article_id)
    
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    # Check if user is the author or admin
    if not current_user.is_admin and (not current_user.author or article.author_id != current_user.author.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to publish this article"
        )
    
    published_article = article_service.publish_article(article_id)
    if not published_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    return published_article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an article."""
    article_service = ArticleService(db)
    article = article_service.get_article_by_id(article_id)
    
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    # Check if user is the author or admin
    if not current_user.is_admin and (not current_user.author or article.author_id != current_user.author.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this article"
        )
    
    # Delete article (implement in service if needed)
    from app.dal.repositories.article_repository import ArticleRepository
    article_repo = ArticleRepository(db)
    article_repo.delete(article_id)




