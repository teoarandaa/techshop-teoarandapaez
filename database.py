"""
Database management module for TechShop.
Handles SQLite database connection and initialization.
"""

import sqlite3
from typing import Optional
from contextlib import contextmanager


class Database:
    """
    Database manager for SQLite connections.
    Implements connection pooling and automatic resource management.
    """
    
    def __init__(self, db_path: str = "techshop.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Ensures proper connection cleanup and transaction management.
        
        Yields:
            sqlite3.Connection: Database connection with row factory
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        """
        Initialize database schema.
        Creates all necessary tables if they don't exist.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create User table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(20) NOT NULL UNIQUE,
                    password_hash VARCHAR(60) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create Product table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
                    stock INTEGER NOT NULL CHECK(stock >= 0)
                )
            """)
            
            # Create Order table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS 'order' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total DECIMAL(10,2) NOT NULL CHECK(total >= 0),
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(id)
                )
            """)
            
            # Create OrderItem table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_item (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL CHECK(quantity > 0),
                    FOREIGN KEY (order_id) REFERENCES 'order'(id),
                    FOREIGN KEY (product_id) REFERENCES product(id)
                )
            """)
            
            conn.commit()
    
    def reset_db(self):
        """
        Drop all tables and recreate schema.
        WARNING: This deletes all data!
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS order_item")
            cursor.execute("DROP TABLE IF EXISTS 'order'")
            cursor.execute("DROP TABLE IF EXISTS product")
            cursor.execute("DROP TABLE IF EXISTS user")
            conn.commit()
        
        self.init_db()


# Global database instance
db = Database()

