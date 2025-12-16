"""
Admin routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.auth import admin_required, editor_required
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository
from app.models.article import Article
from app.services.notification_service import NotificationService
from app.database import db
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)
article_repo = ArticleRepository()
category_repo = CategoryRepository()
user_repo = UserRepository()
notification_service = NotificationService()


def slugify(text):
    """Generate URL-friendly slug from text"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


@admin_bp.route('/articles', methods=['GET'])
@editor_required
def list_all_articles():
    """List all articles (admin/editor)"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        status = request.args.get('status')
        offset = (page - 1) * limit
        
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM articles WHERE 1=1"
            params = []
            
            if status:
                sql += " AND status = %s"
                params.append(status)
            
            sql += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            articles = [Article.from_dict(row) for row in results]
            
            return jsonify({
                'articles': [article.to_dict() for article in articles],
                'page': page,
                'limit': limit
            }), 200
    
    except Exception as e:
        logger.error(f"List articles error: {e}")
        return jsonify({'error': 'Failed to list articles'}), 500


@admin_bp.route('/articles/<int:article_id>', methods=['PUT'])
@editor_required
def update_article(article_id):
    """Update article (admin/editor)"""
    try:
        article = article_repo.find_by_id(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            article.title = data['title']
            article.slug = slugify(data['title'])
        if 'content' in data:
            article.content = data['content']
        if 'excerpt' in data:
            article.excerpt = data['excerpt']
        if 'category_id' in data:
            article.category_id = data['category_id']
        if 'is_breaking' in data:
            article.is_breaking = data['is_breaking']
        if 'is_premium' in data:
            article.is_premium = data['is_premium']
        if 'status' in data:
            article.status = data['status']
            if data['status'] == 'published' and not article.published_at:
                article.published_at = datetime.now()
                if article.is_breaking:
                    notification_service.send_breaking_news(article.id, article.title)
        
        article = article_repo.update(article)
        
        return jsonify({'article': article.to_dict()}), 200
    
    except Exception as e:
        logger.error(f"Update article error: {e}")
        return jsonify({'error': 'Failed to update article'}), 500


@admin_bp.route('/articles/<int:article_id>', methods=['DELETE'])
@editor_required
def delete_article(article_id):
    """Delete article (admin/editor)"""
    try:
        success = article_repo.delete(article_id)
        
        if not success:
            return jsonify({'error': 'Article not found'}), 404
        
        return jsonify({'message': 'Article deleted successfully'}), 200
    
    except Exception as e:
        logger.error(f"Delete article error: {e}")
        return jsonify({'error': 'Failed to delete article'}), 500


@admin_bp.route('/categories', methods=['POST'])
@admin_required
def create_category():
    """Create new category (admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Category name is required'}), 400
        
        from app.models.category import Category
        category = Category(
            name=data['name'],
            slug=slugify(data['name']),
            description=data.get('description')
        )
        
        category = category_repo.create(category)
        
        return jsonify({'category': category.to_dict()}), 201
    
    except Exception as e:
        logger.error(f"Create category error: {e}")
        return jsonify({'error': 'Failed to create category'}), 500


@admin_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """Update category (admin only)"""
    try:
        category = category_repo.find_by_id(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            category.name = data['name']
            category.slug = slugify(data['name'])
        if 'description' in data:
            category.description = data['description']
        
        category = category_repo.update(category)
        
        return jsonify({'category': category.to_dict()}), 200
    
    except Exception as e:
        logger.error(f"Update category error: {e}")
        return jsonify({'error': 'Failed to update category'}), 500


@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    """List all users (admin only)"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        offset = (page - 1) * limit
        
        users = user_repo.find_all(limit=limit, offset=offset)
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'page': page,
            'limit': limit
        }), 200
    
    except Exception as e:
        logger.error(f"List users error: {e}")
        return jsonify({'error': 'Failed to list users'}), 500


@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['PUT'])
@admin_required
def toggle_user_active(user_id):
    """Toggle user active status (admin only)"""
    try:
        user = user_repo.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = not user.is_active
        user = user_repo.update(user)
        
        return jsonify({'message': 'User status updated', 'user': user.to_dict()}), 200
    
    except Exception as e:
        logger.error(f"Toggle user active error: {e}")
        return jsonify({'error': 'Failed to update user status'}), 500

