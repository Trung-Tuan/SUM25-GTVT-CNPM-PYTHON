from typing import List, Optional
from domain.models.cart import Cart, CartItem
from domain.models.icart_repository import ICartRepository
from domain.models.iproduct_repository import IProductRepository
from domain.exceptions import ProductNotFoundError, CartNotFoundError

class CartService:
    def __init__(self, cart_repository: ICartRepository, product_repository: IProductRepository):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def get_cart(self, user_id: int) -> Cart:
        """Lấy giỏ hàng của user"""
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            # Tạo giỏ hàng mới nếu chưa có
            cart = Cart(user_id=user_id)
            cart = self.cart_repository.create_cart(cart)
        return cart

    def add_to_cart(
        self, 
        user_id: int, 
        product_id: int, 
        quantity: int = 1, 
        item_type: str = "buy",
        rental_days: Optional[int] = None
    ) -> Cart:
        """Thêm sản phẩm vào giỏ hàng"""
        # Kiểm tra sản phẩm có tồn tại không
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with id {product_id} not found")

        # Lấy giỏ hàng hiện tại
        cart = self.get_cart(user_id)

        # Xác định giá sản phẩm
        if item_type == "rent" and rental_days:
            if rental_days == 1:
                unit_price = product.price_1_day
            elif rental_days == 7:
                unit_price = product.price_1_week
            elif rental_days == 14:
                unit_price = product.price_2_weeks
            else:
                unit_price = product.price_1_day * rental_days
        else:
            unit_price = product.price

        # Thêm vào giỏ hàng
        cart.add_item(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            item_type=item_type,
            rental_days=rental_days
        )

        # Lưu giỏ hàng
        return self.cart_repository.update_cart(cart)

    def update_cart_item(
        self, 
        user_id: int, 
        product_id: int, 
        quantity: int, 
        item_type: str = "buy"
    ) -> Cart:
        """Cập nhật số lượng sản phẩm trong giỏ hàng"""
        cart = self.get_cart(user_id)
        
        if quantity <= 0:
            # Xóa sản phẩm nếu quantity <= 0
            cart.remove_item(product_id, item_type)
        else:
            # Cập nhật số lượng
            cart.update_quantity(product_id, quantity, item_type)

        return self.cart_repository.update_cart(cart)

    def remove_from_cart(self, user_id: int, product_id: int, item_type: str = "buy") -> Cart:
        """Xóa sản phẩm khỏi giỏ hàng"""
        cart = self.get_cart(user_id)
        cart.remove_item(product_id, item_type)
        return self.cart_repository.update_cart(cart)

    def clear_cart(self, user_id: int) -> Cart:
        """Xóa toàn bộ giỏ hàng"""
        cart = self.get_cart(user_id)
        cart.clear()
        return self.cart_repository.update_cart(cart)

    def get_cart_total(self, user_id: int) -> float:
        """Tính tổng tiền giỏ hàng"""
        cart = self.get_cart(user_id)
        return cart.get_total_amount()

    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Lấy danh sách sản phẩm trong giỏ hàng"""
        cart = self.get_cart(user_id)
        return cart.items
