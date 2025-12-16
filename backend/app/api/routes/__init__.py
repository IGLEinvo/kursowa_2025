"""API routes package."""
from .auth import router as auth_router
from .users import router as users_router
from .articles import router as articles_router
from .comments import router as comments_router
from .notifications import router as notifications_router
from .admin import router as admin_router

__all__ = [
    "auth_router",
    "users_router",
    "articles_router",
    "comments_router",
    "notifications_router",
    "admin_router",
]




