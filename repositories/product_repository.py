"""
Product repository - Data access layer for Product entity.
"""

from typing import Optional, List
from models.product import Product
from database import db


class ProductRepository:
    """
    Repository for Product data access operations.
    Handles all database interactions for products.
    """
    
    @staticmethod
    def create(product: Product) -> int:
        """
        Insert a new product into the database.
        
        Args:
            product: Product instance to insert
        
        Returns:
            int: ID of the newly created product
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO product (name, price, stock)
                VALUES (?, ?, ?)
                """,
                (product.name, float(product.price), product.stock)
            )
            return cursor.lastrowid
    
    @staticmethod
    def find_by_id(product_id: int) -> Optional[Product]:
        """
        Find a product by its ID.
        
        Args:
            product_id: Product ID to search for
        
        Returns:
            Product instance if found, None otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM product WHERE id = ?",
                (product_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return Product(
                    id=row['id'],
                    name=row['name'],
                    price=row['price'],
                    stock=row['stock']
                )
            return None
    
    @staticmethod
    def get_all() -> List[Product]:
        """
        Retrieve all products from the database.
        
        Returns:
            List of Product instances
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product ORDER BY id")
            rows = cursor.fetchall()
            
            return [
                Product(
                    id=row['id'],
                    name=row['name'],
                    price=row['price'],
                    stock=row['stock']
                )
                for row in rows
            ]
    
    @staticmethod
    def update_stock(product_id: int, new_stock: int) -> bool:
        """
        Update the stock quantity of a product.
        
        Args:
            product_id: Product ID to update
            new_stock: New stock quantity
        
        Returns:
            bool: True if update successful, False otherwise
        
        Raises:
            ValueError: If new_stock is negative
        """
        if new_stock < 0:
            raise ValueError("Stock cannot be negative")
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE product SET stock = ? WHERE id = ?",
                (new_stock, product_id)
            )
            return cursor.rowcount > 0
    
    @staticmethod
    def decrease_stock(product_id: int, quantity: int) -> bool:
        """
        Decrease the stock of a product by a given quantity.
        
        Args:
            product_id: Product ID to update
            quantity: Quantity to decrease
        
        Returns:
            bool: True if update successful, False otherwise
        
        Raises:
            ValueError: If resulting stock would be negative
        """
        product = ProductRepository.find_by_id(product_id)
        if not product:
            return False
        
        new_stock = product.stock - quantity
        if new_stock < 0:
            raise ValueError(f"Insufficient stock. Available: {product.stock}, requested: {quantity}")
        
        return ProductRepository.update_stock(product_id, new_stock)
    
    @staticmethod
    def update(product: Product) -> bool:
        """
        Update all fields of a product.
        
        Args:
            product: Product instance with updated values
        
        Returns:
            bool: True if update successful, False otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE product 
                SET name = ?, price = ?, stock = ?
                WHERE id = ?
                """,
                (product.name, float(product.price), product.stock, product.id)
            )
            return cursor.rowcount > 0
    
    @staticmethod
    def delete(product_id: int) -> bool:
        """
        Delete a product from the database.
        
        Args:
            product_id: Product ID to delete
        
        Returns:
            bool: True if deletion successful, False otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM product WHERE id = ?",
                (product_id,)
            )
            return cursor.rowcount > 0

