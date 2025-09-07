from flask import Blueprint, request, jsonify, current_app
import jwt
from infrastructure.databases.mssql import get_db_session
from infrastructure.repositories.cart_repository import CartRepository
from infrastructure.repositories.product_repository import ProductRepository
from services.cart_service import CartService
from api.schemas.cart_schema import CartResponseSchema, CartItemResponseSchema
from domain.exceptions import ProductNotFoundError

cart_bp = Blueprint("cart", __name__, url_prefix="/api")

def get_cart_service():
    db = get_db_session()
    cart_repo = CartRepository(db)
    product_repo = ProductRepository(db)
    return CartService(cart_repo, product_repo)

def get_user_id_from_token():
    """Helper function to get user ID from JWT token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@cart_bp.route("/cart", methods=["GET"])
def get_cart():
    """
    Lấy giỏ hàng của user hiện tại
    ---
    get:
      summary: Get user's cart
      tags:
        - Cart
      security:
        - Bearer: []
      responses:
        200:
          description: Cart retrieved successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CartResponse'
        401:
          description: Unauthorized
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        service = get_cart_service()
        
        cart = service.get_cart(user_id)
        cart_schema = CartResponseSchema()
        cart_data = cart_schema.dump(cart)
        
        return jsonify({
            "success": True,
            "cart": cart_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@cart_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    """
    Thêm sản phẩm vào giỏ hàng
    ---
    post:
      summary: Add product to cart
      tags:
        - Cart
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                product_id:
                  type: integer
                  description: ID of the product
                quantity:
                  type: integer
                  description: Quantity to add
                  default: 1
                item_type:
                  type: string
                  description: Type of item (buy or rent)
                  enum: [buy, rent]
                  default: buy
                rental_days:
                  type: integer
                  description: Number of rental days (required for rent)
      responses:
        200:
          description: Product added to cart successfully
        400:
          description: Bad request
        401:
          description: Unauthorized
        404:
          description: Product not found
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        data = request.get_json()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        item_type = data.get('item_type', 'buy')
        rental_days = data.get('rental_days')
        
        if not product_id:
            return jsonify({
                "success": False,
                "error": "product_id is required"
            }), 400
        
        if item_type == 'rent' and not rental_days:
            return jsonify({
                "success": False,
                "error": "rental_days is required for rent items"
            }), 400
        
        service = get_cart_service()
        cart = service.add_to_cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            item_type=item_type,
            rental_days=rental_days
        )
        
        cart_schema = CartResponseSchema()
        cart_data = cart_schema.dump(cart)
        
        return jsonify({
            "success": True,
            "message": "Product added to cart successfully",
            "cart": cart_data
        }), 200
        
    except ProductNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@cart_bp.route("/cart/update", methods=["PUT"])
def update_cart_item():
    """
    Cập nhật số lượng sản phẩm trong giỏ hàng
    ---
    put:
      summary: Update cart item quantity
      tags:
        - Cart
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                product_id:
                  type: integer
                  description: ID of the product
                quantity:
                  type: integer
                  description: New quantity
                item_type:
                  type: string
                  description: Type of item (buy or rent)
                  enum: [buy, rent]
                  default: buy
      responses:
        200:
          description: Cart item updated successfully
        400:
          description: Bad request
        401:
          description: Unauthorized
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        data = request.get_json()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        item_type = data.get('item_type', 'buy')
        
        if not product_id or quantity is None:
            return jsonify({
                "success": False,
                "error": "product_id and quantity are required"
            }), 400
        
        service = get_cart_service()
        cart = service.update_cart_item(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            item_type=item_type
        )
        
        cart_schema = CartResponseSchema()
        cart_data = cart_schema.dump(cart)
        
        return jsonify({
            "success": True,
            "message": "Cart item updated successfully",
            "cart": cart_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@cart_bp.route("/cart/remove", methods=["DELETE"])
def remove_from_cart():
    """
    Xóa sản phẩm khỏi giỏ hàng
    ---
    delete:
      summary: Remove product from cart
      tags:
        - Cart
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                product_id:
                  type: integer
                  description: ID of the product
                item_type:
                  type: string
                  description: Type of item (buy or rent)
                  enum: [buy, rent]
                  default: buy
      responses:
        200:
          description: Product removed from cart successfully
        400:
          description: Bad request
        401:
          description: Unauthorized
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        data = request.get_json()
        
        product_id = data.get('product_id')
        item_type = data.get('item_type', 'buy')
        
        if not product_id:
            return jsonify({
                "success": False,
                "error": "product_id is required"
            }), 400
        
        service = get_cart_service()
        cart = service.remove_from_cart(
            user_id=user_id,
            product_id=product_id,
            item_type=item_type
        )
        
        cart_schema = CartResponseSchema()
        cart_data = cart_schema.dump(cart)
        
        return jsonify({
            "success": True,
            "message": "Product removed from cart successfully",
            "cart": cart_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@cart_bp.route("/cart/clear", methods=["DELETE"])
def clear_cart():
    """
    Xóa toàn bộ giỏ hàng
    ---
    delete:
      summary: Clear entire cart
      tags:
        - Cart
      security:
        - Bearer: []
      responses:
        200:
          description: Cart cleared successfully
        401:
          description: Unauthorized
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        service = get_cart_service()
        
        cart = service.clear_cart(user_id)
        cart_schema = CartResponseSchema()
        cart_data = cart_schema.dump(cart)
        
        return jsonify({
            "success": True,
            "message": "Cart cleared successfully",
            "cart": cart_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500