"""Recommendation service."""
from typing import List
from sqlalchemy.orm import Session
from app.dal.repositories.article_repository import ArticleRepository
from app.dal.repositories.user_repository import UserRepository
from app.dal.models import ArticleModel, UserModel, LikeModel, SavedArticleModel
from sqlalchemy import func


class RecommendationService:
    """Recommendation service for personalized content."""
    
    def __init__(self, db: Session):
        self.article_repository = ArticleRepository(db)
        self.user_repository = UserRepository(db)
        self.db = db
    
    def get_personalized_recommendations(self, user_id: int, limit: int = 10) -> List[ArticleModel]:
        """Get personalized recommendations for a user."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return []
        
        # Get user's liked article IDs
        liked_article_ids = [row[0] for row in self.db.query(LikeModel.article_id).filter(
            LikeModel.user_id == user_id
        ).all()]
        
        # Get user's saved article IDs
        saved_article_ids = [row[0] for row in self.db.query(SavedArticleModel.article_id).filter(
            SavedArticleModel.user_id == user_id
        ).all()]
        
        # Combine all article IDs user has interacted with
        interacted_article_ids = set(liked_article_ids + saved_article_ids)
        
        # Get categories from liked and saved articles
        if interacted_article_ids:
            user_categories = self.db.query(ArticleModel.category_id).filter(
                ArticleModel.id.in_(interacted_article_ids)
            ).distinct().all()
            category_ids = [cat[0] for cat in user_categories]
        else:
            category_ids = []
        
        # Get recommendations based on user preferences
        if category_ids:
            from app.dal.models import ArticleStatusEnum
            recommendations = self.db.query(ArticleModel).filter(
                ArticleModel.category_id.in_(category_ids),
                ArticleModel.status == ArticleStatusEnum.PUBLISHED,
                ~ArticleModel.id.in_(interacted_article_ids) if interacted_article_ids else True
            ).order_by(
                ArticleModel.views_count.desc(),
                ArticleModel.likes_count.desc()
            ).limit(limit).all()
        else:
            # Fallback to trending articles
            recommendations = self.article_repository.get_trending(0, limit)
        
        return recommendations
    
    def get_trending_articles(self, limit: int = 10) -> List[ArticleModel]:
        """Get trending articles."""
        return self.article_repository.get_trending(0, limit)

