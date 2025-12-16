"""Comment domain model."""
from datetime import datetime
from typing import Optional


class Comment:
    """Comment domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        content: str = "",
        user_id: int = 0,
        article_id: int = 0,
        parent_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.content = content
        self.user_id = user_id
        self.article_id = article_id
        self.parent_id = parent_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def is_reply(self) -> bool:
        """Check if comment is a reply to another comment."""
        return self.parent_id is not None




