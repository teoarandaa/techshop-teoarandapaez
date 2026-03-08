"""
OData v4 endpoints for Tableau Public integration.
Exposes products, orders, order_items and users as OData feeds.
"""

from flask import Blueprint, jsonify, request, make_response
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from repositories.order_item_repository import OrderItemRepository
from repositories.user_repository import UserRepository

odata_bp = Blueprint('odata', __name__, url_prefix='/odata')

ODATA_HEADERS = {
    'OData-Version': '4.0',
    'Content-Type': 'application/json;odata.metadata=minimal;odata.streaming=true',
}


def _base_url():
    return request.host_url.rstrip('/')


def _odata_response(data):
    resp = make_response(jsonify(data))
    for k, v in ODATA_HEADERS.items():
        resp.headers[k] = v
    return resp


@odata_bp.route('/', methods=['GET'])
def service_document():
    """OData service document — lists all available entity sets."""
    base = _base_url()
    return _odata_response({
        "@odata.context": f"{base}/odata/$metadata",
        "value": [
            {"name": "products",    "kind": "EntitySet", "url": "products"},
            {"name": "orders",      "kind": "EntitySet", "url": "orders"},
            {"name": "order_items", "kind": "EntitySet", "url": "order_items"},
            {"name": "users",       "kind": "EntitySet", "url": "users"},
        ]
    })


@odata_bp.route('/$metadata', methods=['GET'])
def metadata():
    """Minimal OData $metadata document (EDMX)."""
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="TechShop" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EntityType Name="Product">
        <Key><PropertyRef Name="id"/></Key>
        <Property Name="id"    Type="Edm.Int32"   Nullable="false"/>
        <Property Name="name"  Type="Edm.String"/>
        <Property Name="price" Type="Edm.Decimal"/>
        <Property Name="stock" Type="Edm.Int32"/>
      </EntityType>
      <EntityType Name="Order">
        <Key><PropertyRef Name="id"/></Key>
        <Property Name="id"         Type="Edm.Int32"    Nullable="false"/>
        <Property Name="total"      Type="Edm.Decimal"/>
        <Property Name="created_at" Type="Edm.DateTimeOffset"/>
        <Property Name="user_id"    Type="Edm.Int32"/>
      </EntityType>
      <EntityType Name="OrderItem">
        <Key><PropertyRef Name="id"/></Key>
        <Property Name="id"         Type="Edm.Int32" Nullable="false"/>
        <Property Name="order_id"   Type="Edm.Int32"/>
        <Property Name="product_id" Type="Edm.Int32"/>
        <Property Name="quantity"   Type="Edm.Int32"/>
      </EntityType>
      <EntityType Name="User">
        <Key><PropertyRef Name="id"/></Key>
        <Property Name="id"         Type="Edm.Int32"  Nullable="false"/>
        <Property Name="username"   Type="Edm.String"/>
        <Property Name="email"      Type="Edm.String"/>
        <Property Name="created_at" Type="Edm.DateTimeOffset"/>
      </EntityType>
      <EntityContainer Name="TechShopContainer">
        <EntitySet Name="products"    EntityType="TechShop.Product"/>
        <EntitySet Name="orders"      EntityType="TechShop.Order"/>
        <EntitySet Name="order_items" EntityType="TechShop.OrderItem"/>
        <EntitySet Name="users"       EntityType="TechShop.User"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>'''
    return xml, 200, {
        'Content-Type': 'application/xml',
        'OData-Version': '4.0',
    }


@odata_bp.route('/products', methods=['GET'])
def get_products():
    products = ProductRepository.get_all()
    return _odata_response({
        "@odata.context": f"{_base_url()}/odata/$metadata#products",
        "value": [p.to_dict() for p in products]
    })


@odata_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = OrderRepository.get_all()
    return _odata_response({
        "@odata.context": f"{_base_url()}/odata/$metadata#orders",
        "value": [o.to_dict() for o in orders]
    })


@odata_bp.route('/order_items', methods=['GET'])
def get_order_items():
    items = OrderItemRepository.get_all()
    return _odata_response({
        "@odata.context": f"{_base_url()}/odata/$metadata#order_items",
        "value": [i.to_dict() for i in items]
    })


@odata_bp.route('/users', methods=['GET'])
def get_users():
    users = UserRepository.get_all()
    return _odata_response({
        "@odata.context": f"{_base_url()}/odata/$metadata#users",
        "value": [u.to_dict() for u in users]
    })
