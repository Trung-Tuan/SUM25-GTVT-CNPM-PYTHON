from flask import Blueprint, request, jsonify, current_app
import jwt
from infrastructure.databases.mssql import get_db_session
from infrastructure.repositories.order_repository import OrderRepository, PaymentRepository
from infrastructure.repositories.cart_repository import CartRepository
from infrastructure.repositories.product_repository import ProductRepository
from services.order_service import OrderService
from api.schemas.order_schema import OrderResponseSchema, OrderListResponseSchema, PaymentResponseSchema
from domain.exceptions import OrderNotFoundError, PaymentFailedError, InsufficientStockError

order_bp = Blueprint("order", __name__, url_prefix="/api")

def get_order_service():
    db = get_db_session()
    order_repo = OrderRepository(db)
    payment_repo = PaymentRepository(db)
    cart_repo = CartRepository(db)
    product_repo = ProductRepository(db)
    return OrderService(order_repo, payment_repo, cart_repo, product_repo)

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

@order_bp.route("/orders", methods=["POST"])
def create_order():
    """
    Tạo đơn hàng từ giỏ hàng
    ---
    post:
      summary: Create order from cart
      tags:
        - Orders
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                shipping_address:
                  type: string
                  description: Shipping address
                order_type:
                  type: string
                  description: Type of order (buy or rent)
                  enum: [buy, rent]
                  default: buy
      responses:
        201:
          description: Order created successfully
        400:
          description: Bad request
        401:
          description: Unauthorized
        404:
          description: Cart is empty
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        data = request.get_json()
        
        shipping_address = data.get('shipping_address')
        order_type = data.get('order_type', 'buy')
        
        if not shipping_address:
            return jsonify({
                "success": False,
                "error": "shipping_address is required"
            }), 400
        
        service = get_order_service()
        order = service.create_order_from_cart(
            user_id=user_id,
            shipping_address=shipping_address,
            order_type=order_type
        )
        
        order_schema = OrderResponseSchema()
        order_data = order_schema.dump(order)
        
        return jsonify({
            "success": True,
            "message": "Order created successfully",
            "order": order_data
        }), 201
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except InsufficientStockError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@order_bp.route("/orders/<int:order_id>/pay", methods=["POST"])
def process_payment():
    """
    Xử lý thanh toán cho đơn hàng
    ---
    post:
      summary: Process payment for order
      tags:
        - Orders
      security:
        - Bearer: []
      parameters:
        - in: path
          name: order_id
          required: true
          schema:
            type: integer
          description: Order ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                payment_method:
                  type: string
                  description: Payment method
                  enum: [credit_card, debit_card, bank_transfer, wallet]
                transaction_id:
                  type: string
                  description: External transaction ID (optional)
      responses:
        200:
          description: Payment processed successfully
        400:
          description: Bad request
        401:
          description: Unauthorized
        404:
          description: Order not found
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        order_id = request.view_args['order_id']
        data = request.get_json()
        
        payment_method = data.get('payment_method')
        transaction_id = data.get('transaction_id')
        
        if not payment_method:
            return jsonify({
                "success": False,
                "error": "payment_method is required"
            }), 400
        
        service = get_order_service()
        payment = service.process_payment(
            order_id=order_id,
            payment_method=payment_method,
            transaction_id=transaction_id
        )
        
        payment_schema = PaymentResponseSchema()
        payment_data = payment_schema.dump(payment)
        
        return jsonify({
            "success": True,
            "message": "Payment processed successfully",
            "payment": payment_data
        }), 200
        
    except OrderNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
        
    except PaymentFailedError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order():
    """
    Lấy thông tin đơn hàng
    ---
    get:
      summary: Get order details
      tags:
        - Orders
      security:
        - Bearer: []
      parameters:
        - in: path
          name: order_id
          required: true
          schema:
            type: integer
          description: Order ID
      responses:
        200:
          description: Order details retrieved successfully
        401:
          description: Unauthorized
        404:
          description: Order not found
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        order_id = request.view_args['order_id']
        service = get_order_service()
        
        order = service.get_order(order_id)
        order_schema = OrderResponseSchema()
        order_data = order_schema.dump(order)
        
        return jsonify({
            "success": True,
            "order": order_data
        }), 200
        
    except OrderNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@order_bp.route("/orders", methods=["GET"])
def get_user_orders():
    """
    Lấy danh sách đơn hàng của user
    ---
    get:
      summary: Get user's orders
      tags:
        - Orders
      security:
        - Bearer: []
      responses:
        200:
          description: Orders retrieved successfully
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
        
        service = get_order_service()
        
        orders = service.get_user_orders(user_id)
        order_schema = OrderResponseSchema(many=True)
        orders_data = order_schema.dump(orders)
        
        return jsonify({
            "success": True,
            "orders": orders_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@order_bp.route("/orders/<int:order_id>/cancel", methods=["PUT"])
def cancel_order():
    """
    Hủy đơn hàng
    ---
    put:
      summary: Cancel order
      tags:
        - Orders
      security:
        - Bearer: []
      parameters:
        - in: path
          name: order_id
          required: true
          schema:
            type: integer
          description: Order ID
      responses:
        200:
          description: Order cancelled successfully
        400:
          description: Bad request
        401:
          description: Unauthorized
        404:
          description: Order not found
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        order_id = request.view_args['order_id']
        service = get_order_service()
        
        order = service.cancel_order(order_id)
        order_schema = OrderResponseSchema()
        order_data = order_schema.dump(order)
        
        return jsonify({
            "success": True,
            "message": "Order cancelled successfully",
            "order": order_data
        }), 200
        
    except OrderNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@order_bp.route("/orders/<int:order_id>/refund", methods=["POST"])
def refund_order():
    """
    Hoàn tiền cho đơn hàng
    ---
    post:
      summary: Refund order
      tags:
        - Orders
      security:
        - Bearer: []
      parameters:
        - in: path
          name: order_id
          required: true
          schema:
            type: integer
          description: Order ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                refund_amount:
                  type: number
                  description: Refund amount
      responses:
        200:
          description: Refund processed successfully
        400:
          description: Bad request
        401:
          description: Unauthorized
        404:
          description: Order not found
    """
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid or missing token"
            }), 401
        
        order_id = request.view_args['order_id']
        data = request.get_json()
        
        refund_amount = data.get('refund_amount')
        if not refund_amount:
            return jsonify({
                "success": False,
                "error": "refund_amount is required"
            }), 400
        
        service = get_order_service()
        payment = service.refund_payment(order_id, refund_amount)
        
        payment_schema = PaymentResponseSchema()
        payment_data = payment_schema.dump(payment)
        
        return jsonify({
            "success": True,
            "message": "Refund processed successfully",
            "payment": payment_data
        }), 200
        
    except OrderNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500