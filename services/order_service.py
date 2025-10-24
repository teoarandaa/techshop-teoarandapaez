"""
Order service - Business logic for order processing.
Handles order creation with stock management and data integrity.
"""

from typing import Dict, Optional
from models.order import Order
from models.order_item import OrderItem
from repositories.order_repository import OrderRepository
from repositories.order_item_repository import OrderItemRepository
from repositories.product_repository import ProductRepository
from services.cart_service import CartService
from decimal import Decimal


class OrderService:
    """
    Service for managing order operations.
    Handles order creation, stock updates, and order history.
    """
    
    @staticmethod
    def create_order(cart: Dict[int, int], user_id: int) -> Dict[str, any]:
        """
        Create an order from the shopping cart.
        
        Business logic:
        1. Validate cart is not empty
        2. Validate all items have sufficient stock
        3. Calculate total amount
        4. Create order record
        5. Create order items
        6. Update product stock
        7. Clear cart
        
        Args:
            cart: Shopping cart dictionary {product_id: quantity}
            user_id: ID of the user placing the order
        
        Returns:
            dict: Result with 'success' (bool), 'message' (str), and 'order_id' (int)
        
        Raises:
            Exception: If order creation fails
        """
        # Validate cart is not empty
        if not cart or len(cart) == 0:
            return {
                'success': False,
                'message': 'El carretó està buit.'
            }
        
        # Validate stock for all items
        stock_validation = CartService.validate_cart_stock(cart)
        if not stock_validation['valid']:
            return {
                'success': False,
                'message': 'Errors de validació: ' + '; '.join(stock_validation['errors'])
            }
        
        # Calculate total
        total = Decimal('0.00')
        order_items_data = []
        
        for product_id, quantity in cart.items():
            product = ProductRepository.find_by_id(product_id)
            if not product:
                return {
                    'success': False,
                    'message': f'Producte {product_id} no trobat.'
                }
            
            subtotal = product.price * quantity
            total += subtotal
            
            order_items_data.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product
            })
        
        try:
            # Create order
            order = Order(
                total=float(total),
                user_id=user_id
            )
            order_id = OrderRepository.create(order)
            
            # Create order items and update stock
            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity']
                )
                OrderItemRepository.create(order_item)
                
                # Decrease stock
                ProductRepository.decrease_stock(
                    item_data['product_id'],
                    item_data['quantity']
                )
            
            # Clear cart after successful order
            CartService.clear_cart(cart)
            
            return {
                'success': True,
                'message': f'Comanda #{order_id} creada correctament.',
                'order_id': order_id
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en crear la comanda: {str(e)}'
            }
    
    @staticmethod
    def get_order_details(order_id: int) -> Optional[Dict[str, any]]:
        """
        Get detailed information about an order.
        
        Args:
            order_id: ID of the order
        
        Returns:
            dict: Order details including items and products, or None if not found
        """
        order = OrderRepository.find_by_id(order_id)
        if not order:
            return None
        
        order_items = OrderItemRepository.find_by_order_id(order_id)
        
        items_details = []
        for item in order_items:
            product = ProductRepository.find_by_id(item.product_id)
            if product:
                items_details.append({
                    'product': product,
                    'quantity': item.quantity,
                    'subtotal': product.price * item.quantity
                })
        
        return {
            'order': order,
            'order_items': items_details  # Renamed from 'items' to avoid Jinja2 conflict
        }
    
    @staticmethod
    def get_user_orders(user_id: int) -> list:
        """
        Get all orders for a specific user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            list: List of orders with their details
        """
        orders = OrderRepository.find_by_user_id(user_id)
        
        orders_with_details = []
        for order in orders:
            order_details = OrderService.get_order_details(order.id)
            if order_details:
                orders_with_details.append(order_details)
        
        return orders_with_details

