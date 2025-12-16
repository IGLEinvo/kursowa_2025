#!/usr/bin/env python3
"""
Test database connection script
"""
import sys
from config import config
import pymysql

def test_connection():
    """Test database connection with current credentials"""
    print("Testing database connection...")
    print(f"Host: {config.DB_HOST}")
    print(f"Port: {config.DB_PORT}")
    print(f"User: {config.DB_USER}")
    print(f"Database: {config.DB_NAME}")
    print(f"Password: {'*' * len(config.DB_PASSWORD) if config.DB_PASSWORD else '(empty)'}")
    print()
    
    try:
        connection = pymysql.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✓ Database connection successful!")
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM categories")
            result = cursor.fetchone()
            print(f"✓ Categories in database: {result['count']}")
            
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            print(f"✓ Users in database: {result['count']}")
        
        connection.close()
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPossible solutions:")
        print("1. Check if MySQL server is running")
        print("2. Verify the password in backend/.env file")
        print("3. Try resetting MySQL root password:")
        print("   sudo /usr/local/mysql/bin/mysqld_safe --skip-grant-tables &")
        print("   /usr/local/mysql/bin/mysql -u root")
        print("   FLUSH PRIVILEGES;")
        print("   ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

