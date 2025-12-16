"""
Subscription routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.subscription_service import SubscriptionService
import logging

logger = logging.getLogger(__name__)

subscriptions_bp = Blueprint('subscriptions', __name__)
subscription_service = SubscriptionService()


@subscriptions_bp.route('', methods=['GET'])
@jwt_required()
def get_user_subscription():
    """Get current user's subscription"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        subscription = subscription_service.get_user_subscription(current_user_id)
        
        if not subscription:
            return jsonify({'message': 'No active subscription', 'subscription': None}), 200
        
        return jsonify({'subscription': subscription}), 200
    
    except Exception as e:
        logger.error(f"Get subscription error: {e}")
        return jsonify({'error': 'Failed to get subscription'}), 500


@subscriptions_bp.route('/tiers', methods=['GET'])
def get_subscription_tiers():
    """Get all available subscription tiers"""
    try:
        tiers = subscription_service.get_all_tiers()
        return jsonify({'tiers': tiers}), 200
    except Exception as e:
        logger.error(f"Get tiers error: {e}")
        return jsonify({'error': 'Failed to get subscription tiers'}), 500


@subscriptions_bp.route('', methods=['POST'])
@jwt_required()
def create_subscription():
    """Create new subscription"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        data = request.get_json()
        
        if not data.get('tier_id'):
            return jsonify({'error': 'tier_id is required'}), 400
        
        subscription = subscription_service.create_subscription(current_user_id, data['tier_id'])
        
        return jsonify({
            'message': 'Subscription created successfully',
            'subscription': subscription
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Create subscription error: {e}")
        return jsonify({'error': 'Failed to create subscription'}), 500

