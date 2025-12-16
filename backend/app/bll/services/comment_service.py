"""Comment service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.dal.repositories.comment_repository import CommentRepository
from app.dal.repositories.article_repository import ArticleRepository
from app.dal.models import CommentModel, ArticleModel
from app.core.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO


class CommentService:
    """Comment service implementation."""
    
    def __init__(self, db: Session):
        self.comment_repository = CommentRepository(db)
        self.article_repository = ArticleRepository(db)
        self.db = db
    
    def create_comment(self, user_id: int, comment_data: CommentCreateDTO) -> CommentModel:
        """Create a new comment."""
        # Verify article exists
        article = self.article_repository.get_by_id(comment_data.article_id)
        if not article:
            raise ValueError("Article not found")
        
        # Create comment
        comment = CommentModel(
            content=comment_data.content,
            user_id=user_id,
            article_id=comment_data.article_id,
            parent_id=comment_data.parent_id
        )
        comment = self.comment_repository.create(comment)
        
        # Update article comments count
        article.comments_count += 1
        self.article_repository.update(article)
        
        return comment
    
    def get_comments_by_article(self, article_id: int, skip: int = 0, limit: int = 100) -> List[CommentModel]:
        """Get comments for an article."""
        return self.comment_repository.get_by_article(article_id, skip, limit)
    
    def update_comment(self, comment_id: int, user_id: int, comment_data: CommentUpdateDTO) -> Optional[CommentModel]:
        """Update a comment."""
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment or comment.user_id != user_id:
            return None
        
        comment.content = comment_data.content
        return self.comment_repository.update(comment)
    
    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        """Delete a comment."""
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment or comment.user_id != user_id:
            return False
        
        # Update article comments count
        article = self.article_repository.get_by_id(comment.article_id)
        if article:
            article.comments_count -= 1
            self.article_repository.update(article)
        
        return self.comment_repository.delete(comment_id)




