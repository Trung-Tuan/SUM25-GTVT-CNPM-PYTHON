from typing import List
from src.domain.models.product import Product
from src.domain.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def get_products(self) -> List[Product]:
        return self.repo.get_all()
