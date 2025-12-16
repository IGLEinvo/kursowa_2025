"""SavedArticle domain model."""
from datetime import datetime
from typing import Optional


class SavedArticle:
    """SavedArticle domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        article_id: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.article_id = article_id
        self.created_at = created_at or datetime.utcnow()




