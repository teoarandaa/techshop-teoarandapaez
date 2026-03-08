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
        created_at: Optional[datetime] = None,
        edat: Optional[int] = None,
        segment: str = '',
        ciutat: str = '',
        provincia: str = '',
        pais: str = ''
    ):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now()
        self.edat = edat
        self.segment = segment
        self.ciutat = ciutat
        self.provincia = provincia
        self.pais = pais

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'edat': self.edat,
            'segment': self.segment,
            'ciutat': self.ciutat,
            'provincia': self.provincia,
            'pais': self.pais,
        }
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

