"""
Order repository - Data access layer for Order entity.
"""

from typing import Optional, List
from models.order import Order
from database import db


class OrderRepository:
    """
    Repository for Order data access operations.
    Handles all database interactions for orders.
    """
    
    @staticmethod
    def create(order: Order) -> int:
        """
        Insert a new order into the database.
        
        Args:
            order: Order instance to insert
        
        Returns:
            int: ID of the newly created order
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO "order" (total, created_at, user_id, ciutat, provincia, pais)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (float(order.total), order.created_at, order.user_id,
                 order.ciutat, order.provincia, order.pais)
            )
            return cursor.fetchone()[0]
    
    @staticmethod
    def find_by_id(order_id: int) -> Optional[Order]:
        """
        Find an order by its ID.
        
        Args:
            order_id: Order ID to search for
        
        Returns:
            Order instance if found, None otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM "order" WHERE id = %s',
                (order_id,)
            )
            row = cursor.fetchone()

            if row:
                return Order(
                    id=row[0], total=row[1], created_at=row[2], user_id=row[3],
                    ciutat=row[4] or '', provincia=row[5] or '', pais=row[6] or ''
                )
            return None
    
    @staticmethod
    def find_by_user_id(user_id: int) -> List[Order]:
        """
        Find all orders for a specific user.
        
        Args:
            user_id: User ID to search for
        
        Returns:
            List of Order instances
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM "order" WHERE user_id = %s ORDER BY created_at DESC',
                (user_id,)
            )
            rows = cursor.fetchall()

            return [
                Order(
                    id=row[0], total=row[1], created_at=row[2], user_id=row[3],
                    ciutat=row[4] or '', provincia=row[5] or '', pais=row[6] or ''
                )
                for row in rows
            ]

    @staticmethod
    def get_all() -> List[Order]:
        """
        Retrieve all orders from the database.
        
        Returns:
            List of Order instances
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "order" ORDER BY created_at DESC')
            rows = cursor.fetchall()

            return [
                Order(
                    id=row[0], total=row[1], created_at=row[2], user_id=row[3],
                    ciutat=row[4] or '', provincia=row[5] or '', pais=row[6] or ''
                )
                for row in rows
            ]

