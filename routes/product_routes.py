"""
Product routes - Handles product listing and display.
Presentation layer for products.
"""

from flask import Blueprint, render_template, jsonify
from repositories.product_repository import ProductRepository

product_bp = Blueprint('products', __name__, url_prefix='/products')


@product_bp.route('/')
def show_products():
    """
    Display all available products.
    
    Returns:
        Rendered template with product list
    """
    try:
        products = ProductRepository.get_all()
        return render_template('products.html', products=products)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@product_bp.route('/api')
def get_products_api():
    """
    API endpoint to get all products as JSON.
    
    Returns:
        JSON response with product list
    """
    try:
        products = ProductRepository.get_all()
        return jsonify({
            'success': True,
            'products': [product.to_dict() for product in products]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@product_bp.route('/<int:product_id>')
def show_product_detail(product_id: int):
    """
    Display details for a specific product.
    
    Args:
        product_id: ID of the product
    
    Returns:
        Rendered template with product details
    """
    try:
        product = ProductRepository.find_by_id(product_id)
        if not product:
            return render_template('error.html', error='Producte no trobat.'), 404
        
        return render_template('product_detail.html', product=product)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

