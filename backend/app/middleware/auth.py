"""
Authentication middleware - Decorator Pattern
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.repositories.user_repository import UserRepository
import logging

logger = logging.getLogger(__name__)


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user_repo = UserRepository()
        user = user_repo.find_by_id(current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def editor_required(f):
    """Decorator to require editor or admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user_repo = UserRepository()
        user = user_repo.find_by_id(current_user_id)
        
        if not user or user.role not in ['admin', 'editor']:
            return jsonify({'error': 'Editor access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def premium_required(f):
    """Decorator to require premium subscription"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        from app.services.subscription_service import SubscriptionService
        
        current_user_id = get_jwt_identity()
        subscription_service = SubscriptionService()
        
        if not subscription_service.has_premium_access(current_user_id):
            return jsonify({'error': 'Premium subscription required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def optional_auth(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
        except:
            pass
        return f(*args, **kwargs)
    
    return decorated_function

