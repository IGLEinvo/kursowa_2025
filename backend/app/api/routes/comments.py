"""Comment routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.utils.database import get_db
from app.core.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO, CommentResponseDTO
from app.api.middleware.auth import get_current_active_user
from app.bll.services.comment_service import CommentService
from app.dal.models import UserModel

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("", response_model=CommentResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreateDTO,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new comment."""
    comment_service = CommentService(db)
    try:
        comment = comment_service.create_comment(current_user.id, comment_data)
        return comment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/article/{article_id}", response_model=List[CommentResponseDTO])
async def get_article_comments(
    article_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get comments for an article."""
    comment_service = CommentService(db)
    comments = comment_service.get_comments_by_article(article_id, skip, limit)
    return comments


@router.put("/{comment_id}", response_model=CommentResponseDTO)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdateDTO,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a comment."""
    comment_service = CommentService(db)
    updated_comment = comment_service.update_comment(comment_id, current_user.id, comment_data)
    if not updated_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return updated_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a comment."""
    comment_service = CommentService(db)
    success = comment_service.delete_comment(comment_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")




