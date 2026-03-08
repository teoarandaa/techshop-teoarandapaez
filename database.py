"""
Database management module for TechShop.
Handles PostgreSQL database connection and initialization.
"""

import os
import psycopg
from contextlib import contextmanager


class Database:
    """
    Database manager for PostgreSQL connections.
    """

    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL', '')

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Ensures proper connection cleanup and transaction management.
        """
        conn = psycopg.connect(self.database_url)
        conn.autocommit = False
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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "user" (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(20) NOT NULL UNIQUE,
                    password_hash VARCHAR(60) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    edat INTEGER,
                    segment VARCHAR(50),
                    ciutat VARCHAR(100),
                    provincia VARCHAR(100),
                    pais VARCHAR(100)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price NUMERIC(10,2) NOT NULL CHECK(price >= 0),
                    stock INTEGER NOT NULL CHECK(stock >= 0),
                    categoria VARCHAR(100),
                    subcategoria VARCHAR(100)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "order" (
                    id SERIAL PRIMARY KEY,
                    total NUMERIC(10,2) NOT NULL CHECK(total >= 0),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    ciutat VARCHAR(100),
                    provincia VARCHAR(100),
                    pais VARCHAR(100),
                    FOREIGN KEY (user_id) REFERENCES "user"(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_item (
                    id SERIAL PRIMARY KEY,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL CHECK(quantity > 0),
                    FOREIGN KEY (order_id) REFERENCES "order"(id),
                    FOREIGN KEY (product_id) REFERENCES product(id)
                )
            """)

    def reset_db(self):
        """
        Drop all tables and recreate schema.
        WARNING: This deletes all data!
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS order_item")
            cursor.execute('DROP TABLE IF EXISTS "order"')
            cursor.execute("DROP TABLE IF EXISTS product")
            cursor.execute('DROP TABLE IF EXISTS "user"')

        self.init_db()


# Global database instance
db = Database()

