from domain.models.iproduct_repository import IProductRepository
from domain.models.product import Product  # domain entity
from infrastructure.models.toys_model import Toys  # ORM
from sqlalchemy.orm import Session
from typing import Optional, List

class ProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Product]:
        product_models = self.session.query(Toys).all()
        return [
            Product(
                id=product_model.id,
                name=product_model.name,
                description=product_model.description,
                category=product_model.category,
                price=product_model.price_sale,
                quantity=product_model.available_quantity,
                is_available=(product_model.is_active == 1),
                image=product_model.image,
                rating=product_model.rating,
                reviews=product_model.reviews,
                created_at=product_model.created_at,
                updated_at=product_model.updated_at,
                min_age=product_model.min_age,
                max_age=product_model.max_age,
                toy_name=product_model.toy_name,
                brand=product_model.brand,
                total_quantity=product_model.total_quantity,
                price_1_day=product_model.price_1_day,
                price_1_week=product_model.price_1_week,
                price_2_weeks=product_model.price_2_weeks,
                is_for_sale=product_model.is_for_sale,
                is_for_rent=product_model.is_for_rent,
                status=product_model.status,
            )
            for product_model in product_models
        ]
    
