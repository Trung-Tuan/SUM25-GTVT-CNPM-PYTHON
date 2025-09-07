from flask import Blueprint, request, jsonify
from infrastructure.databases.mssql import get_db_session
from infrastructure.repositories.product_repository import ProductRepository
from services.product_service import ProductService
from api.schemas.product_schema import ProductResponseSchema, ProductListResponseSchema

product_bp = Blueprint("product", __name__, url_prefix="/api")

def get_service():
    db = get_db_session()
    return ProductService(ProductRepository(db))

# @product_bp.get("/")
# def list_products():
#     service = ProductService(ProductRepositoryImpl())
#     products = service.get_products()
#     return jsonify([p.__dict__ for p in products])

@product_bp.route("/products",methods=["GET"])
def get_all_products():
    try:
        service = get_service()

        product_list = service.get_all_products() # [<Product id=1>, <Product id=2>, <Product id=3>]
        # Lưu list sản phẩm vào biến product_list
        if not product_list:
            return jsonify({"success": False, "message": "Không tìm thấy sản phẩm nào"}), 404
        
        product_schema = ProductResponseSchema(many=True)  # many=True để serialize một list
        products_data = product_schema.dump(product_list) # {"id": 1, "name": "Xe đồ chơi", "price": 100000, ...},...

        return jsonify({"success": True, "products": products_data }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@product_bp.route("/products/featured", methods=["GET"])
def get_featured_products():
    try:
        service = get_service()
        featured_products = service.get_featured_products()
        if not featured_products:
            return jsonify({"success": False, "message": "Không tìm thấy sản phẩm nổi bật nào"}), 404
        
        product_schema = ProductResponseSchema(many=True)
        products_data = product_schema.dump(featured_products)
        return jsonify({"success": True, "featured_products": products_data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@product_bp.route("/categories", methods=["GET"])
def get_categories():
    try:
        service = get_service()
        categories = service.get_all_categories()
        return jsonify({"success": True, "categories": categories}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500