from abc import ABC, abstractmethod
from typing import List, Optional
from .cart import Cart, CartItem

class ICartRepository(ABC):
    @abstractmethod
    def get_cart_by_user_id(self, user_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def create_cart(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    def update_cart(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    def delete_cart(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def add_cart_item(self, user_id: int, cart_item: CartItem) -> bool:
        pass

    @abstractmethod
    def update_cart_item(self, user_id: int, product_id: int, quantity: int, item_type: str = "buy") -> bool:
        pass

    @abstractmethod
    def remove_cart_item(self, user_id: int, product_id: int, item_type: str = "buy") -> bool:
        pass

    @abstractmethod
    def clear_cart(self, user_id: int) -> bool:
        pass
