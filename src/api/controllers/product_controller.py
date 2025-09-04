from flask import Blueprint, request, jsonify
from infrastructure.databases.mssql import get_db_session
from infrastructure.repositories.product_repository import ProductRepository
from services.product_service import ProductService

product_bp = Blueprint("product", __name__, url_prefix="/api/products")

def get_service():
    db = get_db_session()
    return ProductService(ProductRepository(db))

@product_bp.get("/")
def list_products():
    service = ProductService(ProductRepositoryImpl())
    products = service.get_products()
    return jsonify([p.__dict__ for p in products])

@product_bp.get("/products",methods=["GET"])
def get_all_products():
    try:
        service = get_service()

        product_list = service.get_all_products()
        # Lưu list sản phẩm vào biến product_list
        if not product_list:
            return jsonify({"success": False, "message": "No products found"}), 404
        return jsonify({"success": True, "products": product_list }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500