"""
TechShop - E-commerce Flask Application
Main application entry point implementing MVC architecture.
"""

import os
from flask import Flask, render_template, session
from database import db
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.odata_routes import odata_bp
from repositories.product_repository import ProductRepository
from models.product import Product


def _seed_products():
    """Insert sample products if the table is empty."""
    if ProductRepository.get_all():
        return
    sample_products = [
        Product(name="iPhone 15 Pro",         price=1199.00, stock=15),
        Product(name="Samsung Galaxy S24",     price=999.00,  stock=20),
        Product(name="MacBook Air M2",         price=1299.00, stock=10),
        Product(name='iPad Pro 12.9"',         price=1099.00, stock=12),
        Product(name="Sony WH-1000XM5",        price=399.00,  stock=25),
        Product(name="Apple Watch Series 9",   price=449.00,  stock=18),
        Product(name="Dell XPS 15",            price=1799.00, stock=8),
        Product(name="AirPods Pro 2",          price=279.00,  stock=30),
        Product(name="Nintendo Switch OLED",   price=349.00,  stock=22),
        Product(name="PlayStation 5",          price=549.00,  stock=5),
        Product(name='Samsung 4K Monitor 27"', price=399.00,  stock=14),
        Product(name="Logitech MX Master 3S",  price=99.00,   stock=35),
        Product(name="iPad Mini 6",            price=549.00,  stock=16),
        Product(name="Kindle Paperwhite",      price=149.00,  stock=40),
        Product(name="GoPro Hero 12",          price=399.00,  stock=11),
    ]
    for product in sample_products:
        ProductRepository.create(product)
    print(f"✓ {len(sample_products)} productes inserits a la base de dades")


def create_app():
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DATABASE_PATH'] = os.environ.get('DATABASE_PATH', 'techshop.db')
    
    # Initialize database and seed products if empty
    db.init_db()
    _seed_products()
    
    # Register blueprints (routes)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(odata_bp)
    
    # Home route
    @app.route('/')
    def index():
        """
        Home page - redirect to products listing.
        """
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('error.html', error='Pàgina no trobada.'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return render_template('error.html', error='Error intern del servidor.'), 500
    
    # Template context processor for cart count
    @app.context_processor
    def inject_cart_count():
        """
        Inject cart item count into all templates.
        
        Returns:
            dict: Context variables for templates
        """
        try:
            cart = session.get('cart', {})
            
            # Ensure cart is a dict
            if not isinstance(cart, dict):
                cart = {}
            
            # Calculate count safely
            cart_count = 0
            if cart and isinstance(cart, dict):
                try:
                    cart_count = sum(cart.values())
                except (TypeError, AttributeError):
                    cart_count = 0
            
            return {'cart_count': cart_count}
        except Exception as e:
            print(f"ERROR in inject_cart_count: {e}")
            return {'cart_count': 0}
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)

