"""
Article Repository - Repository Pattern
"""
from app.database import db
from app.models.article import Article
from app.models.user import User
from app.models.category import Category
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ArticleRepository:
    """Repository for article data access"""
    
    def __init__(self):
        self.table = 'articles'
    
    def create(self, article):
        """Create a new article"""
        with db.get_cursor() as cursor:
            sql = """
                INSERT INTO articles (title, slug, content, excerpt, author_id, category_id,
                                    is_breaking, is_premium, status, published_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            published_at = article.published_at if article.status == 'published' else None
            cursor.execute(sql, (
                article.title, article.slug, article.content, article.excerpt,
                article.author_id, article.category_id, article.is_breaking,
                article.is_premium, article.status, published_at
            ))
            article.id = cursor.lastrowid
            return article
    
    def find_by_id(self, article_id, include_author=False, include_category=False):
        """Find article by ID"""
        try:
            with db.get_cursor() as cursor:
                sql = "SELECT * FROM articles WHERE id = %s"
                cursor.execute(sql, (article_id,))
                result = cursor.fetchone()
                if not result:
                    return None
                
                article = Article.from_dict(result)
            
            # Load author and category outside the cursor context to avoid nested context issues
            if include_author and article.author_id:
                try:
                    from app.repositories.user_repository import UserRepository
                    user_repo = UserRepository()
                    article.author = user_repo.find_by_id(article.author_id)
                except Exception as e:
                    logger.warning(f"Failed to load author: {e}")
                    article.author = None
            
            if include_category and article.category_id:
                try:
                    from app.repositories.category_repository import CategoryRepository
                    category_repo = CategoryRepository()
                    article.category = category_repo.find_by_id(article.category_id)
                except Exception as e:
                    logger.warning(f"Failed to load category: {e}")
                    article.category = None
            
            return article
        except Exception as e:
            logger.error(f"Error in find_by_id: {e}", exc_info=True)
            raise
    
    def find_by_slug(self, slug):
        """Find article by slug"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM articles WHERE slug = %s"
            cursor.execute(sql, (slug,))
            result = cursor.fetchone()
            return Article.from_dict(result) if result else None
    
    def update(self, article):
        """Update article"""
        with db.get_cursor() as cursor:
            sql = """
                UPDATE articles 
                SET title = %s, slug = %s, content = %s, excerpt = %s,
                    category_id = %s, is_breaking = %s, is_premium = %s,
                    status = %s, published_at = %s, updated_at = %s
                WHERE id = %s
            """
            published_at = article.published_at if article.status == 'published' else None
            cursor.execute(sql, (
                article.title, article.slug, article.content, article.excerpt,
                article.category_id, article.is_breaking, article.is_premium,
                article.status, published_at, datetime.now(), article.id
            ))
            return article
    
    def delete(self, article_id):
        """Delete article"""
        with db.get_cursor() as cursor:
            sql = "DELETE FROM articles WHERE id = %s"
            cursor.execute(sql, (article_id,))
            return cursor.rowcount > 0
    
    def find_published(self, limit=20, offset=0, category_id=None, author_id=None):
        """Find published articles with filters"""
        try:
            with db.get_cursor() as cursor:
                sql = """
                    SELECT a.*, u.username as author_username, c.name as category_name
                    FROM articles a
                    LEFT JOIN users u ON a.author_id = u.id
                    LEFT JOIN categories c ON a.category_id = c.id
                    WHERE a.status = 'published'
                """
                params = []
                
                if category_id:
                    sql += " AND a.category_id = %s"
                    params.append(category_id)
                
                if author_id:
                    sql += " AND a.author_id = %s"
                    params.append(author_id)
                
                sql += " ORDER BY a.published_at DESC LIMIT %s OFFSET %s"
                params.extend([limit, offset])
                
                cursor.execute(sql, params)
                results = cursor.fetchall()
                articles = []
                
                for row in results:
                    try:
                        article = Article.from_dict(row)
                        if row.get('author_username'):
                            article.author = User(username=row['author_username'])
                        if row.get('category_name'):
                            article.category = Category(name=row['category_name'])
                        articles.append(article)
                    except Exception as e:
                        logger.error(f"Error parsing article row: {e}")
                        continue
                
                return articles
        except Exception as e:
            logger.error(f"Error in find_published: {e}", exc_info=True)
            raise
    
    def search(self, query, limit=20, offset=0):
        """Search articles by keyword - includes title, content, excerpt, and author name"""
        with db.get_cursor() as cursor:
            search_term = f"%{query}%"
            sql = """
                SELECT a.*,
                       u.username as author_username, 
                       u.first_name as author_first_name, 
                       u.last_name as author_last_name,
                       c.name as category_name, 
                       c.slug as category_slug
                FROM articles a
                LEFT JOIN users u ON a.author_id = u.id
                LEFT JOIN categories c ON a.category_id = c.id
                WHERE a.status = 'published' 
                AND (
                    MATCH(a.title, a.content, a.excerpt) AGAINST(%s IN NATURAL LANGUAGE MODE)
                    OR a.title LIKE %s 
                    OR a.content LIKE %s
                    OR a.excerpt LIKE %s
                    OR u.username LIKE %s
                    OR u.first_name LIKE %s
                    OR u.last_name LIKE %s
                    OR CONCAT(u.first_name, ' ', u.last_name) LIKE %s
                )
                ORDER BY a.published_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (
                query, search_term, search_term, search_term,
                search_term, search_term, search_term, search_term,
                limit, offset
            ))
            results = cursor.fetchall()
            
            articles = []
            for row in results:
                try:
                    article = Article.from_dict(row)
                    # Load author if available
                    if row.get('author_username'):
                        article.author = User(
                            id=row.get('author_id'),
                            username=row.get('author_username'),
                            first_name=row.get('author_first_name'),
                            last_name=row.get('author_last_name')
                        )
                    # Load category if available
                    if row.get('category_name'):
                        article.category = Category(
                            id=row.get('category_id'),
                            name=row.get('category_name'),
                            slug=row.get('category_slug')
                        )
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Error parsing article in search: {e}")
                    continue
            
            return articles
    
    def increment_views(self, article_id):
        """Increment article views count"""
        with db.get_cursor() as cursor:
            sql = "UPDATE articles SET views_count = views_count + 1 WHERE id = %s"
            cursor.execute(sql, (article_id,))

