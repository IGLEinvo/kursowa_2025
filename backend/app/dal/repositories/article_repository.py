"""Article repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.dal.models import ArticleModel, ArticleStatusEnum
from app.dal.repositories.base_repository import BaseRepository
from app.core.models.article import ArticleStatus


class ArticleRepository(BaseRepository[ArticleModel]):
    """Article repository implementation."""
    
    def __init__(self, db: Session):
        super().__init__(db, ArticleModel)
    
    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[ArticleModel]:
        """Get articles by category."""
        return self.db.query(ArticleModel).filter(
            and_(
                ArticleModel.category_id == category_id,
                ArticleModel.status == ArticleStatusEnum.PUBLISHED
            )
        ).offset(skip).limit(limit).all()
    
    def get_published(self, skip: int = 0, limit: int = 100) -> List[ArticleModel]:
        """Get all published articles."""
        return self.db.query(ArticleModel).filter(
            ArticleModel.status == ArticleStatusEnum.PUBLISHED
        ).order_by(ArticleModel.published_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_author(self, author_id: int, skip: int = 0, limit: int = 100) -> List[ArticleModel]:
        """Get articles by author."""
        return self.db.query(ArticleModel).filter(
            ArticleModel.author_id == author_id
        ).order_by(ArticleModel.created_at.desc()).offset(skip).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[ArticleModel]:
        """Search articles by query."""
        search_pattern = f"%{query}%"
        return self.db.query(ArticleModel).filter(
            and_(
                ArticleModel.status == ArticleStatusEnum.PUBLISHED,
                or_(
                    ArticleModel.title.like(search_pattern),
                    ArticleModel.content.like(search_pattern),
                    ArticleModel.summary.like(search_pattern)
                )
            )
        ).offset(skip).limit(limit).all()
    
    def get_trending(self, skip: int = 0, limit: int = 10) -> List[ArticleModel]:
        """Get trending articles based on views and likes."""
        return self.db.query(ArticleModel).filter(
            ArticleModel.status == ArticleStatusEnum.PUBLISHED
        ).order_by(
            ArticleModel.views_count.desc(),
            ArticleModel.likes_count.desc()
        ).offset(skip).limit(limit).all()
    
    def get_exclusive(self, skip: int = 0, limit: int = 100) -> List[ArticleModel]:
        """Get exclusive articles."""
        return self.db.query(ArticleModel).filter(
            and_(
                ArticleModel.is_exclusive == True,
                ArticleModel.status == ArticleStatusEnum.PUBLISHED
            )
        ).offset(skip).limit(limit).all()




