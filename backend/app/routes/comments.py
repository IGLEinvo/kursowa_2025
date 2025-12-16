"""
Comments routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.middleware.auth import optional_auth
import logging

logger = logging.getLogger(__name__)

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/articles/<int:article_id>/comments', methods=['GET'])
@optional_auth
def get_comments(article_id):
    """Get comments for an article"""
    try:
        with db.get_cursor() as cursor:
            sql = """
                SELECT c.*, u.username, u.first_name, u.last_name
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.article_id = %s AND c.is_approved = TRUE AND c.parent_id IS NULL
                ORDER BY c.created_at DESC
            """
            cursor.execute(sql, (article_id,))
            comments = cursor.fetchall()
            
            # Get replies for each comment
            for comment in comments:
                sql_replies = """
                    SELECT c.*, u.username, u.first_name, u.last_name
                    FROM comments c
                    JOIN users u ON c.user_id = u.id
                    WHERE c.parent_id = %s AND c.is_approved = TRUE
                    ORDER BY c.created_at ASC
                """
                cursor.execute(sql_replies, (comment['id'],))
                comment['replies'] = cursor.fetchall()
            
            return jsonify({'comments': comments}), 200
    
    except Exception as e:
        logger.error(f"Get comments error: {e}")
        return jsonify({'error': 'Failed to get comments'}), 500


@comments_bp.route('/articles/<int:article_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(article_id):
    """Create a new comment"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({'error': 'Comment content is required'}), 400
        
        parent_id = data.get('parent_id')
        
        with db.get_cursor() as cursor:
            sql = """
                INSERT INTO comments (article_id, user_id, content, parent_id, is_approved)
                VALUES (%s, %s, %s, %s, TRUE)
            """
            cursor.execute(sql, (article_id, current_user_id, data['content'], parent_id))
            comment_id = cursor.lastrowid
            
            # Get created comment with user info
            sql_get = """
                SELECT c.*, u.username, u.first_name, u.last_name
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = %s
            """
            cursor.execute(sql_get, (comment_id,))
            comment = cursor.fetchone()
            
            # Get parent comment author (inside cursor context)
            parent_user_id = None
            if parent_id:
                sql_parent = "SELECT user_id FROM comments WHERE id = %s"
                cursor.execute(sql_parent, (parent_id,))
                parent_comment = cursor.fetchone()
                if parent_comment:
                    parent_user_id = parent_comment['user_id']
        
        # Send notification if it's a reply (outside cursor context to avoid nested cursors)
        if parent_id and parent_user_id and parent_user_id != current_user_id:
            try:
                from app.services.notification_service import NotificationService
                notification_service = NotificationService()
                notification_service.create_notification(
                    user_id=parent_user_id,
                    notification_type='comment_reply',
                    title='New Reply to Your Comment',
                    message=data['content'][:100],
                    link=f'/news/{article_id}#comment-{comment_id}'
                )
            except Exception as e:
                logger.warning(f"Failed to create notification: {e}")
                # Don't fail comment creation if notification fails
        
        return jsonify({'comment': comment}), 201
    
    except Exception as e:
        logger.error(f"Create comment error: {e}", exc_info=True)
        error_msg = str(e)
        if 'connection' in error_msg.lower() or 'database' in error_msg.lower():
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        return jsonify({'error': f'Failed to create comment: {error_msg}'}), 500

