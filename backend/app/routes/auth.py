"""
Authentication routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.repositories.user_repository import UserRepository
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)
user_repo = UserRepository()


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if user_repo.find_by_email(data['email']):
            return jsonify({'error': 'Email already registered'}), 400
        
        if user_repo.find_by_username(data['username']):
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=User.hash_password(data['password']),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role='user'
        )
        
        user = user_repo.create(user)
        
        # Create access token (identity must be a string)
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
    
    except Exception as e:
        logger.error(f"Registration error: {e}", exc_info=True)
        error_msg = str(e)
        if 'Access denied' in error_msg or 'password' in error_msg.lower():
            return jsonify({'error': 'Database connection failed. Please check database credentials.'}), 500
        return jsonify({'error': f'Registration failed: {error_msg}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = user_repo.find_by_email(data['email'])
        
        if not user or not user.verify_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Create access token (identity must be a string)
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        current_user_id = get_jwt_identity()
        user = user_repo.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    
    except Exception as e:
        logger.error(f"Get user error: {e}")
        return jsonify({'error': 'Failed to get user'}), 500

