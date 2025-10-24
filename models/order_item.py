"""
OrderItem model representing individual items within an order.
"""

from typing import Optional


class OrderItem:
    """
    Represents a line item in an order (product + quantity).
    
    Attributes:
        id (int): Unique identifier for the order item
        order_id (int): Foreign key to Order
        product_id (int): Foreign key to Product
        quantity (int): Number of units of the product
    """
    
    def __init__(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
        id: Optional[int] = None
    ):
        """
        Initialize an OrderItem instance.
        
        Args:
            order_id: ID of the order this item belongs to
            product_id: ID of the product
            quantity: Number of units
            id: OrderItem ID (auto-generated if None)
        
        Raises:
            ValueError: If quantity is not positive or IDs are invalid
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if order_id is None or order_id <= 0:
            raise ValueError("Invalid order_id")
        if product_id is None or product_id <= 0:
            raise ValueError("Invalid product_id")
        
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
    
    def to_dict(self) -> dict:
        """
        Convert OrderItem instance to dictionary.
        
        Returns:
            dict: Dictionary representation of the order item
        """
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }
    
    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"

