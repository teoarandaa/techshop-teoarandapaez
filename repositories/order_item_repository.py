"""
OrderItem repository - Data access layer for OrderItem entity.
"""

from typing import Optional, List
from models.order_item import OrderItem
from database import db


class OrderItemRepository:
    """
    Repository for OrderItem data access operations.
    Handles all database interactions for order items.
    """
    
    @staticmethod
    def create(order_item: OrderItem) -> int:
        """
        Insert a new order item into the database.
        
        Args:
            order_item: OrderItem instance to insert
        
        Returns:
            int: ID of the newly created order item
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO order_item (order_id, product_id, quantity)
                VALUES (?, ?, ?)
                """,
                (order_item.order_id, order_item.product_id, order_item.quantity)
            )
            return cursor.lastrowid
    
    @staticmethod
    def find_by_id(item_id: int) -> Optional[OrderItem]:
        """
        Find an order item by its ID.
        
        Args:
            item_id: OrderItem ID to search for
        
        Returns:
            OrderItem instance if found, None otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM order_item WHERE id = ?",
                (item_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return OrderItem(
                    id=row['id'],
                    order_id=row['order_id'],
                    product_id=row['product_id'],
                    quantity=row['quantity']
                )
            return None
    
    @staticmethod
    def find_by_order_id(order_id: int) -> List[OrderItem]:
        """
        Find all items for a specific order.
        
        Args:
            order_id: Order ID to search for
        
        Returns:
            List of OrderItem instances
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM order_item WHERE order_id = ?",
                (order_id,)
            )
            rows = cursor.fetchall()
            
            return [
                OrderItem(
                    id=row['id'],
                    order_id=row['order_id'],
                    product_id=row['product_id'],
                    quantity=row['quantity']
                )
                for row in rows
            ]
    
    @staticmethod
    def get_all() -> List[OrderItem]:
        """
        Retrieve all order items from the database.
        
        Returns:
            List of OrderItem instances
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM order_item")
            rows = cursor.fetchall()
            
            return [
                OrderItem(
                    id=row['id'],
                    order_id=row['order_id'],
                    product_id=row['product_id'],
                    quantity=row['quantity']
                )
                for row in rows
            ]

