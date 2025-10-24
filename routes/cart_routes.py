"""
Cart routes - Handles shopping cart operations.
Presentation layer for cart management.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from services.cart_service import CartService
from repositories.product_repository import ProductRepository

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


def get_cart():
    """
    Get cart from session.
    
    Returns:
        dict: Cart dictionary {product_id: quantity}
    """
    if 'cart' not in session:
        session['cart'] = {}
    
    # Ensure cart is a dictionary with integer keys
    cart = session.get('cart', {})
    if not isinstance(cart, dict):
        session['cart'] = {}
        return session['cart']
    
    # Convert string keys to integers if needed
    normalized_cart = {}
    for key, value in cart.items():
        try:
            normalized_cart[int(key)] = int(value)
        except (ValueError, TypeError):
            pass
    
    session['cart'] = normalized_cart
    return session['cart']


@cart_bp.route('/')
def show_cart():
    """
    Display shopping cart page.
    
    Returns:
        Rendered template with cart contents
    """
    try:
        cart = get_cart()
        cart_details = CartService.get_cart_details(cart)
        return render_template('cart.html', cart_details=cart_details)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """
    Add a product to the cart.
    
    Expected form data:
        - product_id: int
        - quantity: int (default: 1)
    
    Returns:
        JSON response with result or redirect
    """
    try:
        product_id = request.form.get('product_id', type=int)
        quantity = request.form.get('quantity', 1, type=int)
        
        if not product_id:
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'ID de producte no vàlid.'
                }), 400
            return redirect(url_for('products.show_products'))
        
        cart = get_cart()
        result = CartService.add_to_cart(cart, product_id, quantity)
        
        # Save updated cart to session
        session['cart'] = cart
        session.modified = True
        
        # Return JSON for AJAX requests
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_details = CartService.get_cart_details(cart)
            return jsonify({
                **result,
                'cart_count': cart_details['item_count']
            })
        
        # Redirect for form submissions
        if result['success']:
            return redirect(url_for('cart.show_cart'))
        else:
            return render_template('error.html', error=result['message']), 400
    
    except Exception as e:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
        return render_template('error.html', error=str(e)), 500


@cart_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id: int):
    """
    Remove a product from the cart.
    
    Args:
        product_id: ID of the product to remove
    
    Returns:
        JSON response or redirect
    """
    try:
        cart = get_cart()
        result = CartService.remove_from_cart(cart, product_id)
        
        session['cart'] = cart
        session.modified = True
        
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_details = CartService.get_cart_details(cart)
            return jsonify({
                **result,
                'cart_count': cart_details['item_count']
            })
        
        return redirect(url_for('cart.show_cart'))
    
    except Exception as e:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
        return render_template('error.html', error=str(e)), 500


@cart_bp.route('/update/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id: int):
    """
    Update quantity of a product in the cart.
    
    Args:
        product_id: ID of the product to update
    
    Expected form data:
        - quantity: int
    
    Returns:
        JSON response or redirect
    """
    try:
        quantity = request.form.get('quantity', type=int)
        
        if quantity is None:
            return jsonify({
                'success': False,
                'message': 'Quantitat no vàlida.'
            }), 400
        
        cart = get_cart()
        result = CartService.update_quantity(cart, product_id, quantity)
        
        session['cart'] = cart
        session.modified = True
        
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_details = CartService.get_cart_details(cart)
            return jsonify({
                **result,
                'cart_count': cart_details['item_count'],
                'cart_total': float(cart_details['total'])
            })
        
        return redirect(url_for('cart.show_cart'))
    
    except Exception as e:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
        return render_template('error.html', error=str(e)), 500


@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    """
    Clear all items from the cart.
    
    Returns:
        JSON response or redirect
    """
    try:
        cart = get_cart()
        CartService.clear_cart(cart)
        
        session['cart'] = cart
        session.modified = True
        
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Carretó buidat.',
                'cart_count': 0
            })
        
        return redirect(url_for('cart.show_cart'))
    
    except Exception as e:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
        return render_template('error.html', error=str(e)), 500

