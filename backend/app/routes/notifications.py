"""
Notification routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import NotificationService
from app.database import db
import logging

logger = logging.getLogger(__name__)

notifications_bp = Blueprint('notifications', __name__)
notification_service = NotificationService()


@notifications_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user notifications"""
    try:
        current_user_id = get_jwt_identity()
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 50))
        
        notifications = notification_service.get_user_notifications(
            current_user_id,
            limit=limit,
            unread_only=unread_only
        )
        
        return jsonify({'notifications': notifications}), 200
    
    except Exception as e:
        logger.error(f"Get notifications error: {e}")
        return jsonify({'error': 'Failed to get notifications'}), 500


@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        current_user_id = get_jwt_identity()
        
        success = notification_service.mark_as_read(notification_id, current_user_id)
        
        if not success:
            return jsonify({'error': 'Notification not found'}), 404
        
        return jsonify({'message': 'Notification marked as read'}), 200
    
    except Exception as e:
        logger.error(f"Mark notification read error: {e}")
        return jsonify({'error': 'Failed to mark notification as read'}), 500


@notifications_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    """Get user notification preferences"""
    try:
        current_user_id = get_jwt_identity()
        
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM notification_preferences WHERE user_id = %s"
            cursor.execute(sql, (current_user_id,))
            prefs = cursor.fetchone()
            
            if not prefs:
                # Create default preferences
                sql_insert = """
                    INSERT INTO notification_preferences 
                    (user_id, breaking_news, daily_digest, author_alerts, comment_replies)
                    VALUES (%s, TRUE, TRUE, TRUE, TRUE)
                """
                cursor.execute(sql_insert, (current_user_id,))
                prefs = {
                    'user_id': current_user_id,
                    'breaking_news': True,
                    'daily_digest': True,
                    'author_alerts': True,
                    'comment_replies': True
                }
            
            return jsonify({'preferences': prefs}), 200
    
    except Exception as e:
        logger.error(f"Get preferences error: {e}")
        return jsonify({'error': 'Failed to get notification preferences'}), 500


@notifications_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_notification_preferences():
    """Update user notification preferences"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        with db.get_cursor() as cursor:
            # Check if preferences exist
            sql_check = "SELECT * FROM notification_preferences WHERE user_id = %s"
            cursor.execute(sql_check, (current_user_id,))
            
            if cursor.fetchone():
                # Update existing
                sql_update = """
                    UPDATE notification_preferences
                    SET breaking_news = %s, daily_digest = %s,
                        author_alerts = %s, comment_replies = %s
                    WHERE user_id = %s
                """
                cursor.execute(sql_update, (
                    data.get('breaking_news', True),
                    data.get('daily_digest', True),
                    data.get('author_alerts', True),
                    data.get('comment_replies', True),
                    current_user_id
                ))
            else:
                # Create new
                sql_insert = """
                    INSERT INTO notification_preferences 
                    (user_id, breaking_news, daily_digest, author_alerts, comment_replies)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (
                    current_user_id,
                    data.get('breaking_news', True),
                    data.get('daily_digest', True),
                    data.get('author_alerts', True),
                    data.get('comment_replies', True)
                ))
            
            return jsonify({'message': 'Preferences updated'}), 200
    
    except Exception as e:
        logger.error(f"Update preferences error: {e}")
        return jsonify({'error': 'Failed to update preferences'}), 500

