"""
User model representing a customer in the TechShop system.
"""

from datetime import datetime
from typing import Optional


class User:
    """
    Represents a user/customer in the system.
    
    Attributes:
        id (int): Unique identifier for the user
        username (str): Username (4-20 characters)
        password_hash (str): Hashed password (never store plain text)
        email (str): User's email address
        created_at (datetime): Account creation timestamp
    """
    
    def __init__(
        self,
        username: str,
        password_hash: str,
        email: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        """
        Initialize a User instance.
        
        Args:
            username: Username (4-20 characters)
            password_hash: Hashed password
            email: User's email address
            id: User ID (auto-generated if None)
            created_at: Creation timestamp (defaults to now if None)
        """
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """
        Convert User instance to dictionary.
        
        Returns:
            dict: Dictionary representation of the user (without password_hash)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

