from flask import Blueprint, jsonify
from src.services.product_service import ProductService
from src.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl

bp = Blueprint("product", __name__, url_prefix="/api/products")

@bp.get("/")
def list_products():
    service = ProductService(ProductRepositoryImpl())
    products = service.get_products()
    return jsonify([p.__dict__ for p in products])
