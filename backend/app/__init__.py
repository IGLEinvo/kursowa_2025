"""
Flask application initialization
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize extensions
jwt = JWTManager()
cors = CORS()


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config)
    
    # JWT Configuration
    from datetime import timedelta
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    # Convert seconds to timedelta - Flask-JWT-Extended accepts timedelta or False
    if config.JWT_ACCESS_TOKEN_EXPIRES:
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=config.JWT_ACCESS_TOKEN_EXPIRES)
    else:
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Never expire (for development)
    
    # Initialize extensions
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from app.routes import auth_bp, news_bp, subscriptions_bp, notifications_bp, admin_bp, users_bp
    from app.routes.comments import comments_bp
    from app.routes.preferences import preferences_bp
    app.register_blueprint(auth_bp, url_prefix=f'{config.API_PREFIX}/auth')
    app.register_blueprint(news_bp, url_prefix=f'{config.API_PREFIX}/news')
    app.register_blueprint(subscriptions_bp, url_prefix=f'{config.API_PREFIX}/subscriptions')
    app.register_blueprint(notifications_bp, url_prefix=f'{config.API_PREFIX}/notifications')
    app.register_blueprint(admin_bp, url_prefix=f'{config.API_PREFIX}/admin')
    app.register_blueprint(users_bp, url_prefix=f'{config.API_PREFIX}/users')
    app.register_blueprint(comments_bp, url_prefix=f'{config.API_PREFIX}/comments')
    app.register_blueprint(preferences_bp, url_prefix=f'{config.API_PREFIX}/preferences')
    
    @app.route('/')
    def index():
        return {'message': 'Online News Newspaper API', 'version': '1.0.0'}
    
    from flask import jsonify
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        import traceback
        try:
            logger.error(f"500 Internal Server Error: {error}", exc_info=True)
            logger.error(f"Traceback: {traceback.format_exc()}")
        except:
            pass  # Don't fail if logger fails
        error_msg = str(error)
        
        # Provide more detailed error messages in debug mode
        if config.DEBUG:
            return jsonify({
                'error': 'Internal server error',
                'message': error_msg,
                'type': type(error).__name__
            }), 500
        else:
            return jsonify({'error': 'Internal server error. Please try again later.'}), 500
    
    # Handle unhandled exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):
        try:
            logger.error(f"Unhandled exception: {e}", exc_info=True)
        except:
            pass  # Don't fail if logger fails
        if config.DEBUG:
            return jsonify({
                'error': 'An unexpected error occurred',
                'message': str(e),
                'type': type(e).__name__
            }), 500
        return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500
    
    # Handle JWT errors
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        try:
            logger.warning(f"Expired token attempt: {jwt_payload}")
        except:
            pass  # Don't fail if logger fails
        return jsonify({'error': 'Token has expired. Please login again.'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        try:
            logger.warning(f"Invalid token attempt: {error}")
        except:
            pass  # Don't fail if logger fails
        error_msg = str(error)
        if 'expired' in error_msg.lower():
            return jsonify({'error': 'Token has expired. Please login again.'}), 401
        elif 'signature' in error_msg.lower():
            return jsonify({'error': 'Invalid token signature. Please login again.'}), 401
        elif 'decode' in error_msg.lower() or 'malformed' in error_msg.lower():
            return jsonify({'error': 'Malformed token. Please login again.'}), 401
        elif 'subject' in error_msg.lower():
            return jsonify({'error': 'Invalid token format. Please login again.'}), 401
        return jsonify({'error': f'Invalid token: {error_msg}. Please login again.'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        try:
            logger.warning(f"Missing token attempt: {error}")
        except:
            pass  # Don't fail if logger fails
        return jsonify({'error': 'Authorization required. Please login.'}), 401
    
    @app.errorhandler(422)
    def handle_validation_error(e):
        error_msg = str(e.description) if hasattr(e, 'description') else str(e)
        return jsonify({'error': f'Validation error: {error_msg}'}), 422
    
    return app

