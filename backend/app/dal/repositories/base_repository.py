"""Base repository interface and implementation."""
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.core.utils.database import Base

T = TypeVar("T", bound=Base)


class IRepository(Generic[T]):
    """Repository interface following Repository pattern."""
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        raise NotImplementedError
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities."""
        raise NotImplementedError
    
    def create(self, entity: T) -> T:
        """Create a new entity."""
        raise NotImplementedError
    
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        raise NotImplementedError
    
    def delete(self, id: int) -> bool:
        """Delete an entity by ID."""
        raise NotImplementedError


class BaseRepository(IRepository[T]):
    """Base repository implementation."""
    
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities."""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, entity: T) -> T:
        """Create a new entity."""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, id: int) -> bool:
        """Delete an entity by ID."""
        entity = self.get_by_id(id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False




