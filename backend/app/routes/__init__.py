from .auth import auth_bp
from .news import news_bp
from .subscriptions import subscriptions_bp
from .notifications import notifications_bp
from .users import users_bp
from .admin import admin_bp

__all__ = ['auth_bp', 'news_bp', 'subscriptions_bp', 'notifications_bp', 'users_bp', 'admin_bp']

