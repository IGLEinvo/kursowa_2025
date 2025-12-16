"""Author domain model."""
from datetime import datetime
from typing import Optional


class Author:
    """Author domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        bio: Optional[str] = None,
        profile_image_url: Optional[str] = None,
        articles_count: int = 0,
        followers_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.bio = bio
        self.profile_image_url = profile_image_url
        self.articles_count = articles_count
        self.followers_count = followers_count
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()




