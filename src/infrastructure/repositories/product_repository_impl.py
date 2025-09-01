from typing import List
from src.domain.models.product import Product
from src.domain.repositories.product_repository import ProductRepository
from src.infrastructure.databases.database import SessionLocal  # repo đã có
from src.infrastructure.models.product_model import ProductModel

class ProductRepositoryImpl(ProductRepository):
    def get_all(self) -> List[Product]:
        session = SessionLocal()
        try:
            rows = session.query(ProductModel).all()
            return [Product(id=r.id, name=r.name, price=r.price) for r in rows]
        finally:
            session.close()
