#!/usr/bin/env python3
"""
Script to add a premium user with premium subscription
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import db
from app.models.user import User
from app.repositories.user_repository import UserRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_premium_user():
    """Add premium user and grant premium subscription"""
    try:
        user_repo = UserRepository()
        
        # Check if user already exists
        existing_user = user_repo.find_by_email('premium1@gmail.com')
        if existing_user:
            logger.info(f"User 'premium1' already exists with ID: {existing_user.id}")
            user_id = existing_user.id
        else:
            # Create new user
            logger.info("Creating new premium user...")
            user = User(
                username='premium1',
                email='premium1@gmail.com',
                password_hash=User.hash_password('premium123'),  # Default password
                first_name='Premium',
                last_name='User',
                role='user'
            )
            user = user_repo.create(user)
            user_id = user.id
            logger.info(f"Created user 'premium1' with ID: {user_id}")
        
        # Check if user already has an active premium subscription
        with db.get_cursor() as cursor:
            # Get premium tier ID (type='paid')
            sql_tier = "SELECT id FROM subscription_tiers WHERE type = 'paid' LIMIT 1"
            cursor.execute(sql_tier)
            tier_result = cursor.fetchone()
            
            if not tier_result:
                logger.error("Premium subscription tier not found in database!")
                logger.info("Please run the database schema to create subscription tiers.")
                return False
            
            tier_id = tier_result['id']
            
            # Check existing subscription
            sql_check = """
                SELECT * FROM user_subscriptions 
                WHERE user_id = %s AND tier_id = %s AND is_active = TRUE 
                AND end_date > NOW()
            """
            cursor.execute(sql_check, (user_id, tier_id))
            existing_sub = cursor.fetchone()
            
            if existing_sub:
                logger.info(f"User already has an active premium subscription (expires: {existing_sub['end_date']})")
                return True
            
            # Create premium subscription (1 year)
            start_date = datetime.now()
            end_date = start_date + timedelta(days=365)  # 1 year subscription
            
            sql_insert = """
                INSERT INTO user_subscriptions (user_id, tier_id, start_date, end_date, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (user_id, tier_id, start_date, end_date, True))
            logger.info(f"Premium subscription created successfully!")
            logger.info(f"  User ID: {user_id}")
            logger.info(f"  Start Date: {start_date}")
            logger.info(f"  End Date: {end_date}")
            logger.info(f"  Username: premium1")
            logger.info(f"  Email: premium1@gmail.com")
            logger.info(f"  Password: premium123")
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding premium user: {e}", exc_info=True)
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Adding Premium User")
    print("=" * 60)
    print()
    
    success = add_premium_user()
    
    if success:
        print()
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Premium user created/updated successfully!")
        print()
        print("Login credentials:")
        print("  Username/Email: premium1@gmail.com")
        print("  Password: premium123")
        print()
    else:
        print()
        print("=" * 60)
        print("ERROR!")
        print("=" * 60)
        print("Failed to create premium user. Check the logs above.")
        sys.exit(1)

