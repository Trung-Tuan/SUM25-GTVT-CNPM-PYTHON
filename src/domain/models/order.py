from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class OrderType(Enum):
    BUY = "buy"
    RENT = "rent"

class OrderItem:
    def __init__(
        self,
        product_id: int,
        quantity: int,
        unit_price: float,
        item_type: str = "buy",
        rental_days: Optional[int] = None,
        return_status: Optional[str] = None,
        days_overdue: Optional[int] = None,
        late_fee: Optional[float] = None,
        damage_fee: Optional[float] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.item_type = item_type
        self.rental_days = rental_days
        self.return_status = return_status
        self.days_overdue = days_overdue
        self.late_fee = late_fee or 0.0
        self.damage_fee = damage_fee or 0.0
        self.total_price = self.calculate_total_price()

    def calculate_total_price(self) -> float:
        if self.item_type == "rent" and self.rental_days:
            return self.unit_price * self.rental_days * self.quantity
        return self.unit_price * self.quantity

class Order:
    def __init__(
        self,
        user_id: int,
        items: List[OrderItem],
        total_amount: float,
        deposit_amount: float = 0.0,
        discount_amount: float = 0.0,
        final_amount: float = None,
        order_type: str = "buy",
        rental_start_date: Optional[datetime] = None,
        rental_end_date: Optional[datetime] = None,
        expected_return_date: Optional[datetime] = None,
        actual_return_date: Optional[datetime] = None,
        order_status: str = "pending",
        payment_status: str = "pending",
        shipping_address: Optional[str] = None,
        supplier_id: Optional[int] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.items = items
        self.total_amount = total_amount
        self.deposit_amount = deposit_amount
        self.discount_amount = discount_amount
        self.final_amount = final_amount or (total_amount - discount_amount)
        self.order_type = order_type
        self.rental_start_date = rental_start_date
        self.rental_end_date = rental_end_date
        self.expected_return_date = expected_return_date
        self.actual_return_date = actual_return_date
        self.order_status = order_status
        self.payment_status = payment_status
        self.shipping_address = shipping_address
        self.supplier_id = supplier_id
        self.created_at = created_at or datetime.utcnow()

    def calculate_final_amount(self) -> float:
        return self.total_amount - self.discount_amount

    def update_status(self, order_status: str = None, payment_status: str = None):
        if order_status:
            self.order_status = order_status
        if payment_status:
            self.payment_status = payment_status

class Payment:
    def __init__(
        self,
        order_id: int,
        payment_method: str,
        payment_amount: float,
        payment_status: str = "pending",
        transaction_id: Optional[str] = None,
        platform_fee: float = 0.0,
        supplier_earnings: float = 0.0,
        refund_amount: float = 0.0,
        refund_date: Optional[datetime] = None,
        id: Optional[int] = None,
        payment_date: Optional[datetime] = None
    ):
        self.id = id
        self.order_id = order_id
        self.payment_method = payment_method
        self.payment_amount = payment_amount
        self.payment_status = payment_status
        self.transaction_id = transaction_id
        self.platform_fee = platform_fee
        self.supplier_earnings = supplier_earnings
        self.refund_amount = refund_amount
        self.refund_date = refund_date
        self.payment_date = payment_date or datetime.utcnow()

    def process_payment(self, transaction_id: str):
        self.transaction_id = transaction_id
        self.payment_status = "paid"

    def refund(self, refund_amount: float):
        self.refund_amount = refund_amount
        self.refund_date = datetime.utcnow()
        self.payment_status = "refunded"
