"""
Database initialization script.
Creates database schema and populates with sample data for testing.
"""

from dotenv import load_dotenv
load_dotenv()

from database import db
from models.product import Product
from repositories.product_repository import ProductRepository


def init_database():
    """
    Initialize database with schema and sample data.
    """
    print("Inicialitzant base de dades...")
    
    # Create schema
    db.init_db()
    print("✓ Esquema de base de dades creat")
    
    # Add sample products
    sample_products = [
        Product(
            name="iPhone 15 Pro",
            price=1199.00,
            stock=15
        ),
        Product(
            name="Samsung Galaxy S24",
            price=999.00,
            stock=20
        ),
        Product(
            name="MacBook Air M2",
            price=1299.00,
            stock=10
        ),
        Product(
            name="iPad Pro 12.9\"",
            price=1099.00,
            stock=12
        ),
        Product(
            name="Sony WH-1000XM5",
            price=399.00,
            stock=25
        ),
        Product(
            name="Apple Watch Series 9",
            price=449.00,
            stock=18
        ),
        Product(
            name="Dell XPS 15",
            price=1799.00,
            stock=8
        ),
        Product(
            name="AirPods Pro 2",
            price=279.00,
            stock=30
        ),
        Product(
            name="Nintendo Switch OLED",
            price=349.00,
            stock=22
        ),
        Product(
            name="PlayStation 5",
            price=549.00,
            stock=5
        ),
        Product(
            name="Samsung 4K Monitor 27\"",
            price=399.00,
            stock=14
        ),
        Product(
            name="Logitech MX Master 3S",
            price=99.00,
            stock=35
        ),
        Product(
            name="iPad Mini 6",
            price=549.00,
            stock=16
        ),
        Product(
            name="Kindle Paperwhite",
            price=149.00,
            stock=40
        ),
        Product(
            name="GoPro Hero 12",
            price=399.00,
            stock=11
        )
    ]
    
    for product in sample_products:
        ProductRepository.create(product)
    
    print(f"✓ {len(sample_products)} productes afegits")
    print("\n✅ Base de dades inicialitzada correctament!")
    print("\nProductes disponibles:")
    
    # Display products
    products = ProductRepository.get_all()
    for product in products:
        print(f"  - {product.name}: {product.price}€ (Stock: {product.stock})")


def reset_database():
    """
    Reset database (drop all tables and recreate).
    WARNING: This deletes all data!
    """
    print("⚠️  ATENCIÓ: Això eliminarà totes les dades!")
    confirm = input("Estàs segur? Escriu 'SÍ' per confirmar: ")
    
    if confirm == "SÍ":
        db.reset_db()
        print("✓ Base de dades resetejada")
        init_database()
    else:
        print("Operació cancel·lada")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()

