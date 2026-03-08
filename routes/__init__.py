"""
Routes package - Presentation layer / Controllers.
Contains Flask route handlers separated from business logic.
"""

from .product_routes import product_bp
from .cart_routes import cart_bp
from .order_routes import order_bp
from .odata_routes import odata_bp

__all__ = ['product_bp', 'cart_bp', 'order_bp', 'odata_bp']

