from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.cart import Cart, CartItem
from domain.models.icart_repository import ICartRepository
from infrastructure.models.cart_model import CartModel, CartItemModel

class CartRepository(ICartRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_cart_by_user_id(self, user_id: int) -> Optional[Cart]:
        cart_model = self.db.query(CartModel).filter(CartModel.user_id == user_id).first()
        if not cart_model:
            return None
        
        # Lấy cart items
        cart_item_models = self.db.query(CartItemModel).filter(CartItemModel.cart_id == cart_model.id).all()
        
        cart_items = []
        for item_model in cart_item_models:
            cart_item = CartItem(
                id=item_model.id,
                product_id=item_model.product_id,
                quantity=item_model.quantity,
                unit_price=item_model.unit_price,
                item_type=item_model.item_type,
                rental_days=item_model.rental_days
            )
            cart_items.append(cart_item)
        
        return Cart(
            id=cart_model.id,
            user_id=cart_model.user_id,
            items=cart_items,
            created_at=cart_model.created_at,
            updated_at=cart_model.updated_at
        )

    def create_cart(self, cart: Cart) -> Cart:
        cart_model = CartModel(
            user_id=cart.user_id,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )
        self.db.add(cart_model)
        self.db.commit()
        self.db.refresh(cart_model)
        
        cart.id = cart_model.id
        return cart

    def update_cart(self, cart: Cart) -> Cart:
        cart_model = self.db.query(CartModel).filter(CartModel.id == cart.id).first()
        if not cart_model:
            return self.create_cart(cart)
        
        cart_model.updated_at = cart.updated_at
        self.db.commit()
        
        # Cập nhật cart items
        self._update_cart_items(cart)
        
        return cart

    def _update_cart_items(self, cart: Cart):
        # Xóa tất cả cart items cũ
        self.db.query(CartItemModel).filter(CartItemModel.cart_id == cart.id).delete()
        
        # Thêm cart items mới
        for item in cart.items:
            cart_item_model = CartItemModel(
                cart_id=cart.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                item_type=item.item_type,
                rental_days=item.rental_days
            )
            self.db.add(cart_item_model)
        
        self.db.commit()

    def delete_cart(self, user_id: int) -> bool:
        cart_model = self.db.query(CartModel).filter(CartModel.user_id == user_id).first()
        if not cart_model:
            return False
        
        # Xóa cart items trước
        self.db.query(CartItemModel).filter(CartItemModel.cart_id == cart_model.id).delete()
        
        # Xóa cart
        self.db.delete(cart_model)
        self.db.commit()
        return True

    def add_cart_item(self, user_id: int, cart_item: CartItem) -> bool:
        cart = self.get_cart_by_user_id(user_id)
        if not cart:
            cart = Cart(user_id=user_id)
            cart = self.create_cart(cart)
        
        cart.add_item(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            item_type=cart_item.item_type,
            rental_days=cart_item.rental_days
        )
        
        self.update_cart(cart)
        return True

    def update_cart_item(self, user_id: int, product_id: int, quantity: int, item_type: str = "buy") -> bool:
        cart = self.get_cart_by_user_id(user_id)
        if not cart:
            return False
        
        cart.update_quantity(product_id, quantity, item_type)
        self.update_cart(cart)
        return True

    def remove_cart_item(self, user_id: int, product_id: int, item_type: str = "buy") -> bool:
        cart = self.get_cart_by_user_id(user_id)
        if not cart:
            return False
        
        cart.remove_item(product_id, item_type)
        self.update_cart(cart)
        return True

    def clear_cart(self, user_id: int) -> bool:
        cart = self.get_cart_by_user_id(user_id)
        if not cart:
            return False
        
        cart.clear()
        self.update_cart(cart)
        return True
