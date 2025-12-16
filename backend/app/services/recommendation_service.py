"""
Recommendation Service - for content personalization
"""
from app.database import db
from app.repositories.user_repository import UserRepository
from app.repositories.article_repository import ArticleRepository
from app.models.article import Article
import logging

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for article recommendations based on user preferences"""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.article_repo = ArticleRepository()
    
    def update_user_preferences(self, user_id, category_id, increment=1.0):
        """Update user preference score for a category"""
        with db.get_cursor() as cursor:
            # Check if preference exists
            sql_check = """
                SELECT * FROM user_preferences
                WHERE user_id = %s AND category_id = %s
            """
            cursor.execute(sql_check, (user_id, category_id))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing preference
                new_score = min(5.0, existing['preference_score'] + increment)
                sql_update = """
                    UPDATE user_preferences
                    SET preference_score = %s
                    WHERE user_id = %s AND category_id = %s
                """
                cursor.execute(sql_update, (new_score, user_id, category_id))
            else:
                # Create new preference
                sql_insert = """
                    INSERT INTO user_preferences (user_id, category_id, preference_score)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql_insert, (user_id, category_id, increment))
    
    def get_recommended_articles(self, user_id, limit=10):
        """Get recommended articles based on user preferences, views, and likes"""
        try:
            # Convert user_id to int if string
            if isinstance(user_id, str):
                try:
                    user_id = int(user_id)
                except (ValueError, TypeError):
                    logger.error(f"Invalid user_id format: {user_id}")
                    return []
            
            # Step 1: Get user's category preferences
            with db.get_cursor() as cursor:
                # PRIORITY 1: Get explicit favorite categories (from user_preferences)
                # These have the highest priority since user explicitly selected them
                sql_favorite = """
                    SELECT category_id, preference_score
                    FROM user_preferences
                    WHERE user_id = %s
                    ORDER BY preference_score DESC
                """
                cursor.execute(sql_favorite, (user_id,))
                favorite_prefs = cursor.fetchall()
                favorite_categories = [(p['category_id'], p.get('preference_score', 1.0)) for p in favorite_prefs if p.get('category_id')]
                favorite_cat_ids = [cat_id for cat_id, _ in favorite_categories]
                
                logger.info(f"User {user_id} favorite categories: {favorite_cat_ids}")
                
                # PRIORITY 2: Get categories from liked articles (medium priority)
                sql_liked = """
                    SELECT DISTINCT a.category_id
                    FROM articles a
                    INNER JOIN article_likes al ON a.id = al.article_id
                    WHERE al.user_id = %s AND a.category_id IS NOT NULL
                """
                cursor.execute(sql_liked, (user_id,))
                liked_categories = [row['category_id'] for row in cursor.fetchall() if row.get('category_id')]
                
                # PRIORITY 3: Get categories from viewed articles (lowest priority)
                sql_viewed = """
                    SELECT DISTINCT a.category_id
                    FROM articles a
                    INNER JOIN article_views av ON a.id = av.article_id
                    WHERE av.user_id = %s AND a.category_id IS NOT NULL
                """
                cursor.execute(sql_viewed, (user_id,))
                viewed_categories = [row['category_id'] for row in cursor.fetchall() if row.get('category_id')]
                
                # Combine categories with priority: favorite > liked > viewed
                # Remove duplicates, keeping favorite categories first
                all_preferred = favorite_cat_ids.copy()
                
                # Add liked categories that aren't in favorites
                for cat_id in liked_categories:
                    if cat_id not in all_preferred:
                        all_preferred.append(cat_id)
                
                # Add viewed categories that aren't already included
                for cat_id in viewed_categories:
                    if cat_id not in all_preferred:
                        all_preferred.append(cat_id)
                
                logger.info(f"User {user_id} all preferred categories: {all_preferred}")
                
                # Get excluded article IDs (only liked and saved, not viewed - so we can show viewed articles from favorites)
                sql_exclude = """
                    SELECT DISTINCT article_id 
                    FROM (
                        SELECT article_id FROM article_likes WHERE user_id = %s
                        UNION
                        SELECT article_id FROM saved_articles WHERE user_id = %s
                    ) as excluded
                """
                cursor.execute(sql_exclude, (user_id, user_id))
                excluded_ids = [row['article_id'] for row in cursor.fetchall()]
                
                logger.info(f"User {user_id} excluded article IDs (liked/saved): {len(excluded_ids)}")
            
            # Step 2: Get articles from favorite categories first (highest priority)
            # ALWAYS prioritize favorite categories - show them even if viewed
            articles = []
            if favorite_cat_ids:
                logger.info(f"Getting articles from favorite categories: {favorite_cat_ids}")
                # Get articles from favorite categories, excluding only liked/saved
                # This allows viewed articles from favorites to appear (they should!)
                articles = self._get_articles_from_categories(favorite_cat_ids, excluded_ids, limit, prioritize=True)
                logger.info(f"Found {len(articles)} articles from favorite categories (limit was {limit})")
            
            # Step 3: If we don't have enough from favorites, get MORE from favorites (even if viewed)
            # This ensures we fill up recommendations with favorite category content
            if len(articles) < limit and favorite_cat_ids:
                logger.info(f"Only got {len(articles)} articles from favorites, getting more from favorite categories")
                current_article_ids = [a.id for a in articles if a.id]
                # Only exclude articles we already have, not viewed ones
                more_articles = self._get_articles_from_categories(favorite_cat_ids, current_article_ids, limit - len(articles), prioritize=True)
                articles.extend(more_articles)
                logger.info(f"Added {len(more_articles)} more articles from favorites, total: {len(articles)}")
            
            # Step 4: If we still need more articles, get from other preferred categories
            if len(articles) < limit:
                other_cats = [cat_id for cat_id in all_preferred if cat_id not in favorite_cat_ids]
                if other_cats:
                    logger.info(f"Getting articles from other preferred categories: {other_cats}")
                    excluded_all = excluded_ids + [a.id for a in articles if a.id]
                    more_articles = self._get_articles_from_categories(other_cats, excluded_all, limit - len(articles))
                    articles.extend(more_articles)
            
            # Step 5: Fill remaining slots with trending articles
            if len(articles) < limit:
                logger.info(f"Filling remaining {limit - len(articles)} slots with trending articles")
                excluded_all = excluded_ids + [a.id for a in articles if a.id]
                trending = self._get_trending_articles(excluded_all, limit - len(articles))
                articles.extend(trending)
            
            logger.info(f"Returning {len(articles[:limit])} recommended articles for user {user_id}")
            return articles[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}", exc_info=True)
            # Fallback to trending articles
            try:
                return self._get_trending_articles([], limit)
            except Exception as e2:
                logger.error(f"Error getting trending articles: {e2}", exc_info=True)
                # Last resort - return published articles
                return self.article_repo.find_published(limit=limit)
    
    def _get_articles_from_categories(self, category_ids, excluded_ids, limit, prioritize=False):
        """Get articles from preferred categories"""
        articles = []
        
        if not category_ids:
            logger.warning("No category IDs provided to _get_articles_from_categories")
            return articles
        
        try:
            with db.get_cursor() as cursor:
                # Build category placeholders
                cat_placeholders = ','.join(['%s'] * len(category_ids))
                
                # Build exclude clause
                if excluded_ids:
                    exclude_placeholders = ','.join(['%s'] * len(excluded_ids))
                    exclude_clause = f"AND a.id NOT IN ({exclude_placeholders})"
                    params = category_ids + excluded_ids + [limit]
                else:
                    exclude_clause = ""
                    params = category_ids + [limit]
                
                # Query with author and category info
                # If prioritizing (favorite categories), prioritize by recency first, then engagement
                if prioritize:
                    order_by = "a.published_at DESC, (a.views_count * 0.3 + a.likes_count * 0.7) DESC"
                else:
                    order_by = "(a.views_count * 0.3 + a.likes_count * 0.7) DESC, a.published_at DESC"
                
                sql = f"""
                    SELECT a.*, 
                           u.username as author_username, u.first_name as author_first_name, u.last_name as author_last_name,
                           c.name as category_name, c.slug as category_slug
                    FROM articles a
                    LEFT JOIN users u ON a.author_id = u.id
                    LEFT JOIN categories c ON a.category_id = c.id
                    WHERE a.status = 'published'
                    AND a.category_id IN ({cat_placeholders})
                    {exclude_clause}
                    ORDER BY {order_by}
                    LIMIT %s
                """
                
                logger.debug(f"Executing query for categories {category_ids} with exclude {len(excluded_ids) if excluded_ids else 0} articles, limit {limit}")
                cursor.execute(sql, params)
                results = cursor.fetchall()
                
                logger.info(f"Query returned {len(results)} articles from categories {category_ids}")
                
                for row in results:
                    try:
                        article = Article.from_dict(dict(row))
                        # Load author if available
                        if row.get('author_username'):
                            from app.models.user import User
                            article.author = User(
                                id=row.get('author_id'),
                                username=row.get('author_username'),
                                first_name=row.get('author_first_name'),
                                last_name=row.get('author_last_name')
                            )
                        # Load category if available
                        if row.get('category_name'):
                            from app.models.category import Category
                            article.category = Category(
                                id=row.get('category_id'),
                                name=row.get('category_name'),
                                slug=row.get('category_slug')
                            )
                        articles.append(article)
                    except Exception as e:
                        logger.error(f"Error parsing article: {e}", exc_info=True)
                        continue
        except Exception as e:
            logger.error(f"Error getting articles from categories: {e}", exc_info=True)
        
        return articles
    
    def _get_trending_articles(self, excluded_ids, limit):
        """Get trending articles based on views and likes"""
        articles = []
        
        try:
            with db.get_cursor() as cursor:
                if excluded_ids:
                    exclude_placeholders = ','.join(['%s'] * len(excluded_ids))
                    exclude_clause = f"AND a.id NOT IN ({exclude_placeholders})"
                    params = excluded_ids + [limit]
                else:
                    exclude_clause = ""
                    params = [limit]
                
                sql = f"""
                    SELECT a.*,
                           u.username as author_username, u.first_name as author_first_name, u.last_name as author_last_name,
                           c.name as category_name, c.slug as category_slug
                    FROM articles a
                    LEFT JOIN users u ON a.author_id = u.id
                    LEFT JOIN categories c ON a.category_id = c.id
                    WHERE a.status = 'published'
                    {exclude_clause}
                    ORDER BY 
                        (a.views_count * 0.4 + a.likes_count * 0.6) DESC,
                        a.published_at DESC
                    LIMIT %s
                """
                
                cursor.execute(sql, params)
                results = cursor.fetchall()
                
                for row in results:
                    try:
                        article = Article.from_dict(dict(row))
                        # Load author if available
                        if row.get('author_username'):
                            from app.models.user import User
                            article.author = User(
                                id=row.get('author_id'),
                                username=row.get('author_username'),
                                first_name=row.get('author_first_name'),
                                last_name=row.get('author_last_name')
                            )
                        # Load category if available
                        if row.get('category_name'):
                            from app.models.category import Category
                            article.category = Category(
                                id=row.get('category_id'),
                                name=row.get('category_name'),
                                slug=row.get('category_slug')
                            )
                        articles.append(article)
                    except Exception as e:
                        logger.error(f"Error parsing trending article: {e}", exc_info=True)
                        continue
        except Exception as e:
            logger.error(f"Error getting trending articles: {e}", exc_info=True)
        
        return articles
    
    def record_view(self, user_id, article_id, ip_address=None):
        """Record article view for personalization"""
        with db.get_cursor() as cursor:
            # Check if already viewed
            sql_check = """
                SELECT * FROM article_views
                WHERE article_id = %s AND user_id = %s
            """
            cursor.execute(sql_check, (article_id, user_id))
            if cursor.fetchone():
                return  # Already viewed
            
            # Record view
            sql_insert = """
                INSERT INTO article_views (article_id, user_id, ip_address)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql_insert, (article_id, user_id, ip_address))
            
            # Update preference based on article category
            sql_article = "SELECT category_id FROM articles WHERE id = %s"
            cursor.execute(sql_article, (article_id,))
            article = cursor.fetchone()
            
            if article and article.get('category_id'):
                self.update_user_preferences(user_id, article['category_id'], increment=0.1)
    
    def record_like(self, user_id, article_id):
        """Record article like for personalization (higher weight than view)"""
        with db.get_cursor() as cursor:
            # Get article category
            sql_article = "SELECT category_id FROM articles WHERE id = %s"
            cursor.execute(sql_article, (article_id,))
            article = cursor.fetchone()
            
            if article and article.get('category_id'):
                # Like has higher weight than view (2.0 vs 0.1)
                self.update_user_preferences(user_id, article['category_id'], increment=2.0)
