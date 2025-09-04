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
                price=product_model.price,
                created_at=product_model.created_at
            ) for product_model in product_models
        ]

