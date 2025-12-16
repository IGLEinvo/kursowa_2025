"""Article DTOs."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from ..models.article import ArticleStatus


class ArticleCreateDTO(BaseModel):
    """DTO for creating an article."""
    title: str
    content: str
    summary: Optional[str] = None
    category_id: int
    is_exclusive: bool = False
    tags: Optional[List[str]] = None


class ArticleUpdateDTO(BaseModel):
    """DTO for updating an article."""
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[ArticleStatus] = None
    is_exclusive: Optional[bool] = None
    tags: Optional[List[str]] = None


class ArticleResponseDTO(BaseModel):
    """DTO for article response."""
    id: int
    title: str
    content: str
    summary: Optional[str]
    author_id: int
    category_id: int
    status: ArticleStatus
    is_exclusive: bool
    views_count: int
    likes_count: int
    comments_count: int
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    tags: List[str]

    class Config:
        from_attributes = True


class ArticleSearchDTO(BaseModel):
    """DTO for article search."""
    query: Optional[str] = None
    category_id: Optional[int] = None
    author_id: Optional[int] = None
    is_exclusive: Optional[bool] = None
    page: int = 1
    page_size: int = 20




