from typing import List, Optional
from datetime import datetime, timedelta
from domain.models.order import Order, OrderItem, Payment, OrderStatus, PaymentStatus
from domain.models.iorder_repository import IOrderRepository, IPaymentRepository
from domain.models.icart_repository import ICartRepository
from domain.models.iproduct_repository import IProductRepository
from domain.exceptions import OrderNotFoundError, PaymentFailedError, InsufficientStockError

class OrderService:
    def __init__(
        self, 
        order_repository: IOrderRepository,
        payment_repository: IPaymentRepository,
        cart_repository: ICartRepository,
        product_repository: IProductRepository
    ):
        self.order_repository = order_repository
        self.payment_repository = payment_repository
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def create_order_from_cart(
        self, 
        user_id: int, 
        shipping_address: str,
        order_type: str = "buy"
    ) -> Order:
        """Tạo đơn hàng từ giỏ hàng"""
        # Lấy giỏ hàng
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart or not cart.items:
            raise ValueError("Cart is empty")

        # Kiểm tra tồn kho
        for cart_item in cart.items:
            product = self.product_repository.get_product_by_id(cart_item.product_id)
            if not product:
                raise ValueError(f"Product {cart_item.product_id} not found")
            
            if product.total_quantity < cart_item.quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for product {product.name}. "
                    f"Available: {product.total_quantity}, Requested: {cart_item.quantity}"
                )

        # Tạo order items từ cart items
        order_items = []
        for cart_item in cart.items:
            order_item = OrderItem(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                item_type=cart_item.item_type,
                rental_days=cart_item.rental_days
            )
            order_items.append(order_item)

        # Tính toán ngày thuê nếu là thuê
        rental_start_date = None
        rental_end_date = None
        expected_return_date = None
        
        if order_type == "rent":
            rental_start_date = datetime.utcnow()
            # Giả sử thuê 7 ngày mặc định, có thể điều chỉnh
            rental_end_date = rental_start_date + timedelta(days=7)
            expected_return_date = rental_end_date

        # Tạo đơn hàng
        total_amount = sum(item.total_price for item in order_items)
        order = Order(
            user_id=user_id,
            items=order_items,
            total_amount=total_amount,
            order_type=order_type,
            rental_start_date=rental_start_date,
            rental_end_date=rental_end_date,
            expected_return_date=expected_return_date,
            shipping_address=shipping_address,
            order_status="pending",
            payment_status="pending"
        )

        # Lưu đơn hàng
        created_order = self.order_repository.create_order(order)
        
        # Lưu order items
        for order_item in order_items:
            order_item.id = None  # Reset ID để tạo mới
            self.order_repository.create_order_item(order_item)

        # Xóa giỏ hàng sau khi tạo đơn hàng thành công
        self.cart_repository.clear_cart(user_id)

        return created_order

    def process_payment(
        self, 
        order_id: int, 
        payment_method: str,
        transaction_id: Optional[str] = None
    ) -> Payment:
        """Xử lý thanh toán cho đơn hàng"""
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")

        if order.payment_status == PaymentStatus.PAID.value:
            raise ValueError("Order already paid")

        # Tạo payment record
        payment = Payment(
            order_id=order_id,
            payment_method=payment_method,
            payment_amount=order.final_amount,
            transaction_id=transaction_id or f"TXN_{order_id}_{int(datetime.utcnow().timestamp())}"
        )

        # Giả lập xử lý thanh toán (trong thực tế sẽ gọi API ngân hàng)
        try:
            # Simulate payment processing
            payment.process_payment(payment.transaction_id)
            
            # Cập nhật trạng thái đơn hàng
            order.update_status(payment_status=PaymentStatus.PAID.value, order_status=OrderStatus.CONFIRMED.value)
            self.order_repository.update_order(order)
            
            # Lưu payment
            created_payment = self.payment_repository.create_payment(payment)
            
            return created_payment
            
        except Exception as e:
            # Xử lý lỗi thanh toán
            payment.payment_status = PaymentStatus.FAILED.value
            order.update_status(payment_status=PaymentStatus.FAILED.value)
            self.order_repository.update_order(order)
            self.payment_repository.create_payment(payment)
            
            raise PaymentFailedError(f"Payment failed: {str(e)}")

    def get_order(self, order_id: int) -> Order:
        """Lấy thông tin đơn hàng"""
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")
        return order

    def get_user_orders(self, user_id: int) -> List[Order]:
        """Lấy danh sách đơn hàng của user"""
        return self.order_repository.get_orders_by_user_id(user_id)

    def update_order_status(self, order_id: int, status: str) -> Order:
        """Cập nhật trạng thái đơn hàng"""
        order = self.get_order(order_id)
        order.update_status(order_status=status)
        return self.order_repository.update_order(order)

    def cancel_order(self, order_id: int) -> Order:
        """Hủy đơn hàng"""
        order = self.get_order(order_id)
        
        if order.order_status in [OrderStatus.DELIVERED.value, OrderStatus.CANCELLED.value]:
            raise ValueError("Cannot cancel order in current status")
        
        order.update_status(order_status=OrderStatus.CANCELLED.value)
        return self.order_repository.update_order(order)

    def refund_payment(self, order_id: int, refund_amount: float) -> Payment:
        """Hoàn tiền cho đơn hàng"""
        order = self.get_order(order_id)
        
        if order.payment_status != PaymentStatus.PAID.value:
            raise ValueError("Order not paid, cannot refund")
        
        # Lấy payment gần nhất
        payments = self.payment_repository.get_payments_by_order_id(order_id)
        if not payments:
            raise ValueError("No payment found for this order")
        
        latest_payment = max(payments, key=lambda p: p.payment_date)
        
        # Thực hiện hoàn tiền
        latest_payment.refund(refund_amount)
        self.payment_repository.update_payment(latest_payment)
        
        return latest_payment
