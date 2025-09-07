from typing import List, Optional
from datetime import datetime

class CartItem:
    def __init__(
        self,
        product_id: int,
        quantity: int,
        unit_price: float,
        item_type: str = "buy",  # "buy" or "rent"
        rental_days: Optional[int] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.item_type = item_type
        self.rental_days = rental_days
        self.total_price = self.calculate_total_price()

    def calculate_total_price(self) -> float:
        if self.item_type == "rent" and self.rental_days:
            return self.unit_price * self.rental_days * self.quantity
        return self.unit_price * self.quantity

class Cart:
    def __init__(
        self,
        user_id: int,
        items: List[CartItem] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.items = items or []
        self.created_at = created_at
        self.updated_at = updated_at

    def add_item(self, product_id: int, quantity: int, unit_price: float, item_type: str = "buy", rental_days: Optional[int] = None):
        # Kiểm tra xem sản phẩm đã có trong giỏ chưa
        for item in self.items:
            if item.product_id == product_id and item.item_type == item_type:
                item.quantity += quantity
                item.total_price = item.calculate_total_price()
                return
        
        # Nếu chưa có, thêm mới
        new_item = CartItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            item_type=item_type,
            rental_days=rental_days
        )
        self.items.append(new_item)

    def remove_item(self, product_id: int, item_type: str = "buy"):
        self.items = [item for item in self.items if not (item.product_id == product_id and item.item_type == item_type)]

    def update_quantity(self, product_id: int, quantity: int, item_type: str = "buy"):
        for item in self.items:
            if item.product_id == product_id and item.item_type == item_type:
                item.quantity = quantity
                item.total_price = item.calculate_total_price()
                break

    def get_total_amount(self) -> float:
        return sum(item.total_price for item in self.items)

    def clear(self):
        self.items = []
