"""
News routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository
from app.models.article import Article
from app.services.recommendation_service import RecommendationService
from app.services.notification_service import NotificationService
from app.services.subscription_service import SubscriptionService
from app.middleware.auth import optional_auth, premium_required
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

news_bp = Blueprint('news', __name__)
article_repo = ArticleRepository()
category_repo = CategoryRepository()
user_repo = UserRepository()
recommendation_service = RecommendationService()
notification_service = NotificationService()
subscription_service = SubscriptionService()


def slugify(text):
    """Generate URL-friendly slug from text"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


@news_bp.route('', methods=['GET'])
@optional_auth
def get_news():
    """Get news feed with pagination and filters"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        category_id = request.args.get('category_id', type=int)
        author_id = request.args.get('author_id', type=int)
        search = request.args.get('search')
        
        offset = (page - 1) * limit
        
        # Get articles
        if search:
            articles = article_repo.search(search, limit=limit, offset=offset)
        else:
            articles = article_repo.find_published(
                limit=limit,
                offset=offset,
                category_id=category_id,
                author_id=author_id
            )
        
        # Check premium access for current user
        current_user_id = None
        has_premium = False
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            from flask_jwt_extended import get_jwt_identity
            current_user_id = get_jwt_identity()
            # Convert to int if it's a string (JWT stores as string)
            if current_user_id and isinstance(current_user_id, str):
                try:
                    current_user_id = int(current_user_id)
                except (ValueError, TypeError):
                    current_user_id = None
            has_premium = subscription_service.has_premium_access(current_user_id) if current_user_id else False
        except:
            pass
        
        # Check saved and liked status for authenticated users
        saved_article_ids = set()
        liked_article_ids = set()
        if current_user_id:
            try:
                from app.database import db
                with db.get_cursor() as cursor:
                    article_ids = [a.id for a in articles if a.id]
                    if article_ids:
                        placeholders = ','.join(['%s'] * len(article_ids))
                        
                        # Check saved articles
                        sql_saved = f"SELECT article_id FROM saved_articles WHERE user_id = %s AND article_id IN ({placeholders})"
                        cursor.execute(sql_saved, [current_user_id] + article_ids)
                        saved_article_ids = {row['article_id'] for row in cursor.fetchall()}
                        
                        # Check liked articles
                        sql_liked = f"SELECT article_id FROM article_likes WHERE user_id = %s AND article_id IN ({placeholders})"
                        cursor.execute(sql_liked, [current_user_id] + article_ids)
                        liked_article_ids = {row['article_id'] for row in cursor.fetchall()}
            except Exception as e:
                logger.warning(f"Failed to check saved/liked articles: {e}")
        
        # Filter out premium articles for non-premium users
        result_articles = []
        for article in articles:
            if article.is_premium and not has_premium:
                # Show limited preview for premium articles
                article_dict = article.to_dict()
                article_dict['content'] = article_dict['content'][:200] + '... [Premium content - Subscribe to read more]'
                article_dict['is_saved'] = article.id in saved_article_ids
                article_dict['is_liked'] = article.id in liked_article_ids
                result_articles.append(article_dict)
            else:
                article_dict = article.to_dict()
                article_dict['is_saved'] = article.id in saved_article_ids
                article_dict['is_liked'] = article.id in liked_article_ids
                result_articles.append(article_dict)
        
        return jsonify({
            'articles': result_articles,
            'page': page,
            'limit': limit,
            'total': len(result_articles)
        }), 200
    
    except Exception as e:
        logger.error(f"Get news error: {e}", exc_info=True)
        error_msg = str(e)
        if 'connection' in error_msg.lower() or 'database' in error_msg.lower():
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        return jsonify({'error': f'Failed to fetch news: {error_msg}'}), 500


@news_bp.route('/<int:article_id>', methods=['GET'])
@optional_auth
def get_article(article_id):
    """Get single article by ID"""
    try:
        article = article_repo.find_by_id(article_id, include_author=True, include_category=True)
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        if article.status != 'published':
            return jsonify({'error': 'Article not available'}), 404
        
        # Check premium access
        current_user_id = None
        has_premium = False
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            from flask_jwt_extended import get_jwt_identity
            current_user_id = get_jwt_identity()
            # Convert to int if it's a string (JWT stores as string)
            if current_user_id and isinstance(current_user_id, str):
                try:
                    current_user_id = int(current_user_id)
                except (ValueError, TypeError):
                    current_user_id = None
            has_premium = subscription_service.has_premium_access(current_user_id) if current_user_id else False
        except:
            pass
        
        # Check premium access
        if article.is_premium and not has_premium:
            return jsonify({'error': 'Premium subscription required'}), 403
        
        # Record view (optional - don't fail if this fails)
        try:
            if current_user_id:
                ip_address = request.remote_addr
                recommendation_service.record_view(current_user_id, article_id, ip_address)
        except Exception as e:
            logger.warning(f"Failed to record view: {e}")
        
        # Increment views (optional - don't fail if this fails)
        try:
            article_repo.increment_views(article_id)
        except Exception as e:
            logger.warning(f"Failed to increment views: {e}")
        
        # Re-fetch article to get updated view count
        article = article_repo.find_by_id(article_id, include_author=True, include_category=True)
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Check if article is saved and liked
        is_saved = False
        is_liked = False
        if current_user_id:
            try:
                from app.database import db
                with db.get_cursor() as cursor:
                    # Check saved status
                    sql_saved = "SELECT * FROM saved_articles WHERE article_id = %s AND user_id = %s"
                    cursor.execute(sql_saved, (article_id, current_user_id))
                    is_saved = cursor.fetchone() is not None
                    
                    # Check liked status
                    sql_liked = "SELECT * FROM article_likes WHERE article_id = %s AND user_id = %s"
                    cursor.execute(sql_liked, (article_id, current_user_id))
                    is_liked = cursor.fetchone() is not None
            except Exception as e:
                logger.warning(f"Failed to check if article is saved/liked: {e}")
        
        # Convert article to dict safely
        try:
            article_dict = article.to_dict()
            article_dict['is_saved'] = is_saved
            article_dict['is_liked'] = is_liked
        except Exception as e:
            logger.error(f"Error converting article to dict: {e}", exc_info=True)
            return jsonify({'error': f'Error formatting article data: {str(e)}'}), 500
        
        return jsonify({'article': article_dict}), 200
    
    except Exception as e:
        logger.error(f"Get article error: {e}", exc_info=True)
        error_msg = str(e)
        if 'connection' in error_msg.lower() or 'database' in error_msg.lower():
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        return jsonify({'error': f'Failed to fetch article: {error_msg}'}), 500


@news_bp.route('/search', methods=['GET'])
def search_news():
    """Search news articles"""
    try:
        query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        offset = (page - 1) * limit
        articles = article_repo.search(query, limit=limit, offset=offset)
        
        return jsonify({
            'articles': [article.to_dict() for article in articles],
            'query': query,
            'page': page,
            'limit': limit
        }), 200
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': 'Search failed'}), 500


@news_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = category_repo.find_all()
        if not categories:
            logger.warning("No categories found in database")
            return jsonify({'categories': []}), 200
        return jsonify({'categories': [cat.to_dict() for cat in categories]}), 200
    except Exception as e:
        logger.error(f"Get categories error: {e}", exc_info=True)
        error_msg = str(e)
        # Try to return empty categories instead of error for better UX
        try:
            return jsonify({'categories': []}), 200
        except:
            if 'connection' in error_msg.lower() or 'database' in error_msg.lower():
                return jsonify({'error': 'Database connection error. Please try again.'}), 500
            return jsonify({'error': f'Failed to fetch categories: {error_msg}'}), 500


@news_bp.route('/recommended', methods=['GET'])
@jwt_required()
def get_recommended():
    """Get recommended articles for current user"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        limit = int(request.args.get('limit', 10))
        
        articles = recommendation_service.get_recommended_articles(current_user_id, limit=limit)
        
        # Check saved and liked status
        saved_article_ids = set()
        liked_article_ids = set()
        if current_user_id:
            try:
                from app.database import db
                with db.get_cursor() as cursor:
                    article_ids = [a.id for a in articles if a.id]
                    if article_ids:
                        placeholders = ','.join(['%s'] * len(article_ids))
                        
                        # Check saved articles
                        sql_saved = f"SELECT article_id FROM saved_articles WHERE user_id = %s AND article_id IN ({placeholders})"
                        cursor.execute(sql_saved, [current_user_id] + article_ids)
                        saved_article_ids = {row['article_id'] for row in cursor.fetchall()}
                        
                        # Check liked articles
                        sql_liked = f"SELECT article_id FROM article_likes WHERE user_id = %s AND article_id IN ({placeholders})"
                        cursor.execute(sql_liked, [current_user_id] + article_ids)
                        liked_article_ids = {row['article_id'] for row in cursor.fetchall()}
            except Exception as e:
                logger.warning(f"Failed to check saved/liked articles: {e}")
        
        # Convert articles to dict with error handling
        articles_dict = []
        for article in articles:
            try:
                article_dict = article.to_dict()
                article_dict['is_saved'] = article.id in saved_article_ids
                article_dict['is_liked'] = article.id in liked_article_ids
                articles_dict.append(article_dict)
            except Exception as e:
                logger.error(f"Error converting article to dict: {e}", exc_info=True)
                # Skip this article if conversion fails
                continue
        
        return jsonify({
            'articles': articles_dict
        }), 200
    
    except Exception as e:
        logger.error(f"Get recommended error: {e}", exc_info=True)
        error_msg = str(e)
        if 'connection' in error_msg.lower() or 'database' in error_msg.lower():
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        return jsonify({'error': f'Failed to get recommendations: {error_msg}'}), 500


@news_bp.route('', methods=['POST'])
@jwt_required()
def create_article():
    """Create new article (editor/admin only)"""
    from app.middleware.auth import editor_required
    
    @editor_required
    def _create():
        try:
            data = request.get_json()
            current_user_id = get_jwt_identity()
            
            # Validate required fields
            if not data.get('title') or not data.get('content'):
                return jsonify({'error': 'Title and content are required'}), 400
            
            # Generate slug
            slug = slugify(data['title'])
            
            # Check if slug exists
            existing = article_repo.find_by_slug(slug)
            if existing:
                slug = f"{slug}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            article = Article(
                title=data['title'],
                slug=slug,
                content=data['content'],
                excerpt=data.get('excerpt', data['content'][:200]),
                author_id=current_user_id,
                category_id=data.get('category_id'),
                is_breaking=data.get('is_breaking', False),
                is_premium=data.get('is_premium', False),
                status=data.get('status', 'draft')
            )
            
            if article.status == 'published':
                article.published_at = datetime.now()
                if article.is_breaking:
                    notification_service.send_breaking_news(None, article.title)
            
            article = article_repo.create(article)
            
            return jsonify({'article': article.to_dict()}), 201
        
        except Exception as e:
            logger.error(f"Create article error: {e}")
            return jsonify({'error': 'Failed to create article'}), 500
    
    return _create()


@news_bp.route('/<int:article_id>/like', methods=['POST'])
@jwt_required()
def like_article(article_id):
    """Like/unlike an article"""
    try:
        from app.database import db
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        if not article_id or article_id <= 0:
            return jsonify({'error': 'Invalid article ID'}), 400
        
        # Verify article exists
        article = article_repo.find_by_id(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        with db.get_cursor() as cursor:
            # Check if already liked
            sql_check = "SELECT * FROM article_likes WHERE article_id = %s AND user_id = %s"
            cursor.execute(sql_check, (article_id, current_user_id))
            existing = cursor.fetchone()
            
            if existing:
                # Unlike
                sql_delete = "DELETE FROM article_likes WHERE article_id = %s AND user_id = %s"
                cursor.execute(sql_delete, (article_id, current_user_id))
                sql_update = "UPDATE articles SET likes_count = GREATEST(0, likes_count - 1) WHERE id = %s"
                cursor.execute(sql_update, (article_id,))
                return jsonify({'message': 'Article unliked', 'liked': False}), 200
            else:
                # Like
                sql_insert = "INSERT INTO article_likes (article_id, user_id) VALUES (%s, %s)"
                cursor.execute(sql_insert, (article_id, current_user_id))
                sql_update = "UPDATE articles SET likes_count = likes_count + 1 WHERE id = %s"
                cursor.execute(sql_update, (article_id,))
                
                # Record like for recommendation system
                try:
                    recommendation_service.record_like(current_user_id, article_id)
                except Exception as e:
                    logger.warning(f"Failed to record like for recommendations: {e}")
                
                return jsonify({'message': 'Article liked', 'liked': True}), 200
    
    except Exception as e:
        logger.error(f"Like article error: {e}", exc_info=True)
        error_msg = str(e)
        if 'duplicate' in error_msg.lower() or 'UNIQUE' in error_msg.upper() or 'Duplicate entry' in error_msg:
            # Already liked, so unlike it
            try:
                from app.database import db
                current_user_id = get_jwt_identity()
                with db.get_cursor() as cursor:
                    sql_delete = "DELETE FROM article_likes WHERE article_id = %s AND user_id = %s"
                    cursor.execute(sql_delete, (article_id, current_user_id))
                    sql_update = "UPDATE articles SET likes_count = GREATEST(0, likes_count - 1) WHERE id = %s"
                    cursor.execute(sql_update, (article_id,))
                return jsonify({'message': 'Article unliked', 'liked': False}), 200
            except:
                return jsonify({'error': 'Article already liked'}), 400
        return jsonify({'error': f'Failed to like article: {error_msg}'}), 500


@news_bp.route('/<int:article_id>/save', methods=['POST'])
@jwt_required()
def save_article(article_id):
    """Save/unsave article for reading later (toggle)"""
    try:
        from app.database import db
        current_user_id = get_jwt_identity()
        # Convert to int if it's a string (JWT stores as string)
        if current_user_id and isinstance(current_user_id, str):
            try:
                current_user_id = int(current_user_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid user ID'}), 400
        
        with db.get_cursor() as cursor:
            # Check if already saved
            sql_check = "SELECT * FROM saved_articles WHERE article_id = %s AND user_id = %s"
            cursor.execute(sql_check, (article_id, current_user_id))
            existing = cursor.fetchone()
            
            if existing:
                # Unsave the article
                sql_delete = "DELETE FROM saved_articles WHERE article_id = %s AND user_id = %s"
                cursor.execute(sql_delete, (article_id, current_user_id))
                return jsonify({
                    'message': 'Article removed from saved',
                    'saved': False
                }), 200
            else:
                # Save the article
                sql_insert = "INSERT INTO saved_articles (article_id, user_id) VALUES (%s, %s)"
                cursor.execute(sql_insert, (article_id, current_user_id))
                return jsonify({
                    'message': 'Article saved',
                    'saved': True
                }), 201
    
    except Exception as e:
        logger.error(f"Save article error: {e}", exc_info=True)
        error_msg = str(e)
        if 'connection' in error_msg.lower() or 'database' in error_msg.lower():
            return jsonify({'error': 'Database connection error. Please try again.'}), 500
        return jsonify({'error': f'Failed to save article: {error_msg}'}), 500

