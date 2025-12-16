"""
Category Repository - Repository Pattern
"""
from app.database import db
from app.models.category import Category
import logging

logger = logging.getLogger(__name__)


class CategoryRepository:
    """Repository for category data access"""
    
    def __init__(self):
        self.table = 'categories'
    
    def create(self, category):
        """Create a new category"""
        with db.get_cursor() as cursor:
            sql = "INSERT INTO categories (name, slug, description) VALUES (%s, %s, %s)"
            cursor.execute(sql, (category.name, category.slug, category.description))
            category.id = cursor.lastrowid
            return category
    
    def find_by_id(self, category_id):
        """Find category by ID"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM categories WHERE id = %s"
            cursor.execute(sql, (category_id,))
            result = cursor.fetchone()
            return Category.from_dict(result) if result else None
    
    def find_by_slug(self, slug):
        """Find category by slug"""
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM categories WHERE slug = %s"
            cursor.execute(sql, (slug,))
            result = cursor.fetchone()
            return Category.from_dict(result) if result else None
    
    def find_all(self):
        """Find all categories"""
        try:
            with db.get_cursor() as cursor:
                sql = "SELECT * FROM categories ORDER BY name"
                cursor.execute(sql)
                results = cursor.fetchall()
                if not results:
                    return []
                categories = []
                for row in results:
                    try:
                        category = Category.from_dict(row)
                        if category:
                            categories.append(category)
                    except Exception as e:
                        logger.error(f"Error parsing category: {e}, row: {row}")
                        continue
                return categories
        except Exception as e:
            logger.error(f"Error in find_all categories: {e}", exc_info=True)
            # Return empty list instead of raising to prevent 500 errors
            return []
    
    def update(self, category):
        """Update category"""
        with db.get_cursor() as cursor:
            sql = "UPDATE categories SET name = %s, slug = %s, description = %s WHERE id = %s"
            cursor.execute(sql, (category.name, category.slug, category.description, category.id))
            return category
    
    def delete(self, category_id):
        """Delete category"""
        with db.get_cursor() as cursor:
            sql = "DELETE FROM categories WHERE id = %s"
            cursor.execute(sql, (category_id,))
            return cursor.rowcount > 0

