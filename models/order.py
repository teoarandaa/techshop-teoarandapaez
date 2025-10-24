"""
Order model representing a customer's purchase order.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal


class Order:
    """
    Represents a purchase order made by a user.
    
    Attributes:
        id (int): Unique identifier for the order
        total (Decimal): Total amount of the order
        created_at (datetime): Order creation timestamp
        user_id (int): Foreign key to User
    """
    
    def __init__(
        self,
        total: float,
        user_id: int,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        """
        Initialize an Order instance.
        
        Args:
            total: Total amount of the order
            user_id: ID of the user who placed the order
            id: Order ID (auto-generated if None)
            created_at: Creation timestamp (defaults to now if None)
        
        Raises:
            ValueError: If total is negative or user_id is invalid
        """
        if total < 0:
            raise ValueError("Total cannot be negative")
        if user_id is None or user_id <= 0:
            raise ValueError("Invalid user_id")
        
        self.id = id
        self.total = Decimal(str(total))
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """
        Convert Order instance to dictionary.
        
        Returns:
            dict: Dictionary representation of the order
        """
        return {
            'id': self.id,
            'total': float(self.total),
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, total={self.total}, user_id={self.user_id})>"

