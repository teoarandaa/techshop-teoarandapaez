"""
Cart service - Business logic for shopping cart operations.
Implements cart management with validation rules.
"""

from typing import Dict, List, Optional
from repositories.product_repository import ProductRepository
from decimal import Decimal


class CartService:
    """
    Service for managing shopping cart operations.
    Enforces business rules like maximum quantity per product (5 units).
    """
    
    # Business rule: Maximum units per product in cart
    MAX_QUANTITY_PER_PRODUCT = 5
    
    @staticmethod
    def add_to_cart(cart: Dict[int, int], product_id: int, quantity: int) -> Dict[str, any]:
        """
        Add a product to the shopping cart with validation.
        
        Business rules:
        - Quantity must be positive
        - Total quantity per product cannot exceed MAX_QUANTITY_PER_PRODUCT
        - Product must exist in database
        - Must have sufficient stock
        
        Args:
            cart: Current cart dictionary {product_id: quantity}
            product_id: ID of the product to add
            quantity: Quantity to add
        
        Returns:
            dict: Result with 'success' (bool) and 'message' (str)
        
        Raises:
            ValueError: If validation fails
        """
        # Validate quantity is positive
        if quantity <= 0:
            return {
                'success': False,
                'message': 'La quantitat ha de ser un nombre positiu.'
            }
        
        # Validate product exists
        product = ProductRepository.find_by_id(product_id)
        if not product:
            return {
                'success': False,
                'message': 'Producte no trobat.'
            }
        
        # Calculate current quantity in cart
        current_quantity = cart.get(product_id, 0)
        new_total_quantity = current_quantity + quantity
        
        # Validate maximum quantity rule
        if new_total_quantity > CartService.MAX_QUANTITY_PER_PRODUCT:
            return {
                'success': False,
                'message': f'No pots afegir més de {CartService.MAX_QUANTITY_PER_PRODUCT} unitats del mateix producte. Ja tens {current_quantity} al carretó.'
            }
        
        # Validate stock availability
        if not CartService.validate_stock(product_id, quantity):
            return {
                'success': False,
                'message': f'Stock insuficient. Disponible: {product.stock} unitats.'
            }
        
        # Add to cart
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        
        return {
            'success': True,
            'message': f'{product.name} afegit al carretó.'
        }
    
    @staticmethod
    def remove_from_cart(cart: Dict[int, int], product_id: int) -> Dict[str, any]:
        """
        Remove a product from the shopping cart.
        
        Args:
            cart: Current cart dictionary {product_id: quantity}
            product_id: ID of the product to remove
        
        Returns:
            dict: Result with 'success' (bool) and 'message' (str)
        """
        if product_id not in cart:
            return {
                'success': False,
                'message': 'Producte no trobat al carretó.'
            }
        
        del cart[product_id]
        
        return {
            'success': True,
            'message': 'Producte eliminat del carretó.'
        }
    
    @staticmethod
    def update_quantity(cart: Dict[int, int], product_id: int, quantity: int) -> Dict[str, any]:
        """
        Update the quantity of a product in the cart.
        
        Args:
            cart: Current cart dictionary {product_id: quantity}
            product_id: ID of the product to update
            quantity: New quantity
        
        Returns:
            dict: Result with 'success' (bool) and 'message' (str)
        """
        if quantity <= 0:
            return CartService.remove_from_cart(cart, product_id)
        
        if product_id not in cart:
            return {
                'success': False,
                'message': 'Producte no trobat al carretó.'
            }
        
        # Validate maximum quantity rule
        if quantity > CartService.MAX_QUANTITY_PER_PRODUCT:
            return {
                'success': False,
                'message': f'No pots tenir més de {CartService.MAX_QUANTITY_PER_PRODUCT} unitats del mateix producte.'
            }
        
        # Validate stock
        product = ProductRepository.find_by_id(product_id)
        if not product or product.stock < quantity:
            return {
                'success': False,
                'message': f'Stock insuficient. Disponible: {product.stock if product else 0} unitats.'
            }
        
        cart[product_id] = quantity
        
        return {
            'success': True,
            'message': 'Quantitat actualitzada.'
        }
    
    @staticmethod
    def validate_stock(product_id: int, quantity: int) -> bool:
        """
        Validate that sufficient stock is available for a product.
        
        Args:
            product_id: ID of the product
            quantity: Quantity requested
        
        Returns:
            bool: True if sufficient stock available, False otherwise
        """
        product = ProductRepository.find_by_id(product_id)
        if not product:
            return False
        
        return product.is_available(quantity)
    
    @staticmethod
    def get_cart_details(cart: Dict[int, int]) -> Dict[str, any]:
        """
        Get detailed information about cart contents.
        
        Args:
            cart: Current cart dictionary {product_id: quantity}
        
        Returns:
            dict: Cart details including items, subtotals, and total
        """
        items = []
        total = Decimal('0.00')
        
        for product_id, quantity in cart.items():
            product = ProductRepository.find_by_id(product_id)
            if product:
                subtotal = product.price * quantity
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total += subtotal
        
        return {
            'cart_items': items,  # Renamed from 'items' to avoid Jinja2 conflict
            'total': total,
            'item_count': sum(cart.values())
        }
    
    @staticmethod
    def clear_cart(cart: Dict[int, int]) -> None:
        """
        Clear all items from the cart.
        
        Args:
            cart: Current cart dictionary {product_id: quantity}
        """
        cart.clear()
    
    @staticmethod
    def validate_cart_stock(cart: Dict[int, int]) -> Dict[str, any]:
        """
        Validate that all items in cart have sufficient stock.
        
        Args:
            cart: Current cart dictionary {product_id: quantity}
        
        Returns:
            dict: Result with 'valid' (bool) and 'errors' (list)
        """
        errors = []
        
        for product_id, quantity in cart.items():
            product = ProductRepository.find_by_id(product_id)
            if not product:
                errors.append(f'Producte {product_id} no trobat.')
            elif not product.is_available(quantity):
                errors.append(
                    f'{product.name}: stock insuficient. '
                    f'Disponible: {product.stock}, requerit: {quantity}.'
                )
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

