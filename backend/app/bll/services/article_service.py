"""Article service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.dal.repositories.article_repository import ArticleRepository
from app.dal.repositories.category_repository import CategoryRepository
from app.dal.models import ArticleModel, ArticleStatusEnum, ArticleTagModel
from app.core.models.article import ArticleStatus
from app.core.dto.article_dto import ArticleCreateDTO, ArticleUpdateDTO, ArticleSearchDTO


class ArticleService:
    """Article service implementation."""
    
    def __init__(self, db: Session):
        self.article_repository = ArticleRepository(db)
        self.category_repository = CategoryRepository(db)
        self.db = db
    
    def create_article(self, author_id: int, article_data: ArticleCreateDTO) -> ArticleModel:
        """Create a new article."""
        # Verify category exists
        category = self.category_repository.get_by_id(article_data.category_id)
        if not category:
            raise ValueError("Category not found")
        
        # Create article
        article = ArticleModel(
            title=article_data.title,
            content=article_data.content,
            summary=article_data.summary,
            author_id=author_id,
            category_id=article_data.category_id,
            is_exclusive=article_data.is_exclusive,
            status=ArticleStatusEnum.DRAFT
        )
        article = self.article_repository.create(article)
        
        # Add tags
        if article_data.tags:
            for tag in article_data.tags:
                article_tag = ArticleTagModel(article_id=article.id, tag=tag)
                self.db.add(article_tag)
        self.db.commit()
        self.db.refresh(article)
        
        return article
    
    def get_article_by_id(self, article_id: int) -> Optional[ArticleModel]:
        """Get article by ID."""
        return self.article_repository.get_by_id(article_id)
    
    def update_article(self, article_id: int, article_data: ArticleUpdateDTO) -> Optional[ArticleModel]:
        """Update an article."""
        article = self.article_repository.get_by_id(article_id)
        if not article:
            return None
        
        if article_data.title is not None:
            article.title = article_data.title
        if article_data.content is not None:
            article.content = article_data.content
        if article_data.summary is not None:
            article.summary = article_data.summary
        if article_data.category_id is not None:
            category = self.category_repository.get_by_id(article_data.category_id)
            if not category:
                raise ValueError("Category not found")
            article.category_id = article_data.category_id
        if article_data.status is not None:
            article.status = ArticleStatusEnum(article_data.status.value)
        if article_data.is_exclusive is not None:
            article.is_exclusive = article_data.is_exclusive
        
        # Update tags if provided
        if article_data.tags is not None:
            # Remove existing tags
            for tag in article.tags:
                self.db.delete(tag)
            # Add new tags
            for tag in article_data.tags:
                article_tag = ArticleTagModel(article_id=article.id, tag=tag)
                self.db.add(article_tag)
        
        return self.article_repository.update(article)
    
    def publish_article(self, article_id: int) -> Optional[ArticleModel]:
        """Publish an article."""
        article = self.article_repository.get_by_id(article_id)
        if not article:
            return None
        
        from datetime import datetime
        article.status = ArticleStatusEnum.PUBLISHED
        article.published_at = datetime.utcnow()
        return self.article_repository.update(article)
    
    def get_published_articles(self, skip: int = 0, limit: int = 20) -> List[ArticleModel]:
        """Get published articles."""
        return self.article_repository.get_published(skip, limit)
    
    def get_articles_by_category(self, category_id: int, skip: int = 0, limit: int = 20) -> List[ArticleModel]:
        """Get articles by category."""
        return self.article_repository.get_by_category(category_id, skip, limit)
    
    def search_articles(self, search_data: ArticleSearchDTO) -> List[ArticleModel]:
        """Search articles."""
        skip = (search_data.page - 1) * search_data.page_size
        limit = search_data.page_size
        
        if search_data.query:
            articles = self.article_repository.search(search_data.query, skip, limit)
        else:
            articles = self.article_repository.get_published(skip, limit)
        
        # Apply filters
        if search_data.category_id:
            articles = [a for a in articles if a.category_id == search_data.category_id]
        if search_data.author_id:
            articles = [a for a in articles if a.author_id == search_data.author_id]
        if search_data.is_exclusive is not None:
            articles = [a for a in articles if a.is_exclusive == search_data.is_exclusive]
        
        return articles
    
    def increment_views(self, article_id: int) -> None:
        """Increment article views."""
        article = self.article_repository.get_by_id(article_id)
        if article:
            article.views_count += 1
            self.article_repository.update(article)
    
    def get_trending_articles(self, limit: int = 10) -> List[ArticleModel]:
        """Get trending articles."""
        return self.article_repository.get_trending(0, limit)




