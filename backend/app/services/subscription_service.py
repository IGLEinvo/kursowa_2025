"""
Subscription Service - Strategy Pattern for different subscription types
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from app.repositories.user_repository import UserRepository
from app.database import db
import logging

logger = logging.getLogger(__name__)


class SubscriptionStrategy(ABC):
    """Abstract base class for subscription strategies"""
    
    @abstractmethod
    def calculate_price(self, base_price, user):
        """Calculate final price based on user context"""
        pass
    
    @abstractmethod
    def get_features(self):
        """Get subscription features"""
        pass


class FreeSubscriptionStrategy(SubscriptionStrategy):
    """Free subscription strategy"""
    
    def calculate_price(self, base_price, user):
        return 0.00
    
    def get_features(self):
        return {
            "ads": True,
            "exclusive_articles": False,
            "offline_reading": False
        }


class PaidSubscriptionStrategy(SubscriptionStrategy):
    """Paid subscription strategy"""
    
    def calculate_price(self, base_price, user):
        return base_price
    
    def get_features(self):
        return {
            "ads": False,
            "exclusive_articles": True,
            "offline_reading": True
        }


class StudentSubscriptionStrategy(SubscriptionStrategy):
    """Student subscription strategy - 50% discount"""
    
    def calculate_price(self, base_price, user):
        return base_price * 0.5
    
    def get_features(self):
        return {
            "ads": False,
            "exclusive_articles": True,
            "offline_reading": True
        }


class CorporateSubscriptionStrategy(SubscriptionStrategy):
    """Corporate subscription strategy"""
    
    def calculate_price(self, base_price, user):
        return base_price * 5  # Higher price for corporate
    
    def get_features(self):
        return {
            "ads": False,
            "exclusive_articles": True,
            "offline_reading": True,
            "multiple_users": True
        }


class SubscriptionStrategyFactory:
    """Factory Pattern for creating subscription strategies"""
    
    @staticmethod
    def create_strategy(tier_type):
        """Create subscription strategy based on tier type"""
        strategies = {
            'free': FreeSubscriptionStrategy(),
            'paid': PaidSubscriptionStrategy(),
            'student': StudentSubscriptionStrategy(),
            'corporate': CorporateSubscriptionStrategy()
        }
        return strategies.get(tier_type, FreeSubscriptionStrategy())


class SubscriptionService:
    """Service for managing subscriptions"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def get_user_subscription(self, user_id):
        """Get active subscription for user"""
        # Convert to int if string
        if isinstance(user_id, str):
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                logger.error(f"Invalid user_id format: {user_id}")
                return None
        
        with db.get_cursor() as cursor:
            sql = """
                SELECT us.*, st.name as tier_name, st.type as tier_type, st.features
                FROM user_subscriptions us
                JOIN subscription_tiers st ON us.tier_id = st.id
                WHERE us.user_id = %s AND us.is_active = TRUE 
                AND us.end_date > NOW()
                ORDER BY us.end_date DESC
                LIMIT 1
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return result
    
    def create_subscription(self, user_id, tier_id):
        """Create a new subscription"""
        # Convert to int if string
        if isinstance(user_id, str):
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                raise ValueError("Invalid user_id format")
        
        with db.get_cursor() as cursor:
            # Get tier information
            sql_tier = "SELECT * FROM subscription_tiers WHERE id = %s"
            cursor.execute(sql_tier, (tier_id,))
            tier = cursor.fetchone()
            
            if not tier:
                raise ValueError("Invalid subscription tier")
            
            # Calculate end date
            start_date = datetime.now()
            end_date = start_date + timedelta(days=tier['duration_days'])
            
            # Get user
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Use strategy pattern to calculate price
            strategy = SubscriptionStrategyFactory.create_strategy(tier['type'])
            final_price = strategy.calculate_price(float(tier['price']), user)
            
            # Create subscription
            sql = """
                INSERT INTO user_subscriptions (user_id, tier_id, start_date, end_date, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, tier_id, start_date, end_date, True))
            subscription_id = cursor.lastrowid
            
            return {
                'id': subscription_id,
                'tier_name': tier['name'],
                'tier_type': tier['type'],
                'price': final_price,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'features': strategy.get_features()
            }
    
    def has_premium_access(self, user_id):
        """Check if user has premium access"""
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            return False
        
        tier_type = subscription['tier_type']
        return tier_type in ['paid', 'student', 'corporate']
    
    def get_all_tiers(self):
        """Get all available subscription tiers"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM subscription_tiers WHERE is_active = TRUE ORDER BY price"
            cursor.execute(sql)
            return cursor.fetchall()

