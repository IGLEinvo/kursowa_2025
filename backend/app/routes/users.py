"""
User routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.user_repository import UserRepository
from app.repositories.article_repository import ArticleRepository
from app.database import db
import logging

logger = logging.getLogger(__name__)

users_bp = Blueprint('users', __name__)
user_repo = UserRepository()
article_repo = ArticleRepository()


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = user_repo.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        return jsonify({'error': 'Failed to get profile'}), 500


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        user = user_repo.find_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'username' in data:
            # Check if username is taken
            existing = user_repo.find_by_username(data['username'])
            if existing and existing.id != current_user_id:
                return jsonify({'error': 'Username already taken'}), 400
            user.username = data['username']
        
        user = user_repo.update(user)
        
        return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200
    
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        return jsonify({'error': 'Failed to update profile'}), 500


@users_bp.route('/saved', methods=['GET'])
@jwt_required()
def get_saved_articles():
    """Get user's saved articles"""
    try:
        current_user_id = get_jwt_identity()
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit
        
        with db.get_cursor() as cursor:
            sql = """
                SELECT a.* FROM articles a
                JOIN saved_articles sa ON a.id = sa.article_id
                WHERE sa.user_id = %s
                ORDER BY sa.created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (current_user_id, limit, offset))
            results = cursor.fetchall()
            
            articles = [article_repo.find_by_id(row['id']) for row in results]
            
            return jsonify({
                'articles': [article.to_dict() for article in articles if article],
                'page': page,
                'limit': limit
            }), 200
    
    except Exception as e:
        logger.error(f"Get saved articles error: {e}")
        return jsonify({'error': 'Failed to get saved articles'}), 500


@users_bp.route('/authors/<int:author_id>/follow', methods=['POST'])
@jwt_required()
def follow_author(author_id):
    """Follow an author"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if author exists
        author = user_repo.find_by_id(author_id)
        if not author:
            return jsonify({'error': 'Author not found'}), 404
        
        with db.get_cursor() as cursor:
            # Check if already following
            sql_check = """
                SELECT * FROM author_subscriptions
                WHERE user_id = %s AND author_id = %s
            """
            cursor.execute(sql_check, (current_user_id, author_id))
            if cursor.fetchone():
                return jsonify({'error': 'Already following this author'}), 400
            
            # Follow author
            sql_insert = """
                INSERT INTO author_subscriptions (user_id, author_id)
                VALUES (%s, %s)
            """
            cursor.execute(sql_insert, (current_user_id, author_id))
            
            return jsonify({'message': 'Author followed successfully'}), 201
    
    except Exception as e:
        logger.error(f"Follow author error: {e}")
        return jsonify({'error': 'Failed to follow author'}), 500


@users_bp.route('/authors/<int:author_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_author(author_id):
    """Unfollow an author"""
    try:
        current_user_id = get_jwt_identity()
        
        with db.get_cursor() as cursor:
            sql_delete = """
                DELETE FROM author_subscriptions
                WHERE user_id = %s AND author_id = %s
            """
            cursor.execute(sql_delete, (current_user_id, author_id))
            
            if cursor.rowcount == 0:
                return jsonify({'error': 'Not following this author'}), 400
            
            return jsonify({'message': 'Author unfollowed successfully'}), 200
    
    except Exception as e:
        logger.error(f"Unfollow author error: {e}")
        return jsonify({'error': 'Failed to unfollow author'}), 500

