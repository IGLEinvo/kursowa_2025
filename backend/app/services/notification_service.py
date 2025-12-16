"""
Notification Service - Observer Pattern
"""
from abc import ABC, abstractmethod
from typing import List
from app.database import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NotificationObserver(ABC):
    """Abstract observer interface"""
    
    @abstractmethod
    def notify(self, notification_data):
        """Handle notification"""
        pass


class EmailNotificationObserver(NotificationObserver):
    """Email notification observer"""
    
    def notify(self, notification_data):
        logger.info(f"Email notification sent: {notification_data}")
        # In production, would send actual email
        pass


class PushNotificationObserver(NotificationObserver):
    """Push notification observer"""
    
    def notify(self, notification_data):
        logger.info(f"Push notification sent: {notification_data}")
        # In production, would send push notification
        pass


class NotificationSubject:
    """Subject class for Observer pattern"""
    
    def __init__(self):
        self._observers: List[NotificationObserver] = []
    
    def attach(self, observer: NotificationObserver):
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: NotificationObserver):
        """Detach an observer"""
        self._observers.remove(observer)
    
    def notify_observers(self, notification_data):
        """Notify all observers"""
        for observer in self._observers:
            try:
                observer.notify(notification_data)
            except Exception as e:
                logger.error(f"Error notifying observer: {e}")


class NotificationService(NotificationSubject):
    """Service for managing notifications"""
    
    def __init__(self):
        super().__init__()
        # Attach default observers
        self.attach(EmailNotificationObserver())
        self.attach(PushNotificationObserver())
    
    def create_notification(self, user_id, notification_type, title, message, link=None):
        """Create and store notification"""
        with db.get_cursor() as cursor:
            sql = """
                INSERT INTO notifications (user_id, type, title, message, link, is_read)
                VALUES (%s, %s, %s, %s, %s, FALSE)
            """
            cursor.execute(sql, (user_id, notification_type, title, message, link))
            notification_id = cursor.lastrowid
            
            # Notify observers
            notification_data = {
                'id': notification_id,
                'user_id': user_id,
                'type': notification_type,
                'title': title,
                'message': message,
                'link': link
            }
            self.notify_observers(notification_data)
            
            return notification_id
    
    def get_user_notifications(self, user_id, limit=50, unread_only=False):
        """Get notifications for user"""
        with db.get_cursor() as cursor:
            sql = """
                SELECT * FROM notifications
                WHERE user_id = %s
            """
            params = [user_id]
            
            if unread_only:
                sql += " AND is_read = FALSE"
            
            sql += " ORDER BY created_at DESC LIMIT %s"
            params.append(limit)
            
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def mark_as_read(self, notification_id, user_id):
        """Mark notification as read"""
        with db.get_cursor() as cursor:
            sql = """
                UPDATE notifications 
                SET is_read = TRUE 
                WHERE id = %s AND user_id = %s
            """
            cursor.execute(sql, (notification_id, user_id))
            return cursor.rowcount > 0
    
    def send_breaking_news(self, article_id, article_title):
        """Send breaking news notification to all users with preference enabled"""
        with db.get_cursor() as cursor:
            # Get users who want breaking news notifications
            sql = """
                SELECT u.id FROM users u
                LEFT JOIN notification_preferences np ON u.id = np.user_id
                WHERE (np.breaking_news = TRUE OR np.breaking_news IS NULL)
                AND u.is_active = TRUE
            """
            cursor.execute(sql)
            users = cursor.fetchall()
            
            for user in users:
                self.create_notification(
                    user_id=user['id'],
                    notification_type='breaking_news',
                    title='Breaking News',
                    message=article_title,
                    link=f'/news/{article_id}'
                )
    
    def send_daily_digest(self, user_id):
        """Send daily digest notification"""
        # Get top articles from last 24 hours
        with db.get_cursor() as cursor:
            sql = """
                SELECT id, title FROM articles
                WHERE status = 'published' 
                AND published_at >= DATE_SUB(NOW(), INTERVAL 1 DAY)
                ORDER BY views_count DESC
                LIMIT 5
            """
            cursor.execute(sql)
            articles = cursor.fetchall()
            
            if articles:
                article_titles = [article['title'] for article in articles]
                message = f"Top stories today: {'; '.join(article_titles[:3])}"
                
                self.create_notification(
                    user_id=user_id,
                    notification_type='daily_digest',
                    title='Daily News Digest',
                    message=message,
                    link='/news'
                )
    
    def send_author_alert(self, user_id, author_id, article_id, article_title):
        """Send notification about new article from followed author"""
        self.create_notification(
            user_id=user_id,
            notification_type='author_alert',
            title='New Article from Followed Author',
            message=article_title,
            link=f'/news/{article_id}'
        )

