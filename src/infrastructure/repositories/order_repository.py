from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.order import Order, OrderItem, Payment
from domain.models.iorder_repository import IOrderRepository, IPaymentRepository
from infrastructure.models.orders_model import Orders
from infrastructure.models.order_items_model import OrderItems
from infrastructure.models.payments_model import Payments

class OrderRepository(IOrderRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_order(self, order: Order) -> Order:
        order_model = Orders(
            user_id=order.user_id,
            total_amount=order.total_amount,
            deposit_amount=order.deposit_amount,
            discount_amount=order.discount_amount,
            final_amount=order.final_amount,
            order_type=order.order_type,
            rental_start_date=order.rental_start_date,
            rental_end_date=order.rental_end_date,
            expected_return_date=order.expected_return_date,
            actual_return_date=order.actual_return_date,
            order_status=order.order_status,
            payment_status=order.payment_status,
            shipping_address=order.shipping_address,
            supplier_id=order.supplier_id,
            created_at=order.created_at
        )
        
        self.db.add(order_model)
        self.db.commit()
        self.db.refresh(order_model)
        
        order.id = order_model.id
        return order

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        order_model = self.db.query(Orders).filter(Orders.id == order_id).first()
        if not order_model:
            return None
        
        # Lấy order items
        order_items = self.get_order_items(order_id)
        
        return Order(
            id=order_model.id,
            user_id=order_model.renter_id,  # Note: using renter_id as user_id
            items=order_items,
            total_amount=order_model.total_amount,
            deposit_amount=order_model.deposit_amount,
            discount_amount=order_model.discount_amount,
            final_amount=order_model.final_amount,
            order_type=order_model.order_type,
            rental_start_date=order_model.retal_start_date,  # Note: typo in model
            rental_end_date=order_model.rental_end_date,
            expected_return_date=order_model.expected_return_date,
            actual_return_date=order_model.actual_return_date,
            order_status=order_model.order_status,
            payment_status=order_model.payment_status,
            shipping_address=order_model.shipping_address,
            supplier_id=order_model.supplier_id,
            created_at=order_model.created_at
        )

    def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        order_models = self.db.query(Orders).filter(Orders.renter_id == user_id).all()
        orders = []
        
        for order_model in order_models:
            order_items = self.get_order_items(order_model.id)
            order = Order(
                id=order_model.id,
                user_id=order_model.renter_id,
                items=order_items,
                total_amount=order_model.total_amount,
                deposit_amount=order_model.deposit_amount,
                discount_amount=order_model.discount_amount,
                final_amount=order_model.final_amount,
                order_type=order_model.order_type,
                rental_start_date=order_model.retal_start_date,
                rental_end_date=order_model.rental_end_date,
                expected_return_date=order_model.expected_return_date,
                actual_return_date=order_model.actual_return_date,
                order_status=order_model.order_status,
                payment_status=order_model.payment_status,
                shipping_address=order_model.shipping_address,
                supplier_id=order_model.supplier_id,
                created_at=order_model.created_at
            )
            orders.append(order)
        
        return orders

    def update_order(self, order: Order) -> Order:
        order_model = self.db.query(Orders).filter(Orders.id == order.id).first()
        if not order_model:
            return self.create_order(order)
        
        order_model.total_amount = order.total_amount
        order_model.deposit_amount = order.deposit_amount
        order_model.discount_amount = order.discount_amount
        order_model.final_amount = order.final_amount
        order_model.order_type = order.order_type
        order_model.retal_start_date = order.rental_start_date
        order_model.rental_end_date = order.rental_end_date
        order_model.expected_return_date = order.expected_return_date
        order_model.actual_return_date = order.actual_return_date
        order_model.order_status = order.order_status
        order_model.payment_status = order.payment_status
        order_model.shipping_address = order.shipping_address
        order_model.supplier_id = order.supplier_id
        
        self.db.commit()
        return order

    def delete_order(self, order_id: int) -> bool:
        order_model = self.db.query(Orders).filter(Orders.id == order_id).first()
        if not order_model:
            return False
        
        # Xóa order items trước
        self.db.query(OrderItems).filter(OrderItems.order_id == order_id).delete()
        
        # Xóa order
        self.db.delete(order_model)
        self.db.commit()
        return True

    def get_order_items(self, order_id: int) -> List[OrderItem]:
        order_item_models = self.db.query(OrderItems).filter(OrderItems.order_id == order_id).all()
        order_items = []
        
        for item_model in order_item_models:
            order_item = OrderItem(
                id=item_model.id,
                product_id=item_model.toy_id,  # Note: using toy_id as product_id
                quantity=item_model.quantity,
                unit_price=item_model.unit_price,
                item_type=item_model.item_type,
                rental_days=None,  # Not stored in current model
                return_status=item_model.return_status,
                days_overdue=item_model.days_overdue,
                late_fee=item_model.late_fee,
                damage_fee=item_model.damage_fee
            )
            order_items.append(order_item)
        
        return order_items

    def create_order_item(self, order_item: OrderItem) -> OrderItem:
        order_item_model = OrderItems(
            order_id=order_item.order_id if hasattr(order_item, 'order_id') else None,
            toy_id=order_item.product_id,
            quantity=order_item.quantity,
            unit_price=order_item.unit_price,
            item_type=order_item.item_type,
            return_status=order_item.return_status,
            days_overdue=order_item.days_overdue,
            late_fee=order_item.late_fee,
            damage_fee=order_item.damage_fee
        )
        
        self.db.add(order_item_model)
        self.db.commit()
        self.db.refresh(order_item_model)
        
        order_item.id = order_item_model.id
        return order_item

    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        order_item_model = self.db.query(OrderItems).filter(OrderItems.id == order_item.id).first()
        if not order_item_model:
            return self.create_order_item(order_item)
        
        order_item_model.quantity = order_item.quantity
        order_item_model.unit_price = order_item.unit_price
        order_item_model.item_type = order_item.item_type
        order_item_model.return_status = order_item.return_status
        order_item_model.days_overdue = order_item.days_overdue
        order_item_model.late_fee = order_item.late_fee
        order_item_model.damage_fee = order_item.damage_fee
        
        self.db.commit()
        return order_item

    def delete_order_item(self, order_item_id: int) -> bool:
        order_item_model = self.db.query(OrderItems).filter(OrderItems.id == order_item_id).first()
        if not order_item_model:
            return False
        
        self.db.delete(order_item_model)
        self.db.commit()
        return True

class PaymentRepository(IPaymentRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_payment(self, payment: Payment) -> Payment:
        payment_model = Payments(
            order_id=payment.order_id,
            payment_method=payment.payment_method,
            payment_amount=payment.payment_amount,
            payment_status=payment.payment_status,
            transaction_id=payment.transaction_id,
            platform_fee=payment.platform_fee,
            supplier_earnings=payment.supplier_earnings,
            payment_date=payment.payment_date,
            refund_amount=payment.refund_amount,
            refund_date=payment.refund_date
        )
        
        self.db.add(payment_model)
        self.db.commit()
        self.db.refresh(payment_model)
        
        payment.id = payment_model.id
        return payment

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        payment_model = self.db.query(Payments).filter(Payments.id == payment_id).first()
        if not payment_model:
            return None
        
        return Payment(
            id=payment_model.id,
            order_id=payment_model.order_id,
            payment_method=payment_model.payment_method,
            payment_amount=float(payment_model.payment_amount),
            payment_status=payment_model.payment_status,
            transaction_id=payment_model.transaction_id,
            platform_fee=float(payment_model.platform_fee) if payment_model.platform_fee else 0.0,
            supplier_earnings=float(payment_model.supplier_earnings) if payment_model.supplier_earnings else 0.0,
            payment_date=payment_model.payment_date,
            refund_amount=float(payment_model.refund_amount) if payment_model.refund_amount else 0.0,
            refund_date=payment_model.refund_date
        )

    def get_payments_by_order_id(self, order_id: int) -> List[Payment]:
        payment_models = self.db.query(Payments).filter(Payments.order_id == order_id).all()
        payments = []
        
        for payment_model in payment_models:
            payment = Payment(
                id=payment_model.id,
                order_id=payment_model.order_id,
                payment_method=payment_model.payment_method,
                payment_amount=float(payment_model.payment_amount),
                payment_status=payment_model.payment_status,
                transaction_id=payment_model.transaction_id,
                platform_fee=float(payment_model.platform_fee) if payment_model.platform_fee else 0.0,
                supplier_earnings=float(payment_model.supplier_earnings) if payment_model.supplier_earnings else 0.0,
                payment_date=payment_model.payment_date,
                refund_amount=float(payment_model.refund_amount) if payment_model.refund_amount else 0.0,
                refund_date=payment_model.refund_date
            )
            payments.append(payment)
        
        return payments

    def update_payment(self, payment: Payment) -> Payment:
        payment_model = self.db.query(Payments).filter(Payments.id == payment.id).first()
        if not payment_model:
            return self.create_payment(payment)
        
        payment_model.payment_method = payment.payment_method
        payment_model.payment_amount = payment.payment_amount
        payment_model.payment_status = payment.payment_status
        payment_model.transaction_id = payment.transaction_id
        payment_model.platform_fee = payment.platform_fee
        payment_model.supplier_earnings = payment.supplier_earnings
        payment_model.payment_date = payment.payment_date
        payment_model.refund_amount = payment.refund_amount
        payment_model.refund_date = payment.refund_date
        
        self.db.commit()
        return payment

    def delete_payment(self, payment_id: int) -> bool:
        payment_model = self.db.query(Payments).filter(Payments.id == payment_id).first()
        if not payment_model:
            return False
        
        self.db.delete(payment_model)
        self.db.commit()
        return True
