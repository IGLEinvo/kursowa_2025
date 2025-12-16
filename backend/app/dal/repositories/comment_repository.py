"""Comment repository."""
from typing import List
from sqlalchemy.orm import Session
from app.dal.models import CommentModel
from app.dal.repositories.base_repository import BaseRepository


class CommentRepository(BaseRepository[CommentModel]):
    """Comment repository implementation."""
    
    def __init__(self, db: Session):
        super().__init__(db, CommentModel)
    
    def get_by_article(self, article_id: int, skip: int = 0, limit: int = 100) -> List[CommentModel]:
        """Get comments by article."""
        return self.db.query(CommentModel).filter(
            CommentModel.article_id == article_id,
            CommentModel.parent_id.is_(None)
        ).order_by(CommentModel.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_replies(self, parent_id: int) -> List[CommentModel]:
        """Get replies to a comment."""
        return self.db.query(CommentModel).filter(
            CommentModel.parent_id == parent_id
        ).order_by(CommentModel.created_at.asc()).all()




