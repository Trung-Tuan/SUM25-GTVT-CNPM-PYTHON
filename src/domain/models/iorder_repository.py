from abc import ABC, abstractmethod
from typing import List, Optional
from .order import Order, OrderItem, Payment

class IOrderRepository(ABC):
    @abstractmethod
    def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def get_orders_by_user_id(self, user_id: int) -> List[Order]:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def delete_order(self, order_id: int) -> bool:
        pass

    @abstractmethod
    def get_order_items(self, order_id: int) -> List[OrderItem]:
        pass

    @abstractmethod
    def create_order_item(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    def delete_order_item(self, order_item_id: int) -> bool:
        pass

class IPaymentRepository(ABC):
    @abstractmethod
    def create_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        pass

    @abstractmethod
    def get_payments_by_order_id(self, order_id: int) -> List[Payment]:
        pass

    @abstractmethod
    def update_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def delete_payment(self, payment_id: int) -> bool:
        pass
