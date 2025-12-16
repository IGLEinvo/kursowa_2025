"""Category repository."""
from typing import Optional
from sqlalchemy.orm import Session
from app.dal.models import CategoryModel
from app.dal.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[CategoryModel]):
    """Category repository implementation."""
    
    def __init__(self, db: Session):
        super().__init__(db, CategoryModel)
    
    def get_by_slug(self, slug: str) -> Optional[CategoryModel]:
        """Get category by slug."""
        return self.db.query(CategoryModel).filter(CategoryModel.slug == slug).first()




