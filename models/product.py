"""
Product model representing an electronic product in TechShop's catalog.
"""

from typing import Optional
from decimal import Decimal


class Product:
    """
    Represents a product available for purchase.
    
    Attributes:
        id (int): Unique identifier for the product
        name (str): Product name (max 100 characters)
        price (Decimal): Product price with 2 decimal places
        stock (int): Available units in inventory
    """
    
    def __init__(
        self,
        name: str,
        price: float,
        stock: int,
        categoria: str = '',
        subcategoria: str = '',
        id: Optional[int] = None
    ):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        self.id = id
        self.name = name
        self.price = Decimal(str(price))
        self.stock = stock
        self.categoria = categoria
        self.subcategoria = subcategoria

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'stock': self.stock,
            'categoria': self.categoria,
            'subcategoria': self.subcategoria,
        }
    
    def is_available(self, quantity: int) -> bool:
        """
        Check if the requested quantity is available in stock.
        
        Args:
            quantity: Number of units requested
        
        Returns:
            bool: True if available, False otherwise
        """
        return self.stock >= quantity
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', categoria='{self.categoria}', price={self.price}, stock={self.stock})>"

