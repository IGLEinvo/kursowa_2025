"""
User preferences routes - Favorite categories
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.repositories.category_repository import CategoryRepository
import logging

logger = logging.getLogger(__name__)

preferences_bp = Blueprint('preferences', __name__)
category_repo = CategoryRepository()


@preferences_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_favorite_categories():
    """Get user's favorite categories"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        with db.get_cursor() as cursor:
            sql = """
                SELECT c.*, up.preference_score
                FROM categories c
                JOIN user_preferences up ON c.id = up.category_id
                WHERE up.user_id = %s
                ORDER BY up.preference_score DESC, c.name ASC
            """
            cursor.execute(sql, (current_user_id,))
            results = cursor.fetchall()
            
            return jsonify({
                'favorite_categories': results,
                'count': len(results)
            }), 200
    
    except Exception as e:
        logger.error(f"Get favorite categories error: {e}", exc_info=True)
        error_msg = str(e)
        if 'connection' in error_msg.lower() or 'database' in error_msg.lower():
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        return jsonify({'error': f'Failed to get favorite categories: {error_msg}'}), 500


@preferences_bp.route('/categories', methods=['POST'])
@jwt_required()
def add_favorite_category():
    """Add a category to favorites"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        data = request.get_json() or {}
        
        if not data.get('category_id'):
            return jsonify({'error': 'category_id is required'}), 400
        
        try:
            category_id = int(data['category_id'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid category_id format'}), 400
        
        # Verify category exists
        category = category_repo.find_by_id(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        with db.get_cursor() as cursor:
            # Check if already in favorites
            sql_check = """
                SELECT * FROM user_preferences
                WHERE user_id = %s AND category_id = %s
            """
            cursor.execute(sql_check, (current_user_id, category_id))
            if cursor.fetchone():
                return jsonify({'error': 'Category already in favorites'}), 400
            
            # Add to favorites with default score
            sql_insert = """
                INSERT INTO user_preferences (user_id, category_id, preference_score)
                VALUES (%s, %s, 1.0)
            """
            cursor.execute(sql_insert, (current_user_id, category_id))
            
            return jsonify({
                'message': 'Category added to favorites',
                'category': category.to_dict()
            }), 201
    
    except ValueError as e:
        logger.error(f"Add favorite category validation error: {e}")
        return jsonify({'error': f'Invalid data: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Add favorite category error: {e}", exc_info=True)
        error_msg = str(e)
        if 'duplicate' in error_msg.lower() or 'UNIQUE' in error_msg.upper():
            return jsonify({'error': 'Category already in favorites'}), 400
        return jsonify({'error': f'Failed to add favorite category: {error_msg}'}), 500


@preferences_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite_category(category_id):
    """Remove a category from favorites"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        with db.get_cursor() as cursor:
            sql_delete = """
                DELETE FROM user_preferences
                WHERE user_id = %s AND category_id = %s
            """
            cursor.execute(sql_delete, (current_user_id, category_id))
            
            if cursor.rowcount == 0:
                return jsonify({'error': 'Category not in favorites'}), 404
            
            return jsonify({'message': 'Category removed from favorites'}), 200
    
    except Exception as e:
        logger.error(f"Remove favorite category error: {e}")
        return jsonify({'error': 'Failed to remove favorite category'}), 500


@preferences_bp.route('/categories/bulk', methods=['POST'])
@jwt_required()
def update_favorite_categories():
    """Update favorite categories in bulk"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        data = request.get_json()
        
        category_ids = data.get('category_ids', [])
        if not isinstance(category_ids, list):
            return jsonify({'error': 'category_ids must be a list'}), 400
        
        with db.get_cursor() as cursor:
            # Remove all existing favorites
            sql_delete = "DELETE FROM user_preferences WHERE user_id = %s"
            cursor.execute(sql_delete, (current_user_id,))
            
            # Add new favorites
            if category_ids:
                sql_insert = """
                    INSERT INTO user_preferences (user_id, category_id, preference_score)
                    VALUES (%s, %s, 1.0)
                """
                for category_id in category_ids:
                    cursor.execute(sql_insert, (current_user_id, int(category_id)))
            
            return jsonify({
                'message': 'Favorite categories updated',
                'count': len(category_ids)
            }), 200
    
    except Exception as e:
        logger.error(f"Update favorite categories error: {e}")
        return jsonify({'error': 'Failed to update favorite categories'}), 500

