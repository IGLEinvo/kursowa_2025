"""Comment DTOs."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CommentCreateDTO(BaseModel):
    """DTO for creating a comment."""
    content: str
    article_id: int
    parent_id: Optional[int] = None


class CommentUpdateDTO(BaseModel):
    """DTO for updating a comment."""
    content: str


class CommentResponseDTO(BaseModel):
    """DTO for comment response."""
    id: int
    content: str
    user_id: int
    article_id: int
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




