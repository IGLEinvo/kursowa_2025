"""Category domain model."""
from datetime import datetime
from typing import Optional


class Category:
    """Category domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        slug: str = "",
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()




