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
from repositories.user_repository import UserRepository
from repositories.order_repository import OrderRepository
from repositories.order_item_repository import OrderItemRepository
from models.product import Product
from models.user import User
from models.order import Order
from models.order_item import OrderItem


def _seed_products():
    """Insert sample products if the table is empty."""
    if ProductRepository.get_all():
        return

    sample_products = [
        # Electrònica > Mòbils
        Product("iPhone 15 Pro",            1199.00, 15, "Electrònica", "Mòbils"),
        Product("iPhone 15",                 999.00, 20, "Electrònica", "Mòbils"),
        Product("Samsung Galaxy S24 Ultra", 1299.00, 12, "Electrònica", "Mòbils"),
        Product("Samsung Galaxy S24",        999.00, 18, "Electrònica", "Mòbils"),
        Product("Google Pixel 8 Pro",        899.00, 10, "Electrònica", "Mòbils"),
        Product("Google Pixel 8",            699.00, 14, "Electrònica", "Mòbils"),
        Product("OnePlus 12",                799.00, 16, "Electrònica", "Mòbils"),
        Product("Xiaomi 14 Pro",             799.00, 13, "Electrònica", "Mòbils"),
        Product("Motorola Edge 40",          499.00, 22, "Electrònica", "Mòbils"),
        Product("Sony Xperia 1 V",           999.00,  8, "Electrònica", "Mòbils"),
        # Electrònica > Portàtils
        Product("MacBook Air M2",           1299.00, 10, "Electrònica", "Portàtils"),
        Product("MacBook Pro M3",           1999.00,  7, "Electrònica", "Portàtils"),
        Product("Dell XPS 15",             1799.00,  8, "Electrònica", "Portàtils"),
        Product("Dell XPS 13",             1299.00, 11, "Electrònica", "Portàtils"),
        Product("HP Spectre x360",         1499.00,  9, "Electrònica", "Portàtils"),
        Product("Lenovo ThinkPad X1",      1599.00,  6, "Electrònica", "Portàtils"),
        Product("ASUS ZenBook 14",          999.00, 15, "Electrònica", "Portàtils"),
        Product("Acer Swift 5",             899.00, 17, "Electrònica", "Portàtils"),
        Product("Microsoft Surface Pro 9", 1299.00,  8, "Electrònica", "Portàtils"),
        Product("Razer Blade 15",          2499.00,  5, "Electrònica", "Portàtils"),
        # Electrònica > Tauletes
        Product('iPad Pro 12.9"',          1099.00, 12, "Electrònica", "Tauletes"),
        Product("iPad Air M1",              749.00, 16, "Electrònica", "Tauletes"),
        Product("iPad Mini 6",              549.00, 20, "Electrònica", "Tauletes"),
        Product("Samsung Galaxy Tab S9",    849.00, 14, "Electrònica", "Tauletes"),
        Product("Samsung Galaxy Tab A9",    299.00, 25, "Electrònica", "Tauletes"),
        Product("Lenovo Tab P12 Pro",       699.00, 11, "Electrònica", "Tauletes"),
        Product("Microsoft Surface Go 3",   599.00, 13, "Electrònica", "Tauletes"),
        # Electrònica > Auriculars
        Product("Sony WH-1000XM5",          399.00, 25, "Electrònica", "Auriculars"),
        Product("AirPods Pro 2",            279.00, 30, "Electrònica", "Auriculars"),
        Product("AirPods Max",              549.00, 12, "Electrònica", "Auriculars"),
        Product("Bose QuietComfort 45",     329.00, 18, "Electrònica", "Auriculars"),
        Product("Samsung Galaxy Buds2 Pro", 229.00, 22, "Electrònica", "Auriculars"),
        Product("Jabra Evolve2 85",         449.00,  9, "Electrònica", "Auriculars"),
        Product("Sennheiser Momentum 4",    349.00, 14, "Electrònica", "Auriculars"),
        # Electrònica > Rellotges Intel·ligents
        Product("Apple Watch Series 9",     449.00, 18, "Electrònica", "Rellotges Intel·ligents"),
        Product("Apple Watch Ultra 2",      799.00,  8, "Electrònica", "Rellotges Intel·ligents"),
        Product("Samsung Galaxy Watch 6",   299.00, 20, "Electrònica", "Rellotges Intel·ligents"),
        Product("Garmin Fenix 7",           699.00, 10, "Electrònica", "Rellotges Intel·ligents"),
        Product("Fitbit Sense 2",           249.00, 23, "Electrònica", "Rellotges Intel·ligents"),
        Product("Xiaomi Smart Band 8",       49.00, 40, "Electrònica", "Rellotges Intel·ligents"),
        # Electrodomèstics > Televisors
        Product('Samsung QLED 55"',         799.00, 10, "Electrodomèstics", "Televisors"),
        Product('LG OLED 65"',             1499.00,  6, "Electrodomèstics", "Televisors"),
        Product('Sony Bravia XR 55"',      1199.00,  8, "Electrodomèstics", "Televisors"),
        Product('Philips Ambilight 50"',    599.00, 12, "Electrodomèstics", "Televisors"),
        Product('Hisense ULED 58"',         499.00, 15, "Electrodomèstics", "Televisors"),
        Product('TCL 4K 43"',               299.00, 20, "Electrodomèstics", "Televisors"),
        # Electrodomèstics > Cuina
        Product("Thermomix TM6",           1299.00,  5, "Electrodomèstics", "Cuina"),
        Product("Nespresso Vertuo Next",    199.00, 25, "Electrodomèstics", "Cuina"),
        Product("Philips Airfryer XXL",     199.00, 22, "Electrodomèstics", "Cuina"),
        Product("KitchenAid Artisan",       499.00, 10, "Electrodomèstics", "Cuina"),
        Product("Instant Pot Duo 7-in-1",   129.00, 18, "Electrodomèstics", "Cuina"),
        Product("Vitamix A3500",            599.00,  8, "Electrodomèstics", "Cuina"),
        Product("De'Longhi Magnifica Evo",  699.00,  9, "Electrodomèstics", "Cuina"),
        # Electrodomèstics > Neteja
        Product("Roomba j9+",               799.00,  8, "Electrodomèstics", "Neteja"),
        Product("Dyson V15 Detect",         699.00, 10, "Electrodomèstics", "Neteja"),
        Product("Dyson V12 Slim",           499.00, 14, "Electrodomèstics", "Neteja"),
        Product("Roborock S8 Pro",          699.00,  7, "Electrodomèstics", "Neteja"),
        Product("Miele Complete C3",        499.00, 11, "Electrodomèstics", "Neteja"),
        # Informàtica > Perifèrics
        Product("Logitech MX Master 3S",     99.00, 35, "Informàtica", "Perifèrics"),
        Product("Logitech MX Keys",         109.00, 28, "Informàtica", "Perifèrics"),
        Product("Apple Magic Keyboard",     129.00, 20, "Informàtica", "Perifèrics"),
        Product("Apple Magic Mouse",         79.00, 22, "Informàtica", "Perifèrics"),
        Product("Razer DeathAdder V3",       99.00, 18, "Informàtica", "Perifèrics"),
        Product("Corsair K100 RGB",         199.00, 12, "Informàtica", "Perifèrics"),
        Product("SteelSeries Apex Pro",     179.00, 14, "Informàtica", "Perifèrics"),
        # Informàtica > Monitors
        Product('Samsung 4K Monitor 27"',   399.00, 14, "Informàtica", "Monitors"),
        Product('LG UltraWide 34"',         499.00, 10, "Informàtica", "Monitors"),
        Product('Dell UltraSharp 27"',      549.00,  9, "Informàtica", "Monitors"),
        Product('ASUS ProArt 32"',          699.00,  7, "Informàtica", "Monitors"),
        Product('BenQ PD2725U 27"',         599.00,  8, "Informàtica", "Monitors"),
        # Informàtica > Emmagatzematge
        Product("Samsung SSD 1TB",          109.00, 30, "Informàtica", "Emmagatzematge"),
        Product("WD Black SSD 2TB",         179.00, 20, "Informàtica", "Emmagatzematge"),
        Product("Seagate HDD 4TB",           89.00, 25, "Informàtica", "Emmagatzematge"),
        Product("SanDisk Extreme SSD 1TB",   99.00, 28, "Informàtica", "Emmagatzematge"),
        Product("Kingston NV2 SSD 2TB",     129.00, 22, "Informàtica", "Emmagatzematge"),
        # Gaming > Consoles
        Product("PlayStation 5",            549.00,  5, "Gaming", "Consoles"),
        Product("Xbox Series X",            499.00,  7, "Gaming", "Consoles"),
        Product("Nintendo Switch OLED",     349.00, 22, "Gaming", "Consoles"),
        Product("Nintendo Switch Lite",     219.00, 28, "Gaming", "Consoles"),
        Product("Steam Deck OLED",          549.00,  9, "Gaming", "Consoles"),
        # Gaming > Accessoris
        Product("DualSense PS5",             69.00, 30, "Gaming", "Accessoris"),
        Product("Xbox Elite Controller 2",  179.00, 15, "Gaming", "Accessoris"),
        Product("Razer Wolverine V2",       149.00, 18, "Gaming", "Accessoris"),
        Product("HyperX Cloud Alpha",       129.00, 20, "Gaming", "Accessoris"),
        Product("Astro A50 Wireless",       299.00, 10, "Gaming", "Accessoris"),
        # Fotografia > Càmeres
        Product("Sony A7 IV",              2499.00,  4, "Fotografia", "Càmeres"),
        Product("Canon EOS R6 Mark II",    2699.00,  3, "Fotografia", "Càmeres"),
        Product("Nikon Z6 III",            2199.00,  5, "Fotografia", "Càmeres"),
        Product("Fujifilm X-T5",           1699.00,  6, "Fotografia", "Càmeres"),
        Product("GoPro Hero 12",            399.00, 11, "Fotografia", "Càmeres"),
        Product("DJI Osmo Pocket 3",        519.00,  8, "Fotografia", "Càmeres"),
        # Fotografia > Accessoris
        Product("DJI Mini 4 Pro",           759.00,  7, "Fotografia", "Accessoris"),
        Product("Rode VideoMic Pro+",       299.00, 12, "Fotografia", "Accessoris"),
        Product("Joby GorillaPod 3K",        79.00, 20, "Fotografia", "Accessoris"),
        # Lectors > E-readers
        Product("Kindle Paperwhite",        149.00, 40, "Lectors", "E-readers"),
        Product("Kindle Scribe",            369.00, 18, "Lectors", "E-readers"),
        Product("Kobo Libra 2",             179.00, 22, "Lectors", "E-readers"),
        Product("Kobo Elipsa 2E",           399.00, 12, "Lectors", "E-readers"),
    ]
    for product in sample_products:
        ProductRepository.create(product)
    print(f"✓ {len(sample_products)} productes inserits")
    _seed_users_and_orders()


def _seed_users_and_orders():
    """Insert sample users and orders if tables are empty."""
    import random
    from datetime import datetime, timedelta

    if UserRepository.get_all():
        return

    ubicacions = [
        ("Barcelona",  "Barcelona",       "Espanya"),
        ("Madrid",     "Madrid",          "Espanya"),
        ("València",   "València",        "Espanya"),
        ("Sevilla",    "Andalusia",       "Espanya"),
        ("Bilbao",     "País Basc",       "Espanya"),
        ("Saragossa",  "Aragó",           "Espanya"),
        ("Màlaga",     "Andalusia",       "Espanya"),
        ("Palma",      "Illes Balears",   "Espanya"),
        ("Las Palmas", "Canàries",        "Espanya"),
        ("Alacant",    "València",        "Espanya"),
        ("Girona",     "Catalunya",       "Espanya"),
        ("Tarragona",  "Catalunya",       "Espanya"),
        ("Lleida",     "Catalunya",       "Espanya"),
        ("Murcia",     "Múrcia",          "Espanya"),
        ("Valladolid", "Castella i Lleó", "Espanya"),
    ]
    segments = ["Jove", "Adult", "Professional", "Sènior"]

    users = []
    for i in range(1, 51):
        ciutat, provincia, pais = random.choice(ubicacions)
        segment = random.choice(segments)
        edat = random.randint(18, 70)
        u = User(
            username=f"user{i:02d}",
            password_hash="$2b$12$placeholder_hash",
            email=f"user{i:02d}@techshop.com",
            edat=edat,
            segment=segment,
            ciutat=ciutat,
            provincia=provincia,
            pais=pais,
        )
        uid = UserRepository.create(u)
        u.id = uid
        users.append(u)

    print(f"✓ {len(users)} usuaris inserits")

    products = ProductRepository.get_all()
    now = datetime.now()
    orders_created = 0

    for _ in range(200):
        user = random.choice(users)
        days_ago = random.randint(0, 365)
        order_date = now - timedelta(days=days_ago)
        num_items = random.randint(1, 4)
        selected = random.sample(products, min(num_items, len(products)))
        total = sum(float(p.price) * random.randint(1, 3) for p in selected)

        order = Order(
            total=round(total, 2),
            user_id=user.id,
            created_at=order_date,
            ciutat=user.ciutat,
            provincia=user.provincia,
            pais=user.pais,
        )
        oid = OrderRepository.create(order)

        for p in selected:
            qty = random.randint(1, 3)
            OrderItemRepository.create(OrderItem(order_id=oid, product_id=p.id, quantity=qty))

        orders_created += 1

    print(f"✓ {orders_created} comandes inserides")


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

