"""
Order routes - Handles checkout and order processing.
Presentation layer for order management.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from services.order_service import OrderService
from services.cart_service import CartService
from services.user_service import UserService
from routes.cart_routes import get_cart

order_bp = Blueprint('orders', __name__, url_prefix='/orders')


@order_bp.route('/checkout')
def checkout():
    """
    Display checkout page with cart summary and user form.
    
    Returns:
        Rendered checkout template
    """
    try:
        cart = get_cart()
        
        if not cart or len(cart) == 0:
            return redirect(url_for('products.show_products'))
        
        cart_details = CartService.get_cart_details(cart)
        
        # Validate stock before showing checkout
        stock_validation = CartService.validate_cart_stock(cart)
        if not stock_validation['valid']:
            return render_template(
                'error.html',
                error='Alguns productes no tenen stock suficient: ' + 
                      '; '.join(stock_validation['errors'])
            ), 400
        
        return render_template('checkout.html', cart_details=cart_details)
    
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@order_bp.route('/place', methods=['POST'])
def place_order():
    """
    Process checkout and create order.
    
    Expected form data:
        - username: str (4-20 characters)
        - password: str (minimum 8 characters)
        - email: str
        - address: str
    
    Returns:
        Redirect to order confirmation or error page
    """
    try:
        # Get form data
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        
        # Validate required fields
        if not all([username, password, email, address]):
            return render_template(
                'error.html',
                error='Tots els camps són obligatoris.'
            ), 400
        
        cart = get_cart()
        
        if not cart or len(cart) == 0:
            return render_template(
                'error.html',
                error='El carretó està buit.'
            ), 400
        
        # Register or authenticate user
        # First try to authenticate
        user = UserService.authenticate(username, password)
        
        if not user:
            # Try to register new user
            registration_result = UserService.register_user(username, password, email)
            
            if not registration_result['success']:
                return render_template(
                    'error.html',
                    error=registration_result['message']
                ), 400
            
            user_id = registration_result['user_id']
        else:
            user_id = user.id
        
        # Create order
        order_result = OrderService.create_order(cart, user_id)
        
        if not order_result['success']:
            return render_template(
                'error.html',
                error=order_result['message']
            ), 400
        
        # Save session
        session['cart'] = cart
        session.modified = True
        
        # Redirect to confirmation
        return redirect(url_for('orders.order_confirmation', order_id=order_result['order_id']))
    
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@order_bp.route('/confirmation/<int:order_id>')
def order_confirmation(order_id: int):
    """
    Display order confirmation page.
    
    Args:
        order_id: ID of the completed order
    
    Returns:
        Rendered confirmation template
    """
    try:
        order_details = OrderService.get_order_details(order_id)
        
        if not order_details:
            return render_template('error.html', error='Comanda no trobada.'), 404
        
        return render_template('order_confirmation.html', order_details=order_details)
    
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@order_bp.route('/<int:order_id>')
def show_order(order_id: int):
    """
    Display order details.
    
    Args:
        order_id: ID of the order
    
    Returns:
        Rendered order details template
    """
    try:
        order_details = OrderService.get_order_details(order_id)
        
        if not order_details:
            return render_template('error.html', error='Comanda no trobada.'), 404
        
        return render_template('order_details.html', order_details=order_details)
    
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

